import hashlib
import qrcode
import os
from io import BytesIO
import base64

def generate_qr(prepaid_no):
    hash_data = hashlib.md5(prepaid_no.encode()).hexdigest()

    img = qrcode.make(hash_data)

    buffer = BytesIO()
    img.save(buffer, format="PNG")

    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    return image_base64