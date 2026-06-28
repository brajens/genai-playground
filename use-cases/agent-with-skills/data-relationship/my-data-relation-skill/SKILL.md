---
name: my-data-relation-skill
description: This skill identifies Primary Keys (PK), Foreign Keys (FK), and 1-to-many structural relationships between CSV datasets using ONLY data values — no column names, no semantic matching, no embeddings, no metadata. It uses statistical analysis (uniqueness ratios, inclusion dependencies, coefficient of variation) to find true ID-to-ID foreign key relationships while filtering out coincidental value matches (like amounts appearing in both tables)..
---


# my-data-relation-skill

## Relationship Rules

### Primary Key Rule

A column is a Primary Key candidate if:

```python
uniqueness_ratio > 0.95
```

Meaning:

```python
COUNT(DISTINCT column) / COUNT(*) > 0.95
```

### Structural PK Filter

Not all unique columns are meaningful PKs for joining. After identifying PK candidates, classify each as **identifier** or **measure**:

A column is likely an **identifier** (good PK) if ANY of:
- Values are strings (even if numeric-looking, e.g. "S001", "TX002")
- Values are integers with low coefficient of variation (CV < 0.5) — sequential IDs
- Values follow a consistent pattern (common prefix + incrementing suffix)

A column is likely a **measure** (bad PK — skip it) if ALL of:
- Values are purely numeric (int or float)
- High coefficient of variation (CV > 0.5)
- No common prefix or pattern
- Values look like amounts, scores, or quantities

Only **identifier** PKs should be used as join targets.

Calculate:

```python
cv = std(values) / mean(values)  # coefficient of variation
is_string_type = any non-numeric values exist
has_prefix = values share a common alphanumeric prefix
is_sequential = values form a near-contiguous integer range
is_identifier_pk = is_string_type OR has_prefix OR is_sequential OR cv < 0.5
```

### Foreign Key Rule

A column is a Foreign Key if:
1. values repeat (uniqueness_ratio < 0.95)
2. values exist inside an **identifier** PK column (not a measure PK)

Meaning:

```python
child_values ⊆ parent_identifier_pk_values
```

## Workflow

### STEP 1: Load Datasets

Load datasets using DuckDB.

```python
import duckdb
```

### STEP 2: Calculate Column Statistics

For every dataset:
- identify columns
- calculate: total rows, distinct values, uniqueness ratio, data type (string vs numeric)

### STEP 3: Identify and Filter Primary Key Candidates

Rule:

```python
uniqueness_ratio > 0.95
```

Then apply the **Structural PK Filter** to classify each candidate as identifier or measure. Discard measure columns — they are not valid join targets.

Why: A column of unique dollar amounts (250, 120, 500...) passes the uniqueness test but is not a meaningful FK target. Structural FKs reference identifiers like customer IDs, order codes, or sequential keys.

### STEP 4: Compare Columns Across Datasets

Compare repeating columns (uniqueness_ratio < 0.95) against **identifier PK** columns across datasets.

Do NOT compare:
- PK vs PK
- same dataset columns
- against measure PKs

### STEP 5: Validate Inclusion Dependency

Use SQL similar to:

```sql
SELECT
    COUNT(DISTINCT child.column) as child_unique,
    COUNT(DISTINCT parent.column) as matched
FROM child
LEFT JOIN parent
ON CAST(child.column AS VARCHAR) = CAST(parent.column AS VARCHAR)
WHERE parent.column IS NOT NULL
```

Calculate:

```python
inclusion_score = matched / child_unique
```

### STEP 6: Determine Relationships

If:

```python
inclusion_score > 0.90
```

Then a structural relationship exists.

## Expected Output Format

Return:

```json
[
  {
    "parent_dataset": "customers",
    "parent_column": "col_1",
    "child_dataset": "sales",
    "child_column": "col_b",
    "relationship": "1_to_many",
    "inclusion_score": 1.0
  }
]
```

## Performance Guidance

For large datasets:
- use DuckDB
- avoid loading full CSVs into memory
- avoid Pandas unless necessary
- use SQL aggregation
- avoid row-by-row Python loops

## Important Constraints

DO NOT:
- use column names
- use embeddings
- use LLM reasoning for joins
- infer semantics from headers

ONLY use:
- uniqueness
- duplicates
- inclusion dependency
- statistical validation
- data type classification (string vs numeric)
- coefficient of variation for identifier detection

## Example Usage

Input datasets:
- customers.csv
- sales.csv
- transactions.csv

Expected relationships:

```text
customers.col_1 → sales.col_b     (ID → ID)
sales.col_a → transactions.x2     (ID → ID)
```

NOT expected (filtered out):

```text
sales.col_c → transactions.x3     (amount → amount, not structural)
```
