from io import BytesIO
from typing import TypedDict

from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

from .qr_codes import generate_qrcode


class PageParameters(TypedDict):
    box_h: float
    box_w: float
    box_x: float
    box_y: float
    columns: int
    rows: int


class ProductData(TypedDict):
    sku: str
    quantity: int
    title: str
    subtitle: str
    price: int


def generate_price_tags(
    filename: str,
    products: list[ProductData],
    tagsize=(30 * mm, 50 * mm),
    pagesize=A4,
    margin=10 * mm,
    padding=2 * mm,
):
    for fontname, fontfile in [
        ("Exo 2.0 Regular", "Exo2.0-Regular.ttf"),
        ("Exo 2.0 Medium", "Exo2.0-Medium.ttf"),
        ("Exo 2.0 Bold", "Exo2.0-Bold.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(fontname, f"assets/fonts/{fontfile}"))

    tag_data = [product for product in products for _ in range(product["quantity"])]
    url_format = "cosmicflowch.art/p/{sku}"
    url_format_qr = "https://cosmicflowch.art/p/{sku}"

    logo_drawing = svg2rlg("assets/logo/cfc-logo-grey.svg")
    logo_scale = (tagsize[0] - 2 * padding) / logo_drawing.width
    logo_drawing.scale(sx=logo_scale, sy=logo_scale)

    parameters = calculate_page_parameters(
        tagsize=tagsize, pagesize=pagesize, margin=margin
    )
    rows, columns = parameters["rows"], parameters["columns"]
    pages = len(tag_data) // (rows * columns) + 1
    pdf_canvas = canvas.Canvas(filename, pagesize=A4)
    pdf_canvas.setTitle("Price Tags")
    for n_page in range(pages):
        page_data = tag_data[n_page * rows * columns : (n_page + 1) * rows * columns]

        add_mesh(pdf_canvas, parameters, tagsize=tagsize)
        for n_row in range(rows):
            for n_column, product in enumerate(
                page_data[n_row * columns : (n_row + 1) * columns]
            ):
                x = parameters["box_x"] + tagsize[0] * n_column
                y = parameters["box_y"] + parameters["box_h"] - tagsize[1] * n_row

                pdf_canvas.circle(x + tagsize[0] / 2, y - 5 * mm, 2.5 * mm)

                renderPDF.draw(
                    logo_drawing,
                    pdf_canvas,
                    x + padding,
                    y - 30 * mm,
                )

                pdf_canvas.setFont("Exo 2.0 Bold", 12)
                pdf_canvas.drawCentredString(
                    x + tagsize[0] / 2,
                    y - 38 * mm,
                    product["title"],
                )

                pdf_canvas.setFont("Exo 2.0 Medium", 8)
                lines = simpleSplit(
                    product["subtitle"], "Exo 2.0 Medium", 8, tagsize[0] - 2 * padding
                )
                for k, line in enumerate(lines):
                    pdf_canvas.drawCentredString(
                        x + tagsize[0] / 2,
                        y - 43 * mm - k * 3 * mm,
                        line,
                    )

        pdf_canvas.showPage()
        add_mesh(pdf_canvas, parameters, tagsize=tagsize)

        for n_row in range(rows):
            for n_column, product in enumerate(
                page_data[n_row * columns : (n_row + 1) * columns]
            ):
                x = parameters["box_x"] + tagsize[0] * (columns - n_column - 1)
                y = parameters["box_y"] + parameters["box_h"] - tagsize[1] * n_row

                pdf_canvas.circle(x + tagsize[0] / 2, y - 5 * mm, 2.5 * mm)

                pdf_canvas.setFont("Exo 2.0 Bold", 8)
                pdf_canvas.drawCentredString(
                    x + tagsize[0] / 2,
                    y - 13 * mm,
                    "Scan for more info",
                )

                qr = BytesIO()
                generate_qrcode(qr, url_format_qr.format(sku=product["sku"].lower()))
                qr.seek(0)
                qr_drawing = svg2rlg(qr)
                qr_scale = (tagsize[0] - 2 * padding) / qr_drawing.width
                qr_drawing.scale(sx=qr_scale, sy=qr_scale)
                renderPDF.draw(
                    qr_drawing,
                    pdf_canvas,
                    x + padding,
                    y - qr_drawing.height * qr_scale - 14 * mm,
                )
                pdf_canvas.setFont("Exo 2.0 Regular", 5)
                pdf_canvas.drawCentredString(
                    x + tagsize[0] / 2,
                    y - qr_drawing.height * qr_scale - 16 * mm,
                    url_format.format(sku=product["sku"].lower()),
                )

                pdf_canvas.setFont("Exo 2.0 Bold", 12)
                pdf_canvas.drawCentredString(
                    x + tagsize[0] / 2,
                    y - 48 * mm,
                    f"{product["price"]} kr",
                )

        if n_page < pages - 1:
            pdf_canvas.showPage()

    pdf_canvas.save()


def calculate_page_parameters(
    tagsize=(60 * mm, 20 * mm), pagesize=A4, margin=10 * mm
) -> (int, int):
    parameters = {
        "columns": int((pagesize[0] - 2 * margin) // tagsize[0]),
        "rows": int((pagesize[1] - 2 * margin) // tagsize[1]),
    }

    parameters["box_w"] = parameters["columns"] * tagsize[0]
    parameters["box_h"] = parameters["rows"] * tagsize[1]
    parameters["box_x"] = (pagesize[0] - parameters["box_w"]) / 2
    parameters["box_y"] = (pagesize[1] - parameters["box_h"]) / 2

    return parameters


def add_mesh(
    pdf_canvas: canvas.Canvas,
    parameters: PageParameters,
    tagsize=(30 * mm, 50 * mm),
):
    pdf_canvas.setLineWidth(0.4)
    pdf_canvas.rect(
        parameters["box_x"],
        parameters["box_y"],
        parameters["box_w"],
        parameters["box_h"],
    )
    for i in range(1, parameters["columns"]):
        pdf_canvas.line(
            parameters["box_x"] + i * tagsize[0],
            parameters["box_y"],
            parameters["box_x"] + i * tagsize[0],
            parameters["box_y"] + parameters["box_h"],
        )
    for i in range(1, parameters["rows"]):
        pdf_canvas.line(
            parameters["box_x"],
            parameters["box_y"] + i * tagsize[1],
            parameters["box_x"] + parameters["box_w"],
            parameters["box_y"] + i * tagsize[1],
        )
