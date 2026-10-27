from pathlib import Path
import pandas as pd
# pyrefly: ignore[missing-import]
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parent
INPUT_DIR = BASE_DIR / 'datos' / 'entrada'
OUTPUT_DIR = BASE_DIR / 'datos' / 'salida'
ALUMNS = 'alumnos.csv'
CALIFICATIONS = 'notas.csv'
MIN_CAL = 0
MAX_CAL = 10
REPORT_CSV = 'report.csv'
REPORT_JSON = 'report.json'


def prepare_data():
    alumns_path = INPUT_DIR / ALUMNS
    califications_path = INPUT_DIR / CALIFICATIONS

    if not alumns_path.exists() or not califications_path.exists():
        print(f'Error: {ALUMNS} or {CALIFICATIONS} was not found')
        return None, None

    try:
        df_alumns = pd.read_csv(alumns_path, sep=';', encoding='utf-8', dtype={'id_alumno': str})
        df_califications = pd.read_csv(califications_path, sep=';', encoding='utf-8', dtype={'id_alumno': str})
    except Exception as e:
        print(f'Error while loading files: {e}')
        return None, None

    required_alumns_col = {'id_alumno', 'nombre'}
    required_califications_col = {'id_alumno', 'nota1', 'nota2', 'nota3'}
    if not required_alumns_col.issubset(df_alumns.columns) or not required_califications_col.issubset(df_califications.columns):
        print(f'Review {ALUMNS} or {CALIFICATIONS}: Missing columns')
        return None, None
    
    if df_califications['id_alumno'].duplicated().any():
        print(f'Review {CALIFICATIONS}: Duplicated identifiers')
        return None

    initial_rows = len(df_alumns)
    df_alumns = df_alumns.drop_duplicates(subset = ['id_alumno']).copy()
    removed_rows = initial_rows - len(df_alumns)
    
    if removed_rows > 0:
        print(f'{ALUMNS}: Removed {removed_rows} duplicate rows based on id_alumno')
    
    califications_cols = ['nota1', 'nota2', 'nota3']
    for col in califications_cols:
        df_califications[col] = pd.to_numeric(df_califications[col], errors='coerce').round(2)
        df_califications.loc[(df_califications[col] < MIN_CAL) | (df_califications[col] > MAX_CAL), col] = float('nan')
    
    alumns_id = set(df_alumns['id_alumno'])
    califications_id = set(df_califications['id_alumno'])

    no_calification_alumns = sorted(list(alumns_id - califications_id))
    no_alumns_califications = sorted(list(califications_id - alumns_id))

    print(f"Alumns without califications: {', '.join(no_calification_alumns) if no_calification_alumns else 'None'}")
    print(f"Califications without alumns: {', '.join(no_alumns_califications) if no_alumns_califications else 'None'}")

    if not (alumns_id & califications_id):
        print(f'Warning: No coincidences in merge')
        return None, None

    report = pd.merge(df_alumns, df_califications, on='id_alumno', how='left')
    
    if report[califications_cols].isna().all().all():
        print(f'Error: The report doesnt contain valid califications')
        return None

    report['total'] = report[califications_cols].mean(axis=1).round(2)
    report['average'] = (report['total'] / 3).round(2)

    report = report.sort_values('id_alumno').reset_index(drop=True)
    
    return report

def save_report(report):
    if report is None:
        return
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    csv_path = OUTPUT_DIR / REPORT_CSV
    json_path = OUTPUT_DIR / REPORT_JSON

    report.to_csv(csv_path, sep=';', index=False, encoding='utf-8')
    report.to_json(json_path, orient='records', indent=4, force_ascii=False)

    df_read_csv = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    df_read_json = pd.read_json(json_path, dtype={'id_alumno': str}, orient='records')

    csv_comprobation = (
        len(df_read_csv) == len(report)
        and list(df_read_csv.columns) == list(report.columns)
        and list(df_read_csv['id_alumno']) == list(report['id_alumno'])
    )
    json_comprobation = (
        len(df_read_json) == len(report)
        and list(df_read_json.columns) == list(report.columns)
        and list(df_read_json["id_alumno"]) == list(report["id_alumno"])
    )

    show_columns = ['id_alumno', 'nombre', 'nota1', 'nota2', 'nota3', 'total', 'average']
    table_show = report[show_columns].fillna('N/A')
    print(f'\n{table_show.to_string(index=False)}\n')
    
    total_alumns = len(report)
    completed = report["average"].notna().sum()
    pending = total_alumns - completed
    print(f"\nTotal alumns: {total_alumns} | Completed: {completed} | Pending: {pending}")

    if csv_comprobation and json_comprobation:
        print("CSV and JSON saved and checked in datos/salida.")

    
def show_graphic(report):
    if report is None:
        return
    
    califications_cols = ['nota1', 'nota2', 'nota3']

    complete_alumns = report[report[califications_cols].notna().all(axis=1)]
    alumn_num = len(complete_alumns)

    if alumn_num == 0:
        print('No data available to display')
        return
    
    average = complete_alumns[califications_cols].mean().round(2)
    
    plt.figure(figsize=(10,6))
    tags = ['Activity 1', 'Activity 2', 'Activity 3']
    plt.bar(tags, average, color='#2978a0', width=0.5)

    plt.ylim(0, 10)
    plt.ylabel("Nota media")
    plt.title(f"Media por actividad ({alumn_num} alumnos)")
    plt.tight_layout()

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    graphic_path = OUTPUT_DIR / 'media_actividades.png'
    plt.savefig(graphic_path)
    print(f'Graphic saved to {graphic_path.resolve()}')

    plt.show()
    plt.close()