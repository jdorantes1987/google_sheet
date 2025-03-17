import gspread
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build

# Autenticación y acceso a Google Sheets
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]
creds = ServiceAccountCredentials.from_json_keyfile_name("key.json", scope)
client = gspread.authorize(creds)

# Selecciona la hoja de Google Sheets
spreadsheet = client.open("Datos_Encuentro")
worksheet = spreadsheet.worksheet("DATA")

# Construir el servicio de la API de Google Sheets
sheet_service = build("sheets", "v4", credentials=creds)

# Quitar los filtros de la hoja
clear_filter_request = {"clearBasicFilter": {"sheetId": worksheet.id}}
sheet_service.spreadsheets().batchUpdate(
    spreadsheetId=spreadsheet.id, body={"requests": [clear_filter_request]}
).execute()

# Obtiene los datos de las columnas A (índice 14) y B (índice 15)
column_data_A = worksheet.col_values(14)
column_data_B = worksheet.col_values(15)

# Acumula las celdas que necesitan ser actualizadas
requests = []

# Definir los colores de fondo
colors = {
    "greater": {"red": 0.67, "green": 0.89, "blue": 0.75},
    "equal": {"red": 0.29, "green": 0.78, "blue": 0.52},
    "zero": {"red": 1, "green": 0.61, "blue": 0.53},
    "default": {"red": 1, "green": 1, "blue": 1},
}

# Recorre los datos de las columnas A y B y establece el color de fondo según la condición
for i, (val_A, val_B) in enumerate(zip(column_data_A, column_data_B)):
    try:
        cell_A = float(val_A)
        cell_B = float(val_B)
        if cell_B == 0:
            color = colors["zero"]
        elif cell_A > cell_B:
            color = colors["greater"]
        elif cell_A == cell_B:
            color = colors["equal"]
        else:
            color = colors["default"]

        requests.append(
            {
                "repeatCell": {
                    "range": {
                        "sheetId": worksheet.id,
                        "startRowIndex": i,
                        "endRowIndex": i + 1,
                        "startColumnIndex": 0,
                        "endColumnIndex": 17,
                    },
                    "cell": {"userEnteredFormat": {"backgroundColor": color}},
                    "fields": "userEnteredFormat.backgroundColor",
                }
            }
        )
    except ValueError:
        # Ignorar celdas que no contienen números
        continue

# Si hay celdas que necesitan ser actualizadas, hacer una sola llamada a la API
if requests:
    body = {"requests": requests}
    sheet_service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet.id, body=body
    ).execute()

print("¡Colores actualizados!")
