# Data Intelligence Platform

**A Python-based platform for data automation, validation, analytics, reporting, and execution monitoring.**

An extensible data processing application designed to transform raw business datasets into validated information, analytical insights, and structured reports.

Built with Python, pandas, SQLite, Streamlit, and automated testing.

## Overview

Data Intelligence Platform provides a modular workflow for processing structured business data.

The application supports CSV, Excel, and JSON ingestion, data quality validation, sales analysis, anomaly detection, Excel report generation, and persistent execution tracking.

It includes a command-line interface (CLI) for running data pipelines and a Streamlit dashboard for monitoring historical executions.

### Key Features

- **Multi-format ingestion:** Import datasets from CSV, XLSX, and JSON files.
- **Data validation:** Check required fields, missing values, duplicate identifiers, and invalid numerical data.
- **Data transformation:** Standardize text, convert numerical fields, and calculate sales totals.
- **Business analytics:** Calculate revenue, sales volume, product performance, and category-level metrics.
- **Anomaly detection:** Identify potential outliers using an interquartile range (IQR) approach.
- **Excel reporting:** Generate formatted workbooks containing KPIs, processed data, and charts.
- **Execution tracking:** Store processing results, failures, timestamps, and execution metadata in SQLite.
- **CLI:** Run processing jobs and inspect execution history from the terminal.
- **Monitoring dashboard:** Explore execution history, performance metrics, and processing status through Streamlit.
- **Automated testing:** Validate core business logic and persistence with pytest.

## Technology Stack

| Category | Technology |
|---|---|
| Language | Python 3.13 |
| Data processing | pandas |
| Excel input | openpyxl |
| Excel reporting | XlsxWriter |
| Database | SQLite |
| Dashboard | Streamlit |
| Testing | pytest |
| Linting and formatting | Ruff |
| Packaging | setuptools / pyproject.toml |
| Version control | Git and GitHub |

## Architecture

The application follows a modular architecture, separating ingestion, validation, transformation, analysis, reporting, and persistence.

```text
data-intelligence-platform/
├── src/
│   └── automacao_dados/
│       ├── analysis/
│       │   ├── anomaly_detector.py
│       │   └── sales_analyzer.py
│       ├── ingestion/
│       │   ├── csv_reader.py
│       │   ├── excel_reader.py
│       │   └── json_reader.py
│       ├── processing/
│       │   └── data_processor.py
│       ├── reporting/
│       │   └── excel_report.py
│       ├── validation/
│       │   └── data_validator.py
│       ├── cli.py
│       ├── config.py
│       ├── dashboard.py
│       ├── exceptions.py
│       ├── history.py
│       ├── logging_config.py
│       └── pipeline.py
├── tests/
├── data/
│   ├── raw/
│   ├── processed/
│   └── reports/
├── .gitignore
├── pyproject.toml
└── README.md
```

Data directories are created or populated locally as needed. Generated files and local databases are excluded from version control.

### Processing Flow

```text
CSV / Excel / JSON
        |
        v
   Data Ingestion
        |
        v
   Data Validation
        |
        v
  Data Transformation
        |
        v
   Business Analytics
        |
        +----> Anomaly Detection
        |
        v
   Excel Reporting
        |
        v
  SQLite Execution History
        |
        v
  Streamlit Monitoring
```

The CLI orchestrates processing operations, while the dashboard reads persisted execution data.

## Getting Started

### Prerequisites

- Python 3.13 or later, within the supported dependency constraints
- Git
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/DARK3KN1GHT/data-intelligence-platform.git
cd data-intelligence-platform
```

### 2. Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -e ".[dev]"
```

This installs the application in editable mode, together with its development tools.

### 4. Prepare a Dataset

Create a directory named `data/raw` and place a supported data file inside it.

For example, create `data/raw/vendas.csv`:

```csv
id,produto,categoria,quantidade,preco_unitario
1,Notebook,Eletronicos,2,3500.00
2,Mouse,Perifericos,5,80.00
3,Teclado,Perifericos,3,150.00
4,Monitor,Eletronicos,2,1200.00
5,Cadeira,Moveis,1,900.00
```

The current sales pipeline expects the following columns:

| Column | Description |
|---|---|
| `id` | Unique record identifier |
| `produto` | Product name |
| `categoria` | Product category |
| `quantidade` | Quantity sold |
| `preco_unitario` | Price per unit |

The pipeline calculates `valor_total` during processing.

## Command-Line Interface

### Run the Pipeline

```bash
automacao-dados run --input data/raw/vendas.csv
```

Supported input formats:

```bash
automacao-dados run --input data/raw/vendas.csv
automacao-dados run --input data/raw/vendas.xlsx
automacao-dados run --input data/raw/vendas.json
```

### Custom Report Directory

```bash
automacao-dados run --input data/raw/vendas.csv --output data/reports/custom
```

### View Execution History

```bash
automacao-dados history --limit 10
```

### CLI Help

```bash
automacao-dados --help
automacao-dados run --help
```

## Analytics

The current analytics module calculates:

- Total revenue
- Total quantity sold
- Revenue per unit sold
- Highest-revenue product
- Most-sold product
- Revenue by category

For the example CSV dataset:

| Metric | Result |
|---|---:|
| Total revenue | R$ 11,150.00 |
| Units sold | 13 |
| Average revenue per unit | R$ 857.69 |
| Highest-revenue product | Notebook |
| Most-sold product | Mouse |

These metrics describe the sample dataset and are not application benchmarks.

## Anomaly Detection

The platform uses a configurable-in-code interquartile range (IQR) approach to identify unusually high or low numerical values.

The current implementation analyzes:

- `quantidade`
- `preco_unitario`
- `valor_total`

**Current limitation:** statistical detection is skipped for columns with fewer than six valid numerical observations. Therefore, zero detected anomalies does not necessarily mean the dataset has been statistically assessed.

An explicit insufficient-data status is planned for a future release.

## Excel Reporting

The platform generates Excel workbooks containing:

- An executive summary
- Sales KPIs
- Revenue by category
- Charts
- Processed records

Each CLI execution receives a unique UUID, which is included in generated filenames to avoid overwriting previous execution reports.

Generated files are stored locally and excluded from Git tracking.

## Execution History

SQLite provides persistent execution tracking.

Each execution stores information such as:

| Field | Description |
|---|---|
| Execution ID | Unique UUID |
| Input file | Original dataset |
| Status | RUNNING, SUCCESS, or FAILED |
| Started at | Execution start timestamp |
| Finished at | Execution completion timestamp |
| Duration | Processing duration |
| Records processed | Total processed records |
| Revenue | Calculated sales revenue |
| Anomalies | Number of detected anomalies |
| Report file | Generated report location |
| Error message | Failure details, when applicable |

The database is automatically initialized when the execution repository is created.

## Monitoring Dashboard

A Streamlit-based monitoring interface is included in the project.

To launch it:

```bash
python -m streamlit run src/automacao_dados/dashboard.py
```

Open the local address displayed by Streamlit, typically:

`http://localhost:8501`

The dashboard is designed to provide execution metrics, status distribution, historical activity, filtering, execution details, and report downloads.

**Development status:** the initial dashboard implementation is included, but its interface and end-to-end behavior are still being refined.

## Testing and Code Quality

Run all automated tests:

```bash
python -m pytest -q
```

Check coding standards:

```bash
python -m ruff check .
```

Check formatting:

```bash
python -m ruff format --check .
```

Apply formatting:

```bash
python -m ruff format .
```

The current test suite contains **23 passing tests**, covering core validation, processing, analytics, anomaly detection, and SQLite execution history.

Additional CLI, report-generation, and integration tests are planned.

## Security and Data Handling

The repository excludes local runtime artifacts such as:

- Virtual environments
- Environment variable files
- SQLite databases
- Log files
- Raw business datasets
- Generated reports

Avoid committing real customer information, API keys, access tokens, credentials, or other sensitive data.

The current application is intended for local development and further engineering, rather than deployment as a hardened multi-user service.

## Roadmap

- [x] CSV, Excel, and JSON ingestion
- [x] Data validation and transformation
- [x] Business analytics
- [x] Initial anomaly detection
- [x] Excel reporting
- [x] CLI and structured logging
- [x] SQLite execution history
- [x] UUID-based execution tracking
- [x] Initial Streamlit dashboard implementation
- [x] Unit tests and Ruff configuration
- [ ] Expanded integration and CLI testing
- [ ] Refined monitoring dashboard
- [ ] Improved anomaly detection diagnostics
- [ ] Historical dataset analysis and richer reporting
- [ ] GitHub Actions continuous integration
- [ ] REST API
- [ ] AI-assisted executive summaries
- [ ] Docker packaging and deployment configuration

## Project Goals

This project is being developed as a practical software engineering and data engineering portfolio project.

Its goals include:

- Building maintainable Python applications
- Designing modular data pipelines
- Applying automated validation and testing
- Implementing persistent execution tracking
- Creating business-oriented analytical outputs
- Improving software quality and deployment practices

## Author

**DARK3KN1GHT**

GitHub: https://github.com/DARK3KN1GHT

---

*Data Intelligence Platform — Python, automation, analytics, and software engineering.*