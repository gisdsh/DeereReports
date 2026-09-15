import os
import settings
import hashlib
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlencode
import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colormaps
import numpy as np
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
    df = pd.json_normalize(res.json()["values"])
    return df


def create_table(df_measurements):
    i = 0
    dct = dict()
    defs_list = df_measurements['machineMeasurementDefinition.name'].to_list()
    for mmd in defs_list:
        if 'Engine RPM at Power' in mmd:
            rpm = df_measurements['machineMeasurementDefinition.bucketDefinitions.bucketDefinitions'][i][0]['description']
            idx = str(df_measurements['machineMeasurementDefinition.axesGroup.priority'][i])
            rpm_result_dict = {}
            dct_key = idx + ' - ' + mmd
            def_list = [(d.get('sequenceNumber'), d.get('description')) for d in
                        df_measurements['machineMeasurementDefinition.bucketDefinitions.bucketDefinitions'][i]]
            values_list = [(d.get('sequenceNumber'), d.get('value')) for d in
                           df_measurements['series.intervals'][i][0]['buckets']['buckets']]
            for val in values_list:
                rpm = int(next((second for first, second in def_list if first == val[0]), None))
                rpm_result_dict[rpm] = val[1] / 3600
            rpm_result_dict = dict(sorted(rpm_result_dict.items()))
            # Convert keys to strings
            rpm_result_dict = {str(key): value for key, value in rpm_result_dict.items()}
            dct[dct_key] = rpm_result_dict
        i += 1

    sorted_by_key = dict(sorted(dct.items(), reverse=True))
    sorted_by_key = {key[26:]: value for key, value in sorted_by_key.items()}
    df_load_profile = pd.DataFrame.from_dict(sorted_by_key, orient='index')
    return df_load_profile


def heatmap(df_load_profile, pin, iso_datetime_from, iso_datetime_to):
    col_headers = df_load_profile.columns.tolist()
    row_headers = df_load_profile.index.tolist()
    data = df_load_profile.to_numpy()
    # .tolist()

    fig, ax = plt.subplots(figsize=(12, 6))
    im = ax.imshow(data, cmap=plt.cm.YlGn, aspect='auto')

    # Show all ticks and label them with the respective list entries
    ax.set_xticks(range(len(col_headers)), labels=col_headers,
                  rotation=90, rotation_mode="xtick")
    ax.set_yticks(range(len(row_headers)), labels=row_headers)

    # Loop over data dimensions and create text annotations.
    for i in range(len(row_headers)):
        for j in range(len(col_headers)):
            if data[i, j] > 0:
                num = round(data[i, j], 2)
                text = ax.text(j, i, num,
                               ha="center", va="center", color="black",
                               fontsize=10, wrap=True)

    ax.set_title(f"Perfil de carga - {pin} - desde {iso_datetime_from} hasta {iso_datetime_to}")
    fig.tight_layout()
    plt.show()

    # df_load_profile.to_csv('load_profile_table.csv', index=True)
    # df_load_profile.to_json("kk.json", indent=2)


def process_machine_measurements(window):
    pin = window.edtSerie.text()    # '1BM8270RKPS101195'
    columns = list(zip(*settings.MACHINES))
    position = columns[2].index(pin)
    principal_id = columns[1][position]
    datetime_from = window.dteInicio.dateTime()  # PySide6.QtCore.QDateTime(2026, 8, 1, 0, 0, 0, 0, 0) → convert to ISO: '2026-08-01T00:00:00.000Z'
    datetime_to = window.dteFin.dateTime()       # PySide6.QtCore.QDateTime(2026, 8, 31, 23, 59, 0, 0, 0) → convert to ISO: '2026-08-31T23:59:59.999'
    iso_datetime_from = qdatetime2iso(datetime_from)
    iso_datetime_to = qdatetime2iso(datetime_to)
    offset = settings.UTC_OFFSET
    df_measurements = get_machine_measurements(settings.TOKENS, principal_id, iso_datetime_from, iso_datetime_to, offset)
    if 'Engine RPM at Power 0 to 10' in df_measurements['machineMeasurementDefinition.name'].to_list():
        df_load_profile = create_table(df_measurements)
        heatmap(df_load_profile, pin, iso_datetime_from, iso_datetime_to)
        print(df_load_profile.to_string())
    else:
        print("No hay datos de perfil de carga para esta unidad")


'''
1BM8295RCRS100610
1BM8345RVRS101337
1RW8320RJGP112097
1J07230CHR3000159
1BM8250RTRS000047
1BM8320RVRS100913
1BM8295RJSS100630
1J07200CCR3000180
1BM8270RCRS101339
1J07230CKR3000282
1RW8270RVAP009515
1BM8345RCHS100007
1BM8270RPSS101494
1BM8320RLSS100970
1J07230CHR3000288
1BM8370RESS100998
1BM8295RPJ0100070
1RW8335RTDP082699
1BM8345RTSS101403
1J07230CLR3000256
1RW8295RAAP005423
1RW8335RJCP057255
1RW8345RJGS115650
1BM8270RCKS100415
1RW7230STLC110497
1RW8335RKCP055701
1BM8270RKPS101195
1RW8335RCCP055659
1RW8335RCCP055659
1BM8345RVHS100008
1RW8270RHGP112608
1BM8250RHSS000194
1BM8270RKJ0100177
1J07230CTR3000201
'''


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


if __name__ == "__main__":
    pass
    # refreshed_tokens = refresh_token(secrets, tokens["refresh_token"])
    # print(f"Refreshed tokens: {refreshed_tokens}")

