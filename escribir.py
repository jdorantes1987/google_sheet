from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
KEY = "key.json"
SPREADSHEET_ID = "1OydEtwNEBl7ZacVRw_fJLkOJQQrgy184VyNJOAq8KpE"

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# Debe ser una matriz por eso el doble [[]]
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
    ],
    [
        "V183291145",
        "JACKSON DORANTES",
        "MASCULINO",
        datetime.strptime("19870806", "%Y%m%d").strftime("%m-%d-%Y"),
        37,
        "CASAD@",
        "04143893828",
        "APOSENTO ALTO",
        "MATRIMONIO JÓVEN",
        "DIOS",
        None,
        None,
        "SERVIDOR",
    ],
    [
        "V15152791",
        "MIRTHA GRATEROL",
        "FEMENINO",
        datetime.strptime("19801122", "%Y%m%d").strftime("%m-%d-%Y"),
        45,
        "CASAD@",
        "04146126353",
        "APOSENTO ALTO",
        "MATRIMONIO JÓVEN",
        "DIOS",
        None,
        None,
        "SERVIDOR",
    ],
]
# Llamamos a la api
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
print(f"Datos insertados correctamente.\n{(result.get('updates').get('updatedCells'))}")
