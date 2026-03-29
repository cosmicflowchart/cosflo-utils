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
    return NOCODB_API_TOKEN, NOCODB_API_URL


@app.cell
def _():
    NOCODB_TABLE_IDS = {
        "Project Groups": "muaqk7nokq4km2x",
        "Projects": "mjfuyrtmar5m5kt",
    }
    return (NOCODB_TABLE_IDS,)


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
    return (get_nocodb_data,)


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
    return (nocodb_data,)


@app.cell
def _(nocodb_data):
    nocodb_data["Projects"]
    return


@app.cell
def _(nocodb_data):
    products = {}
    for project_group in nocodb_data["Project Groups"]["list"]:
        products[project_group["Title"]] = {
            "Item name": project_group["Title"],
            "Track inventory": "Yes",
            "Category": project_group["Category"],
            "variants": [],
        }
        for project in nocodb_data["Projects"]["list"]:
            if project["Project Group"]["Id"] != project_group["Id"]:
                continue
            products[project_group["Title"]]["variants"].append(
                {
                    "Variations": project["Title"].split(" - ")[-1]
                    if " - " in project["Title"]
                    else project["Title"],
                    "Price": project["Price"],
                    "SKU": project["SKU"],
                    "Quantity": project["initial stock"],
                    "Low stock threshold": 1,
                    "Image 1": "https://nocodb.cosmicflowch.art/"
                    + project["Image"][0]["thumbnails"]["card_cover"][
                        "signedPath"
                    ]
                    if project["Image"]
                    else "",
                }
            )
    return (products,)


@app.cell
def _(products):
    headers = "Item name,Variations,Option set 1,Option 1,Option set 2 ,Option 2,Option set 3,Option 3,Option set 4,Option 4,Is variation visible? (Yes/No),Price,On sale in Online Store?,Regular price (before sale),Tax rate (%),Set up different prices and VAT for takeaway,Takeaway price,Takeaway tax rate,Unit,Track inventory? (Yes/No),Quantity,Low stock threshold,SKU,Barcode,Modifiers,Description (Online Store and Invoices only),Category,Display colour in POS checkout ,Image 1,Image 2,Image 3,Image 4,Image 5,Image 6,Image 7,Display item in Online Store? (Yes/No),SEO title (Online Store only),SEO description (Online Store only),Shipping weight [kg] (Online Store only),Item id (Do not change),Variant id (Do not change)".split(
        ","
    )
    lines = []
    for product in products.values():
        lines.append({k: v for k, v in product.items() if k != "variants"})
        lines.extend(product["variants"])
    return headers, lines


@app.cell
def _(headers, lines):
    output = [",".join(headers)]
    for line in lines:
        output.append(",".join([f"{line.get(header, '')}" for header in headers]))

    with open("sumup_import.csv", "w") as f:
        for line in output:
            f.write(line + "\n")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
