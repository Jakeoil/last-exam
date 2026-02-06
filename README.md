# Humanity's Last Exam

A web-based viewer for the [Humanity's Last Exam](https://huggingface.co/datasets/centerforaisafety/hle) (HLE) benchmark dataset, which contains 2,500 expert-level questions across math, science, humanities, and more.

## Setup

1. Download the parquet file from [HuggingFace](https://huggingface.co/datasets/centerforaisafety/hle):

2. Install dependencies and convert to JSON:

```bash
pip install pandas pyarrow
python convert.py test-00000-of-00001.parquet
```

3. Start a local server and open in your browser:

```bash
python3 -m http.server 8080
open http://localhost:8080
```

The `convert.py` script reads the parquet file and produces `questions.json`, which the web viewer loads. You can also specify a custom output path:

```bash
python convert.py test-00000-of-00001.parquet my_output.json
```

## What is a Parquet File?

Parquet is a **binary columnar storage format** — it is not human-readable text. If you open a `.parquet` file in a text editor, you'll see gibberish. The file starts and ends with the magic bytes `PAR1`, which is how tools identify it.

### Why not just use CSV or JSON?

| | CSV/JSON | Parquet |
|---|---|---|
| Format | Text, human-readable | Binary, not human-readable |
| Storage | Row-oriented | Column-oriented |
| Compression | None (or external) | Built-in (Snappy, gzip, etc.) |
| Size | Large | Much smaller |
| Read speed | Must scan entire file | Can read individual columns |
| Schema | Implicit (CSV) or flexible (JSON) | Strict, embedded schema |
| Types | Everything is a string (CSV) | Native int, float, binary, nested structs |

Parquet shines for datasets with many columns where you only need a few at a time, or where storage/transfer size matters. This dataset is 274MB as Parquet — the exported JSON with base64 images is 117MB for just the text fields, but Parquet also stores binary image data natively.

### How is data stored inside?

Parquet files organize data into **row groups** (horizontal partitions) and **columns** (vertical partitions). This file has:

- **25 row groups**, each containing ~100 rows
- **14 columns** (id, question, image, image_preview.bytes, image_preview.path, answer, answer_type, author_name, rationale, rationale_image.bytes, rationale_image.path, raw_subject, category, canary)
- **2,500 total rows**

When you read a single column, Parquet only loads that column's data from disk, skipping everything else. This is why it's fast for analytics on wide tables.

### How to read a Parquet file

**Python with pandas** (most common):

```python
pip install pandas pyarrow

import pandas as pd
df = pd.read_parquet("test-00000-of-00001.parquet")
print(df.shape)        # (2500, 12)
print(df.columns)      # ['id', 'question', 'image', ...]
print(df.head())       # first 5 rows
```

**Python with pyarrow** (lower-level, inspect metadata):

```python
import pyarrow.parquet as pq

f = pq.ParquetFile("test-00000-of-00001.parquet")
print(f.schema)              # column names and types
print(f.metadata.num_rows)   # 2500
print(f.metadata.created_by) # parquet-cpp-arrow version 16.1.0

# Read just one column
table = f.read(columns=["question"])
```

**Command-line** with `parquet-tools`:

```bash
pip install parquet-tools
parquet-tools show test-00000-of-00001.parquet
parquet-tools schema test-00000-of-00001.parquet
```

**Other languages**: Parquet has native readers in Java, Rust, Go, R, JavaScript, and most data-oriented languages. It was originally created by Twitter and Cloudera for the Apache Hadoop ecosystem.

### Schema of this dataset

```
id              string    Unique question identifier
question        string    The question text (may include answer choices)
image           string    Base64-encoded image data URI (if the question has an image)
image_preview   struct    {bytes, path} - thumbnail preview
answer          string    The correct answer
answer_type     string    "multipleChoice" or "exactMatch"
author_name     string    Question author
rationale       string    Explanation of the answer
rationale_image struct    {bytes, path} - image for the rationale
raw_subject     string    Subject area (e.g., "Chess", "Philosophy", "Algebraic Geometry")
category        string    Broad category (Math, Physics, Biology/Medicine, etc.)
canary          string    Training data contamination canary string
```
