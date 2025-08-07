import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import requests
    import os
    return (os,)


@app.cell
def _(os):
    NOCODB_API_TOKEN = os.environ.get("NOCODB_API_TOKEN")
    NOCODB_API_URL = os.environ.get("NOCODB_API_URL")
    STRAPI_API_TOKEN = os.environ.get("STRAPI_API_TOKEN")
    STRAPI_API_URL = os.environ.get("STRAPI_API_URL")
    return (NOCODB_API_URL,)


@app.cell
def _(NOCODB_API_URL):
    NOCODB_API_URL
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
