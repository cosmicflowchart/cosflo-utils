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
    from generators import generate_backing_cards
    return (generate_backing_cards,)


@app.cell
def _():
    products = [
        {"sku": "AC0118", "title": "Genderqueer", "subtitle": "Flower Pin", "price": 100, "quantity": 4},
        {"sku": "AC0118", "title": "Genderqueer", "subtitle": "Flower Pin with\u00A0Pronouns", "price": 120, "quantity": 2},
        {"sku": "AC0111", "title": "Rainbow", "subtitle": "Flower Pin", "price": 100, "quantity": 1},
        {"sku": "AC0111", "title": "Rainbow", "subtitle": "Flower Pin with\u00A0Pronouns", "price": 120, "quantity": 1},
        {"sku": "AC0113", "title": "Trans Pride", "subtitle": "Flower Pin with\u00A0Pronouns", "price": 120, "quantity": 1},
    ]
    return (products,)


@app.cell
def _(products):
    print(sum([p["quantity"] for p in products]))
    return


@app.cell
def _(datetime, generate_backing_cards, products):
    now = datetime.now()
    generate_backing_cards(f"backing-cards-{now:%Y-%m-%d}.pdf", products)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
