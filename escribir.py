from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Definir los alcances y la ruta del archivo de credenciales
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
KEY = "key.json"
SPREADSHEET_ID = "1OydEtwNEBl7ZacVRw_fJLkOJQQrgy184VyNJOAq8KpE"

# Autenticarse utilizando las credenciales del servicio
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

# Construir el servicio de la API de Google Sheets
service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# Obtener la fecha y hora actual
hoy = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Definir los valores a insertar en la tabla
values = [
    [
        "V28154135",
        "ANTHONY CÁCERES",
        "MASCULINO",
        None,
        23,
        "SOLTER@",
        "04241519249",
        "APOSENTO ALTO",
        "MATRIMONIO JÓVEN",
        "ESPOSOS DEFITT",
        None,
        "JACKSON DORANTES",
        "ENCUENTRISTA",
        30.0,
        15.0,
        "JDORANTES",
        hoy,
    ],
    [
        "V183291145",
        "JACKSON DORANTES",
        "MASCULINO",
        datetime.strptime("19870806", "%Y%m%d").strftime("%d-%m-%Y"),
        37,
        "CASAD@",
        "04143893828",
        "APOSENTO ALTO",
        "MATRIMONIO JÓVEN",
        "DIOS",
        None,
        None,
        "SERVIDOR",
        25.0,
        25.0,
        "MJGRATEROL",
        hoy,
    ],
    [
        "V15152791",
        "MIRTHA GRATEROL",
        "FEMENINO",
        datetime.strptime("19801122", "%Y%m%d").strftime("%d-%m-%Y"),
        45,
        "CASAD@",
        "04146126353",
        "APOSENTO ALTO",
        "MATRIMONIO JÓVEN",
        "DIOS",
        None,
        None,
        "SERVIDOR",
        25.0,
        20.0,
        "JDORANTES",
        hoy,
    ],
]

# Llamar a la API para insertar los valores
result = (
    sheet.values()
    .append(
        spreadsheetId=SPREADSHEET_ID,
        range="DATA",
        valueInputOption="USER_ENTERED",
        body={"values": values},
    )
    .execute()
)

# Imprimir el resultado de la operación
print(f"Datos insertados correctamente.\n{(result.get('updates').get('updatedCells'))}")
