from typing import TypedDict

from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from svglib.svglib import svg2rlg

from .qr_codes import generate_qrcode


class ProductData(TypedDict):
    sku: str
    quantity: int
    title: str
    subtitle: str


def generate_price_tags(
    filename: str,
    products: list[ProductData],
    tagsize=(60 * mm, 20 * mm),
    pagesize=A4,
    margin=10 * mm,
):
    sku = "KC0001"
    url_format = "https://cosmicflowch.art/p/{sku}"

    rows, columns = calculate_column_row_count(tagsize, pagesize, margin)
    pdf_canvas = canvas.Canvas(filename, pagesize=A4)
    pdf_canvas.setTitle("Price Tags")
    add_mesh(pdf_canvas, tagsize, pagesize, margin)
    for n_row in range(0, len(products), columns):
        for n_column, product in enumerate(products[n_row : n_row + columns]):
            x = pagesize[0] / 2 + tagsize[0] * (n_column - columns / 2)
            y = pagesize[1] / 2 - tagsize[1] * (n_row - rows / 2)
            qr = svg2rlg(generate_qrcode(url_format.format(sku=product["sku"])))
            renderPDF.draw(pdf_canvas, qr, x, y)

    pdf_canvas.showPage()
    add_mesh(pdf_canvas, tagsize, pagesize, margin)

    pdf_canvas.save()


def calculate_column_row_count(
    tagsize=(60 * mm, 20 * mm), pagesize=A4, margin=10 * mm
) -> (int, int):
    return (
        int((pagesize[0] - 2 * margin) // tagsize[0]),
        int((pagesize[1] - 2 * margin) // tagsize[1]),
    )


def price_tag_top_left(tagsize=(60 * mm, 20 * mm), page_size=A4, margin=10 * mm):
    return (margin, margin)


def add_mesh(
    pdf_canvas: canvas.Canvas, tagsize=(60 * mm, 20 * mm), pagesize=A4, margin=10 * mm
):
    columns, rows = calculate_column_row_count(tagsize, pagesize, margin)

    pdf_canvas.setLineWidth(0.4)
    box_w, box_h = columns * tagsize[0], rows * tagsize[1]
    box_x, box_y = (pagesize[0] - box_w) / 2, (pagesize[1] - box_h) / 2
    pdf_canvas.rect(box_x, box_y, box_w, box_h)
    for i in range(1, columns):
        pdf_canvas.line(
            box_x + i * tagsize[0], box_y, box_x + i * tagsize[0], box_y + box_h
        )
    for i in range(1, rows):
        pdf_canvas.line(
            box_x, box_y + i * tagsize[1], box_x + box_w, box_y + i * tagsize[1]
        )
