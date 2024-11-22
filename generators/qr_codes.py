from decimal import Decimal
from io import BytesIO

import qrcode
from qrcode.image.styles import moduledrawers
from qrcode.image.svg import SvgPathImage


def generate_qrcode(f, url: str):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L, border=0)
    qr.add_data(url)
    img = qr.make_image(image_factory=SvgPathImage)
    img.save(f)
