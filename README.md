# Matching Pandas Activity

Project for data ingestion, cleaning, consolidation, export, and visualization of student grades using Python, **pandas**, and **matplotlib**.

## Project Overview

This project reads student records and exam/activity scores from CSV files, cleans and validates the data (handling duplicates, missing values, and out-of-range marks), merges the datasets, computes grade summaries, exports the consolidated report to both CSV and JSON formats, and produces a bar chart visualization representing the average score across activities.

## Features

- **Data Ingestion & Cleaning**:
  - Reads `alumnos.csv` and `notas.csv` using `;` delimiter and UTF-8 encoding.
  - Retains student ID leading zeros using string types.
  - Removes duplicate records by `id_alumno`.
  - Normalizes and bounds numeric grades between 0 and 10.
  - Detects unmatched students and grades (students without marks, and grades without matching student profiles).
- **Consolidation**:
  - Performs a left join matching students with their grades.
  - Computes `total` (mean of valid activities) and `average` per student.
- **Reporting & Exporting**:
  - Displays a summary table in the terminal.
  - Exports reports to `datos/salida/report.csv` and `datos/salida/report.json`.
  - Validates integrity of exported files.
- **Data Visualization**:
  - Generates a bar chart comparing averages per activity (`Activity 1`, `Activity 2`, `Activity 3`) for students with all completed grades.
  - Saves chart to `datos/salida/media_actividades.png`.

## Project Structure

```text
matching_pandas/
├── datos/
│   ├── entrada/
│   │   ├── alumnos.csv       # Student data (id_alumno;nombre)
│   │   └── notas.csv         # Scores data (id_alumno;nota1;nota2;nota3)
│   └── salida/               # Generated reports and charts (auto-created)
│       ├── media_actividades.png
│       ├── report.csv
│       └── report.json
├── datos.py                  # Data processing, report generation & visualization functions
├── main.py                   # CLI interactive menu
├── requirements.txt          # Project dependencies (pandas, matplotlib)
└── README.md                 # Project documentation
```

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - `pandas`
  - `matplotlib`

## Installation & Setup

1. **Clone or open the repository**:
   ```bash
   cd matching_pandas
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main application:

```bash
python main.py
```

### Interactive Menu Options

```text
PANDAS ACTIVITY - MAIN MENU
1. Prepare data
2. Save report
3. Show graphic
4. Exit
```

1. **Prepare data**: Loads and validates the input datasets, reports missing/duplicated data, computes summary statistics, and prepares the internal dataset.
2. **Save report**: Shows a formatted table in the console, displays student completion stats, and saves both `report.csv` and `report.json` in `datos/salida/`.
3. **Show graphic**: Computes the mean for each activity (for students with complete scores), saves the chart to `datos/salida/media_actividades.png`, and displays it.
4. **Exit**: Closes the program.
