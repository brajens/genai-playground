from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent, tool
import boto3, uuid, datetime
from strands.models import BedrockModel

model_id = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
model = BedrockModel(
    model_id=model_id,
)

TABLE = "agent_records"
table = boto3.resource("dynamodb").Table(TABLE)

@tool
def save_record(content: str) -> str:
    """Save a text record to the database. Returns the new record_id."""
    rid = str(uuid.uuid4())
    table.put_item(Item={"id": rid, "content": content,
                         "created_at": datetime.datetime.utcnow().isoformat()})
    return rid

agent = Agent(
    model=model,
    tools=[save_record],
    system_prompt="You save records. Call save_record then report the record_id.",
)

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload):
    result = agent(payload.get("prompt", ""))
    return {"result": result.message}

if __name__ == "__main__":
    app.run()
