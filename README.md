# Humanity's Last Exam

A web-based quiz viewer for the [Humanity's Last Exam](https://huggingface.co/datasets/cais/hle) (HLE) benchmark dataset — 2,500 expert-level questions across math, science, humanities, and more.

## Quick Start

1. **Open the app** at [jakeoil.github.io/last-exam](https://jakeoil.github.io/last-exam/)

2. **Download the dataset** from HuggingFace (requires a free account):
   [huggingface.co/datasets/cais/hle/tree/main/data](https://huggingface.co/datasets/cais/hle/tree/main/data)
   — download the `test-00000-of-00001.parquet` file.

3. **Drop the file** onto the page. It's decoded locally in your browser — nothing is uploaded.

That's it. Your data is cached in the browser so you only need to drop the file once. Use the **Clear** button in the header to reset and re-upload if needed.

## Features

- Multiple choice and exact match question types
- Category and type filters, search, shuffle
- Keyboard navigation (arrow keys, Enter to submit, R to reveal)
- LaTeX rendering via MathJax
- Chess FEN notation rendered as inline boards
- Score tracking persisted across sessions

## Local Development

If you prefer to run locally:

```bash
pip install pandas pyarrow
python convert.py test-00000-of-00001.parquet
python3 -m http.server 8080
open http://localhost:8080
```

This converts the parquet file to `questions.json`, which the app loads directly (skipping the drag-and-drop flow).
