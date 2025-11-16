import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests
    import os
    return os, requests


@app.cell
def _(os):
    NOCODB_API_TOKEN = os.environ.get("NOCODB_API_TOKEN")
    NOCODB_API_URL = os.environ.get("NOCODB_API_URL")
    STRAPI_API_TOKEN = os.environ.get("STRAPI_API_TOKEN")
    STRAPI_API_URL = os.environ.get("STRAPI_API_URL")
    return NOCODB_API_TOKEN, NOCODB_API_URL, STRAPI_API_TOKEN, STRAPI_API_URL


@app.cell
def _():
    NOCODB_TABLE_IDS = {
        "Project Groups": "muaqk7nokq4km2x",
        "Projects": "mjfuyrtmar5m5kt",
    }
    STRAPI_ENDPOINTS = ["projects"]
    return NOCODB_TABLE_IDS, STRAPI_ENDPOINTS


@app.cell
def _(
    NOCODB_API_TOKEN,
    NOCODB_API_URL,
    NOCODB_TABLE_IDS,
    STRAPI_API_TOKEN,
    STRAPI_API_URL,
    requests,
):
    def get_nocodb_data(table_name: str, params: dict[str, str] = None) -> dict:
        headers = {
            "xc-token": NOCODB_API_TOKEN,
            "Content-Type": "application/json",
        }
        url = f"{NOCODB_API_URL}/api/v2/tables/{NOCODB_TABLE_IDS[table_name]}/records"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


    def get_strapi_data(endpoint: str, params: dict[str, str] = None) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {STRAPI_API_TOKEN}",
        }
        url = f"{STRAPI_API_URL}/api/{endpoint}"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    return get_nocodb_data, get_strapi_data


@app.cell
def _(NOCODB_TABLE_IDS, get_nocodb_data):
    nocodb_data = {
        table_name: get_nocodb_data(table_name, params={"limit": 1000})
        for table_name in NOCODB_TABLE_IDS.keys()
    }
    for table_name, table_data in nocodb_data.items():
        print(
            f"{table_name} data fetched successfully with {len(table_data['list'])} records."
        )
    return


@app.cell
def _(STRAPI_ENDPOINTS, get_strapi_data):
    strapi_data = {
        endpoint: get_strapi_data(
            endpoint,
            params={
                "populate": "*",
                "pagination[pageSize]": 100,
                "status": "draft",
            },
        )
        for endpoint in STRAPI_ENDPOINTS
    }
    for endpoint, endpoint_data in strapi_data.items():
        print(
            f"{endpoint} data fetched successfully with {len(endpoint_data['data'])} records."
        )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
