import hashlib
import qrcode
import os



def generate_qr(prepaid_no):
    hash_data = hashlib.md5(prepaid_no.encode()).hexdigest()

    filename = f"qr_{hash_data}.png"
    folder = "media"

    # ✅ AUTO CREATE FOLDER
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)

    img = qrcode.make(hash_data)
    img.save(path)

    return filename