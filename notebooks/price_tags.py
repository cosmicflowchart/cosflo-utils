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
            "sku": "AC0001",
            "title": "Rainbow/Black",
            "subtitle": "Bottle Holder",
            "price": 250,
            "quantity": 4,
        },
        {
            "sku": "AC003",
            "title": "Bi Pride/Black",
            "subtitle": "Bottle Holder",
            "price": 250,
            "quantity": 4,
        },
        {
            "sku": "KC0113",
            "title": "Trans Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 6,
        },
        {
            "sku": "KC0116",
            "title": "Ace Pride",
            "subtitle": "Octopus Keychain",
            "price": 100,
            "quantity": 6,
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
            "quantity": 6,
        },
        {
            "sku": "DB0209",
            "title": "Andromeda",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0210",
            "title": "Space Walk",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0211",
            "title": "Moon Phase",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 4,
        },
        {
            "sku": "DB0212",
            "title": "Orbit",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0213",
            "title": "Supernova",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0214",
            "title": "Luna",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0215",
            "title": "Sun Halo",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0216",
            "title": "Pollux",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 2,
        },
        {
            "sku": "DB0217",
            "title": "Intergalactic Monster",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 4,
        },
        {
            "sku": "DB0218",
            "title": "Dark Matter",
            "subtitle": "Dragonscale Dice Bag",
            "price": 250,
            "quantity": 4,
        },
        {
            "sku": "DB0219",
            "title": "Zombie Planet",
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
def _(datetime, generate_price_tags, products):
    now = datetime.now()
    generate_price_tags(f"price-tags-{now:%Y-%m-%d}.pdf", products)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
