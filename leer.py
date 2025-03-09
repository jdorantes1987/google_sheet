from googleapiclient.discovery import build
from google.oauth2 import service_account
from pandas import DataFrame

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
KEY = "key.json"
# Escribe aquí el ID de tu documento:
SPREADSHEET_ID = "1OydEtwNEBl7ZacVRw_fJLkOJQQrgy184VyNJOAq8KpE"

creds = None
creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

# Llamada a la api
result = (
    sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="ENCUENTRISTAS").execute()
)
# Extraemos values del resultado en un dataframe de pandas
values = result.get("values", [])
df = DataFrame(values[1:], columns=values[0])
print(df)
