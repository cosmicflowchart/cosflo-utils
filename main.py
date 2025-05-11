import typer
from typing_extensions import Annotated

from generators import ProductData, generate_price_tags

app = typer.Typer()


@app.command()
def price_tags(
    input_file: str,
    output_file: Annotated[str, typer.Option("--output", "-o")] = "price_tags.pdf",
):
    with open(input_file) as f:
        lines = [line.split(",") for line in f]
        products: list[ProductData] = []
        for line in lines[1:]:
            if len(line) < 5 or not line[0]:
                continue
            products.append(
                {
                    "sku": line[0],
                    "title": line[3],
                    "subtitle": line[2],
                    "price": int(line[4]),
                    "quantity": int(line[5]),
                }
            )

    generate_price_tags(output_file, products)


if __name__ == "__main__":
    app()
