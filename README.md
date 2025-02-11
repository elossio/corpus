---

# Pharmaceutical Corpus Builder

This repository contains a Python script (`create_corpus.py`) to build and preprocess a structured pharmaceutical corpus from Excel datasets. The corpus maps active principles (e.g., drug compounds) to their associated product names, with support for text normalization and synonym handling. Designed for Portuguese medical datasets (e.g., ABCFarma), it outputs a JSON corpus and a preprocessed Parquet file.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Input Dataset Format](#input-dataset-format)
6. [Output](#output)
7. [Customization](#customization)
8. [License](#license)
9. [Contributing](#contributing)

---

## Features

- Load pharmaceutical datasets from Excel (or CSV) files.
- Preprocess and clean text data (lowercasing, missing value handling).
- Normalize text using spaCy (lemmatization, stopword removal).
- Generate a structured corpus mapping active principles to product names.
- Save outputs as JSON (corpus) and Parquet (preprocessed data).
- Portuguese language support via `pt_core_news_sm` spaCy model.

---

## Prerequisites

- Python 3.7+
- Required libraries:
  ```bash
  pip install pandas spacy nltk openpyxl
  python -m spacy download pt_core_news_sm  # Portuguese language model
  ```

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/pharmaceutical-corpus-builder.git
   cd pharmaceutical-corpus-builder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt  # Create this file if needed
   ```

---

## Usage

### Step 1: Configure Paths
Modify the following variables in `create_corpus.py`:
```python
TERMO = 'nome'          # Column name for product names
SINONIMO = 'composição' # Column name for active principles
ORIGEM = 'abcfarma'     # Dataset identifier (used for output naming)
DATASET_FILE = '/path/to/your/dataset.xlsx'  # Input Excel file
CORPUS_FILE = '/path/to/output/corpus.json'  # Output JSON corpus
```

### Step 2: Run the Script
```bash
python create_corpus.py
```

---

## Input Dataset Format

- **File Format**: Excel (`.xlsx`) with a sheet named `Planilha1`.
- **Required Columns**:
  - `nome`: Product names (e.g., "Paracetamol 500mg").
  - `composição`: Active principles (e.g., "paracetamol").
- Example:
  | nome                 | composição | ...other_columns |
  |----------------------|------------|------------------|
  | Dipirona Sódica 500mg| dipirona   | ...              |

---

## Output

1. **Corpus (JSON)**:
   ```json
   {
     "dipirona": ["dipirona sódica 500mg", "dipirona composto"],
     "paracetamol": ["paracetamol 500mg"]
   }
   ```
2. **Preprocessed Data (Parquet)**:  
   Saved as `abcfarma.parquet` (or your specified `ORIGEM` value).

---

## Customization

### Adjust Preprocessing
Modify these methods in `Corpus` class:
- `preprocess_dataset()`: Customize column renaming/text standardization.
- `normalize_text()`: Change spaCy-based lemmatization rules.
- `get_synonyms()`: Add/remove synonym extraction logic (uses WordNet).

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).

---

## Contributing

Contributions are welcome!  
1. Fork the repository.  
2. Create a feature branch.  
3. Submit a pull request with a description of changes.  

---

**Note**: Ensure compliance with data usage rights when working with proprietary datasets.
