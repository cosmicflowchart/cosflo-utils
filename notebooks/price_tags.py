import marimo

__generated_with = "0.14.10"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    from datetime import datetime

    return (datetime,)


@app.cell
def _():
    from generators import generate_price_tags

    return (generate_price_tags,)


@app.cell
def _():
    products = [
        {
            "sku": "AC0013",
            "title": "Lesbian Pride/Black",
            "subtitle": "Bottle Holder",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "AC0014",
            "title": "Lesbian Pride/White",
            "subtitle": "Bottle Holder",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "KC0101",
            "title": "Blue",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 6,
        },
        {
            "sku": "KC0102",
            "title": "Purple",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 2,
        },
        {
            "sku": "KC0111",
            "title": "Rainbow",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 6,
        },
        {
            "sku": "KC0112",
            "title": "Bi Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 6,
        },
        {
            "sku": "KC0113",
            "title": "Trans Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 6,
        },
        {
            "sku": "KC0114",
            "title": "Pan Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "KC0115",
            "title": "NB Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "KC0116",
            "title": "Ace Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "KC0117",
            "title": "Lesbian Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 6,
        },
        {
            "sku": "DB0202",
            "title": "Interstellar",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0204",
            "title": "Vega",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0205",
            "title": "Outer Space",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0206",
            "title": "Stella Polaris",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0207",
            "title": "Supercluster",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0208",
            "title": "Galactic",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
    ]
    return (products,)


@app.cell
def _(products):
    print(sum([p["quantity"] for p in products]))
    return


@app.cell
def _(datetime):
    datetime.now().date().isoformat()
    return


@app.cell
def _(datetime, generate_price_tags, products):
    now = datetime.now()
    generate_price_tags(f"price-tags-{now:%Y-%m-%d}.pdf", products)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
