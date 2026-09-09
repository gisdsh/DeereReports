import os
import settings
import hashlib
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlencode
import requests
import pandas as pd
from pathlib import Path
from html.parser import HTMLParser

settings.SCOPES = ["ag1", "ag2", "ag3", "eq1", "eq2", "org1", "org2", "files", "offline_access"]
settings.HOST = "localhost"
settings.PORT = 9090
settings.UTC_OFFSET = "-03:00"


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.server: "Server"
        self.server.query_params = dict(parse_qsl(self.path.split("?")[1]))
        self.wfile.write(b"<h1>Authorised! You may now close this tab</h1>")


class Server(HTTPServer):
    def __init__(self, host: str, port: int) -> None:
        super().__init__((host, port), RequestHandler)
        self.query_params: dict[str, str] = {}


def authorise(secrets: dict[str, str]) -> dict[str, str]:
    redirect_uri = f"{secrets['redirect_uris'][0]}:{settings.PORT}/callback"

    params = {
        "response_type": "code",
        "client_id": secrets["client_id"],
        "redirect_uri": redirect_uri,
        "scope": " ".join(settings.SCOPES),
        "state": hashlib.sha256(os.urandom(1024)).hexdigest(),
    }
        # "access_type": "offline",
    url = f"{secrets['auth_uri']}?{urlencode(params)}"
    if not webbrowser.open(url):
        raise RuntimeError("Failed to open browser")

    server = Server(settings.HOST, settings.PORT)
    try:
        server.handle_request()
    finally:
        server.server_close()

    if params["state"] != server.query_params["state"]:
        raise RuntimeError("Invalid state")

    code = server.query_params["code"]

    params = {
        "grant_type": "authorization_code",
        "client_id": secrets["client_id"],
        "client_secret": secrets["client_secret"],
        "redirect_uri": redirect_uri,
        "code": code,
    }
    with requests.post(
        secrets["token_uri"],
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ) as response:
        if response.status_code != 200:
            raise RuntimeError("Failed to authorise")

        return response.json()


def refresh_token(secrets_: dict[str, str], refresh_token_: str) -> dict[str, str]:
    params = {
        "grant_type": "refresh_token",
        "client_id": secrets_["client_id"],
        "client_secret": secrets_["client_secret"],
        "refresh_token": refresh_token_,
    }
    with requests.post(
        secrets_["token_uri"],
        data=params,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    ) as response:
        if response.status_code != 200:
            raise RuntimeError("Failed to refresh token")

        return response.json()


def api_get(access_token, resource_url):
    headers = {
        'authorization': 'Bearer ' + access_token,
        'Accept': 'application/vnd.deere.axiom.v3+json',
        'Accept-Language': 'es',
        'x-deere-no-paging': 'true',
    }
    return requests.get(resource_url, headers=headers)


def get_tokens() -> dict:
    secrets = {
    "client_id": "0oakx4g6yjiXGPK5c5d7",
    "client_secret": "2v3NrRR924Yj6dnftvjMhr7Q79wM2tIUB4whG-EkHToDs-rvntAvDzlUMrEj0ypp",
    "auth_uri": "https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/authorize",
    "token_uri": "https://signin.johndeere.com/oauth2/aus78tnlaysMraFhC1t7/v1/token",
    "redirect_uris": ["http://localhost"]
    }
    return authorise(secrets)


def get_organizations(tokens) -> list:
    url = f"https://sandboxapi.deere.com/platform/organizations"
    res = api_get(tokens['access_token'], url)
    dfOrg = pd.json_normalize(res.json()["values"])
    orgsList = dfOrg[['id', 'name']].values.tolist()
    return orgsList


def get_machines(tokens) -> list:
    url = f"https://equipmentapi.deere.com/isg/equipment?itemLimit=5000&categories=machine"
    res = api_get(tokens['access_token'], url)
    machines = res.json()["values"]
    dfMach = pd.json_normalize(machines)
    dfMach.sort_values(by='id', key=lambda x: x.astype(int), ascending=False)
    machinesList = dfMach[['id', 'principalId', 'serialNumber', 'name', 'organization.id']].values.tolist()
    machinesList.sort(key=lambda x: int(x[1]), reverse=True)
    return machinesList


def get_machine_measurements(tokens, principal_id, datetime_from, datetime_to, offset) -> pd.DataFrame:
    url = (f"https://api.deere.com/platform/machines/{principal_id}/machineMeasurements?"
           f"embed=measurementDefinition&startDate={datetime_from}&endDate={datetime_to}"
           f"&interval=aggregated&aggregationUTCOffset={offset}&itemLimit=5000&x-deere-no-paging=true")
    res = api_get(tokens['access_token'], url)
    dfMeas = pd.json_normalize(res.json()["values"])


def process_machine_measurements(window):

    principal_id = window.edtSerie.text()    # '1BM8270RKPS101195'
    datetime_from = window.dteInicio.dateTime()  # PySide6.QtCore.QDateTime(2026, 8, 1, 0, 0, 0, 0, 0) → convert to ISO: '2026-08-01T00:00:00.000Z'
    datetime_to = window.dteFin.dateTime()       # PySide6.QtCore.QDateTime(2026, 8, 31, 23, 59, 0, 0, 0) → convert to ISO: '2026-08-31T23:59:59.999'
    iso_datetime_from = qdatetime2iso(datetime_from)
    iso_datetime_ti = qdatetime2iso(datetime_to)
    offset = settings.UTC_OFFSET
    url = get_machine_measurements(settings.TOKENS, principal_id, iso_datetime_from, iso_datetime_ti, offset)
    pass


def qdatetime2iso(qdt):
    YY = str(qdt.date().year())
    MM = str(qdt.date().month()).zfill(2)
    DD = str(qdt.date().day()).zfill(2)
    hh = str(qdt.time().hour()).zfill(2)
    mm = str(qdt.time().minute()).zfill(2)
    if mm == "59":
        ss = "59.999"
    else:
        ss = "00.000"
    return f"{YY}-{MM}-{DD}T{hh}:{mm}:{ss}Z"


# def process_machine_measurements():
#     principal_id = '1BM8270RKPS101195'
#     datetime_from = '1/8/2026 00:00'
#     datetime_to = '31/8/2026 23:59'
#     offset = UTC_OFFSET

if __name__ == "__main__":
    pass
    # process_machine_measurements()
    # refreshed_tokens = refresh_token(secrets, tokens["refresh_token"])
    # print(f"Refreshed tokens: {refreshed_tokens}")

