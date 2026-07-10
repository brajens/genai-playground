import json, re, boto3

TABLE = "agent_records"
table = boto3.resource("dynamodb").Table(TABLE)

UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

def _record_exists(rid):
    return "Item" in table.get_item(Key={"id": rid})

def _collect_strings(obj, out):
    """Recursively gather all string values from a nested span object."""
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _collect_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _collect_strings(v, out)

def _is_save_record_span(span):
    blob = json.dumps(span).lower()
    return "save_record" in blob

def lambda_handler(event, context=None):
    """AgentCore code-based evaluator: verify save_record persisted a record to DynamoDB.

    Robust to span-format differences: rather than relying on a specific attribute
    name, it scans every string in the save_record tool span for a UUID and checks
    each candidate against DynamoDB.
    """
    try:
        spans = event.get("evaluationInput", {}).get("sessionSpans", [])
        target = (event.get("evaluationTarget") or {}).get("traceIds", [None])[0]

        # Prefer spans that mention save_record; fall back to all spans in the target trace.
        candidate_spans = [s for s in spans if _is_save_record_span(s)]
        if not candidate_spans:
            candidate_spans = [s for s in spans
                               if not target or s.get("traceId") == target]

        if not candidate_spans:
            return {"label": "FAIL", "value": 0.0,
                    "explanation": "No save_record tool span found in the session."}

        # Gather all UUIDs mentioned in those spans, check each against the table.
        checked = []
        for span in candidate_spans:
            strings = []
            _collect_strings(span, strings)
            for text in strings:
                for rid in UUID_RE.findall(text):
                    if rid in checked:
                        continue
                    checked.append(rid)
                    if _record_exists(rid):
                        return {"label": "PASS", "value": 1.0,
                                "explanation": f"Record {rid} found in DynamoDB."}

        if checked:
            return {"label": "FAIL", "value": 0.0,
                    "explanation": f"Found record id(s) {checked} in the trace but none exist in DynamoDB."}
        return {"label": "FAIL", "value": 0.0,
                "explanation": "save_record span found but no record_id (UUID) present in it. "
                               "Check that tool input/output is captured in spans."}
    except Exception as e:
        return {"errorCode": "EVALUATION_ERROR", "errorMessage": str(e)}
