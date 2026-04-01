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
            "sku": "KC0113",
            "title": "Trans Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 10,
        },
        {
            "sku": "KC0117",
            "title": "Lesbian Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 10,
        },
        {
            "sku": "KC0115",
            "title": "Non-Binary Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 10,
        },
        {
            "sku": "KC0101",
            "title": "Blue",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 5,
        },
        {
            "sku": "KC0102",
            "title": "Purple",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 5,
        },
        {
            "sku": "KC0103",
            "title": "Orange",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 5,
        },
        {
            "sku": "KC0111",
            "title": "Rainbow",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 5,
        },
        {
            "sku": "KC0112",
            "title": "Bi Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 5,
        },
        {
            "sku": "KC0114",
            "title": "Pan Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 5,
        },
        {
            "sku": "AC0011",
            "title": "Asexual Pride/Black",
            "subtitle": "Bottle Holder",
            "price": 250,
            "quantity": 3,
        },
        {
            "sku": "AC0012",
            "title": "Asexual Pride/White",
            "subtitle": "Bottle Holder",
            "price": 250,
            "quantity": 3,
        },
        {
            "sku": "KC001",
            "title": "Alien",
            "subtitle": "Keychain",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "KC0002",
            "title": "Cthulhu",
            "subtitle": "Keychain",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "KC0004",
            "title": "Mindflayer",
            "subtitle": "Keychain",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "BM0015",
            "title": "Calico",
            "subtitle": "Cat Bookmark",
            "price": 100,
            "quantity": 5,
        },
        {
            "sku": "BM0017",
            "title": "Soot",
            "subtitle": "Cat Bookmark",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "BM0016",
            "title": "Dusty",
            "subtitle": "Cat Bookmark",
            "price": 100,
            "quantity": 3,
        },
        {
            "sku": "BM0014",
            "title": "Tux",
            "subtitle": "Cat Bookmark",
            "price": 100,
            "quantity": 4,
        },
        {
            "sku": "BM0013",
            "title": "Ginger",
            "subtitle": "Cat Bookmark",
            "price": 100,
            "quantity": 3,
        },
        {
            "sku": "BM0011",
            "title": "Void",
            "subtitle": "Cat Bookmark",
            "price": 100,
            "quantity": 3,
        },
        {
            "sku": "DB1001",
            "title": "Prismatic/Black",
            "subtitle": "Segmented Dice\u00a0Bag",
            "price": 600,
            "quantity": 4,
        },
        {
            "sku": "DB1002",
            "title": "Prismatic/White",
            "subtitle": "Segmented Dice\u00a0Bag",
            "price": 600,
            "quantity": 4,
        },
        {
            "sku": "DB1101",
            "title": "Planned Pooling Orange/Purple/White",
            "subtitle": "Segmented Dice\u00a0Bag",
            "price": 600,
            "quantity": 4,
        },
        {
            "sku": "DB1102",
            "title": "Planned Pooling Orange/Green",
            "subtitle": "Segmented Dice\u00a0Bag",
            "price": 600,
            "quantity": 4,
        },
        {
            "sku": "DB1103",
            "title": "Planned Pooling Orange/Purple",
            "subtitle": "Segmented Dice\u00a0Bag",
            "price": 600,
            "quantity": 4,
        },
    ]
    return (products,)


@app.cell
def _(products):
    print(sum([p["quantity"] for p in products]))
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
