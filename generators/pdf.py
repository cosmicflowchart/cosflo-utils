from io import BytesIO
from typing import TypedDict

from pypdf import PdfReader, PdfWriter
from qrcode import ERROR_CORRECT_H, ERROR_CORRECT_L
from reportlab.graphics import renderPDF
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
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


def find_max_fontsize(
    text: str, fontname: str, line_width: float, starting_fontsize: int = 12
) -> int:
    """Finds the maximum fontsize that can be used to fit the given
    text in the given line width.

    Arguments:
        text: The string to be split into lines.
        fontname: The name of the font.
        line_width: The max width of each line.
        starting_fontsize: The initial fontsize.

    Returns:
        The max fontsize.
    """
    text_width = pdfmetrics.stringWidth(text, fontname, starting_fontsize)
    if text_width <= line_width:
        return starting_fontsize
    return starting_fontsize // (text_width / line_width)


def line_wrap_text(
    text: str, fontname: str, fontsize: int, line_width: float
) -> list[str]:
    """Line wraps a string to lines of a give width. This reimplements
    reportlab's simpleSplit function, which unfortunately does not
    respect non-breaking spaces.

    Argument:
        text: The string to be split into lines.
        fontname: The name of the font.
        fontsize: The size of the font.
        line_width: The max width of each line.

    Returns:
        A list of strings representing individual lines.
    """
    lines = [""]

    # Only split by regular space, not by non-breaking space. (This
    # assumes the text contains no other whitespace characters like
    # tabs or en-spaces.)
    for word in text.split(" "):
        if lines[-1] == "":
            lines[-1] = word
        elif (
            pdfmetrics.stringWidth(f"{lines[-1]} {word}", fontname, fontsize)
            <= line_width
        ):
            lines[-1] = f"{lines[-1]} {word}"
        else:
            lines.append(word)

    return lines


def generate_backing_cards(
    filename: str,
    products: list[ProductData],
    pagesize=A4,
    padding=4 * mm,
    text_color="#e5ccff",
):
    for fontname, fontfile in [
        ("Exo 2.0 Regular", "Exo2.0-Regular.ttf"),
        ("Exo 2.0 Medium", "Exo2.0-Medium.ttf"),
        ("Exo 2.0 Bold", "Exo2.0-Bold.ttf"),
    ]:
        pdfmetrics.registerFont(TTFont(fontname, f"assets/fonts/{fontfile}"))

    data = [product for product in products for _ in range(product["quantity"])]
    url_format = "cosmicflowch.art/p/{sku}"
    url_format_qr = "https://cosmicflowch.art/p/{sku}"

    x0, y0 = 23.5 * mm, pagesize[1] - 19 * mm
    width, height = 53 * mm, 85 * mm
    gap = 2 * mm

    rows, columns = 3, 3
    pages = len(data) // (rows * columns) + 1
    pdf_canvas = canvas.Canvas(filename, pagesize=A4)
    pdf_canvas.setTitle("Backing Cards")
    text_color_rgb = tuple(int(text_color[i : i + 2], 16) / 255 for i in (1, 3, 5))

    for n_page in range(pages):
        page_data = data[n_page * rows * columns : (n_page + 1) * rows * columns]
        if len(page_data) == 0:
            break

        pdf_canvas.setFillColorRGB(*text_color_rgb)
        for n_row in range(rows):
            for n_column, product in enumerate(
                page_data[n_row * columns : (n_row + 1) * columns]
            ):
                x = x0 + (width + gap) * n_column
                y = y0 - (height + gap) * n_row

                pdf_canvas.setFont(
                    "Exo 2.0 Bold",
                    find_max_fontsize(
                        product["title"],
                        "Exo 2.0 Bold",
                        width - 2 * padding,
                        starting_fontsize=20,
                    ),
                )
                pdf_canvas.drawCentredString(
                    x + width / 2,
                    y - 10 * mm,
                    product["title"],
                )

                pdf_canvas.setFont("Exo 2.0 Medium", 12)
                lines = line_wrap_text(
                    product["subtitle"], "Exo 2.0 Medium", 12, width - 2 * padding
                )
                for k, line in enumerate(lines):
                    pdf_canvas.drawCentredString(
                        x + width / 2,
                        y - 15 * mm - k * 4 * mm,
                        line,
                    )

        pdf_canvas.showPage()

        pdf_canvas.setFillColorRGB(*text_color_rgb)
        for n_row in range(rows):
            for n_column, product in enumerate(
                page_data[n_row * columns : (n_row + 1) * columns]
            ):
                x = x0 + (width + gap) * (columns - n_column - 1)
                y = y0 - (height + gap) * n_row

                pdf_canvas.setFont("Exo 2.0 Bold", 10)
                pdf_canvas.drawCentredString(
                    x + width / 2,
                    y - 38 * mm,
                    "Scan for more info",
                )

                qr = BytesIO()
                generate_qrcode(
                    qr,
                    url_format_qr.format(sku=product["sku"].lower()),
                    error_correction=ERROR_CORRECT_H,
                )
                qr.seek(0)
                qr_bytes = qr.read()
                qr = BytesIO(
                    qr_bytes.replace(
                        b'fill="#000000"', f'fill="{text_color}"'.encode("utf-8")
                    )
                )
                qr_drawing = svg2rlg(qr)
                qr_scale = 30 * mm / qr_drawing.height
                qr_drawing.scale(sx=qr_scale, sy=qr_scale)
                renderPDF.draw(
                    qr_drawing,
                    pdf_canvas,
                    x + width / 2 - qr_drawing.width * qr_scale / 2,
                    y - qr_drawing.height * qr_scale - 40 * mm,
                )
                pdf_canvas.setFont("Exo 2.0 Regular", 7)
                pdf_canvas.drawCentredString(
                    x + width / 2,
                    y - qr_drawing.height * qr_scale - 43 * mm,
                    url_format.format(sku=product["sku"].lower()),
                )

                pdf_canvas.setFont("Exo 2.0 Bold", 16)
                pdf_canvas.drawCentredString(
                    x + width / 2,
                    y - 80 * mm,
                    f"{product['price']} kr",
                )

        if n_page < pages - 1:
            pdf_canvas.showPage()

    pdf_canvas.save()

    reader = PdfReader(filename)
    writer = PdfWriter()
    writer.add_metadata({"/Title": "Backing Cards"})
    template_files = [
        "assets/templates/backing-cards-front.pdf",
        "assets/templates/backing-cards-back.pdf",
    ]

    for k, page in enumerate(reader.pages):
        template = PdfReader(template_files[k % len(template_files)]).pages[0]
        template.merge_page(page)
        writer.add_page(template)

    with open(filename, "wb") as f:
        writer.write(f)


def generate_price_tags(
    filename: str,
    products: list[ProductData],
    tagsize=(30 * mm, 52 * mm),
    pagesize=A4,
    cross_size=2 * mm,
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
        if len(page_data) == 0:
            break

        add_mesh(pdf_canvas, parameters, tagsize=tagsize, cross_size=cross_size)
        for n_row in range(rows):
            for n_column, product in enumerate(
                page_data[n_row * columns : (n_row + 1) * columns]
            ):
                x = parameters["box_x"] + tagsize[0] * n_column
                y = parameters["box_y"] + parameters["box_h"] - tagsize[1] * n_row

                pdf_canvas.circle(x + tagsize[0] / 2, y - 6 * mm, 2 * mm)

                renderPDF.draw(
                    logo_drawing,
                    pdf_canvas,
                    x + padding,
                    y - 30 * mm,
                )

                pdf_canvas.setFont(
                    "Exo 2.0 Bold",
                    find_max_fontsize(
                        product["title"],
                        "Exo 2.0 Bold",
                        tagsize[0] - 2 * padding,
                        starting_fontsize=12,
                    ),
                )
                pdf_canvas.drawCentredString(
                    x + tagsize[0] / 2,
                    y - 38 * mm,
                    product["title"],
                )

                pdf_canvas.setFont("Exo 2.0 Medium", 8)
                lines = line_wrap_text(
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

                pdf_canvas.circle(x + tagsize[0] / 2, y - 6 * mm, 2 * mm)

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
                    f"{product['price']} kr",
                )

        if n_page < pages - 1:
            pdf_canvas.showPage()

    pdf_canvas.save()


def calculate_page_parameters(
    tagsize=(60 * mm, 20 * mm), pagesize=A4, margin=10 * mm
) -> tuple[int, int]:
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
    cross_size=2 * mm,
):
    pdf_canvas.setLineWidth(0.4)
    for i in range(parameters["columns"] + 1):
        for j in range(parameters["rows"] + 1):
            pdf_canvas.line(
                parameters["box_x"] + i * tagsize[0],
                parameters["box_y"] + j * tagsize[1] - cross_size,
                parameters["box_x"] + i * tagsize[0],
                parameters["box_y"] + j * tagsize[1] + cross_size,
            )
    for i in range(parameters["rows"] + 1):
        for j in range(parameters["columns"] + 1):
            pdf_canvas.line(
                parameters["box_x"] + j * tagsize[0] - cross_size,
                parameters["box_y"] + i * tagsize[1],
                parameters["box_x"] + j * tagsize[0] + cross_size,
                parameters["box_y"] + i * tagsize[1],
            )
