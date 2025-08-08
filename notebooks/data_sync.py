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
        "Materials": "mh47vbxv0dwtz3b",
        "Material Variants": "mq1fefdad9129q0",
        "Project Materials": "mtnll2g9qzlj0e0",
    }
    STRAPI_ENDPOINTS = ["projects", "material-groups", "material-variants"]
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


    def create_strapi_document(endpoint: str, data: dict) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {STRAPI_API_TOKEN}",
        }
        url = f"{STRAPI_API_URL}/api/{endpoint}"
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()


    def update_strapi_document(
        endpoint: str, document_id: int, data: dict
    ) -> dict:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {STRAPI_API_TOKEN}",
        }
        url = f"{STRAPI_API_URL}/api/{endpoint}/{document_id}"
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    return (
        create_strapi_document,
        get_nocodb_data,
        get_strapi_data,
        update_strapi_document,
    )


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
    return (strapi_data,)


@app.cell
def _(create_strapi_document, nocodb_data):
    strapi_material_groups_document_ids = {}
    for material in nocodb_data["Materials"]["list"]:
        created_material_group = create_strapi_document(
            "material-groups",
            {
                "data": {
                    "brand": material["Brand"],
                    "name": material["Title"],
                    "type": "Yarn",
                    "yardage": f"{material['Length (m)']} m / {material['Weight (g)']} g",
                    "composition": material["Composition"],
                }
            },
        )
        strapi_material_groups_document_ids[material["Id"]] = (
            created_material_group["data"]["documentId"]
        )
    return (strapi_material_groups_document_ids,)


@app.cell
def _(
    create_strapi_document,
    nocodb_data,
    strapi_material_groups_document_ids,
):
    strapi_material_variants_document_ids = {}
    for material_variant in nocodb_data["Material Variants"]["list"]:
        created_material_variant = create_strapi_document(
            "material-variants",
            {
                "data": {
                    "name": material_variant["Name"],
                    "manufacturerNumber": material_variant["Manufacturer Number"],
                    "materialGroup": strapi_material_groups_document_ids[
                        material_variant["Materials_id"]
                    ],
                }
            },
        )
        strapi_material_variants_document_ids[material_variant["Id"]] = (
            created_material_variant["data"]["documentId"]
        )
    return (strapi_material_variants_document_ids,)


@app.cell
def _(nocodb_data, strapi_data):
    nocodb_project_ids_by_sku = {
        project["SKU"]: project["Id"]
        for project in nocodb_data["Projects"]["list"]
    }
    strapi_project_document_ids_sku = {
        project["sku"]: project["documentId"]
        for project in strapi_data["projects"]["data"]
    }
    nocodb_project_ids_to_strapi = {
        nocodb_id: strapi_project_document_ids_sku[sku]
        for sku, nocodb_id in nocodb_project_ids_by_sku.items()
        if sku in strapi_project_document_ids_sku
    }
    print(
        len(nocodb_project_ids_by_sku),
        len(strapi_project_document_ids_sku),
        len(nocodb_project_ids_to_strapi),
    )
    return (nocodb_project_ids_to_strapi,)


@app.cell
def _(nocodb_data, strapi_material_variants_document_ids):
    project_materials = {}
    for project_material in nocodb_data["Project Materials"]["list"]:
        project_id = project_material["Projects_id"]
        if project_id not in project_materials:
            project_materials[project_id] = {}
        if project_material["Status"] == "Main":
            key = "primary"
        else:
            key = "secondary"

        if key not in project_materials[project_id]:
            project_materials[project_id][key] = []
        project_materials[project_id][key].append(
            {
                "materialVariant": strapi_material_variants_document_ids[
                    project_material["Material Variants_id"]
                ],
                "quantity": project_material["Quantity"],
                "amountGrams": project_material["Amount (g)"],
            }
        )
    return (project_materials,)


@app.cell
def _(nocodb_data, nocodb_project_ids_to_strapi, project_materials):
    strapi_project_updates = {}
    for project in nocodb_data["Projects"]["list"]:
        strapi_project_id = nocodb_project_ids_to_strapi.get(project["Id"])
        if not strapi_project_id:
            continue

        strapi_project_updates[strapi_project_id] = {
            "data": {
                "title": project["Title"],
                "sku": project["SKU"],
                "primaryMaterial": project_materials.get(project["Id"], {}).get(
                    "primary", []
                ),
                "secondaryMaterial": project_materials.get(project["Id"], {}).get(
                    "secondary", []
                ),
            }
        }
    return (strapi_project_updates,)


@app.cell
def _(strapi_project_updates, update_strapi_document):
    for document_id, project_update_data in strapi_project_updates.items():
        updated_document = update_strapi_document(
            "projects", document_id, project_update_data
        )
        print(
            f"Updated project {document_id} with primary and secondary materials."
        )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
