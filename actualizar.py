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

# Obtiene los datos de las columnas A (índice 0) y B (índice 1)
column_data_A = worksheet.col_values(14)
column_data_B = worksheet.col_values(15)

# Acumula las celdas que necesitan ser actualizadas
requests = []

# Recorre los datos de las columnas A y B y establece el color de fondo amarillo para celdas que cumplan la condición
for i in range(len(column_data_A)):
    try:
        cell_A = float(column_data_A[i])
        cell_B = float(column_data_B[i])
        # Condición: el valor en la columna A debe ser mayor que el valor en la columna B
        if cell_B < cell_A:
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
                        "cell": {
                            "userEnteredFormat": {
                                "backgroundColor": {"red": 1, "green": 1, "blue": 0}
                            }
                        },
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
    sheet_service = build("sheets", "v4", credentials=creds)
    sheet_service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet.id, body=body
    ).execute()

print("¡Colores actualizados!")
