import img2pdf
import cv2
import os
import datetime
import numpy as np
from scanner import get_best_scan
from transform import four_point_transform

def process_and_save_handler(image, custom_name):
    if image is None: return None, "Görüntü alınamadı."

    orig = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    screenCnt, ratio, target_img = get_best_scan(orig)

    if screenCnt is None:
        return None, "Kağıt kenarı bulunamadı."

    warped = four_point_transform(target_img, screenCnt.reshape(4, 2) * ratio)

    save_path = "Taramalar"
    os.makedirs(save_path, exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name_part = custom_name.strip() if custom_name and custom_name.strip() else f"Scan_{timestamp}"
    fname = f"{name_part}.pdf"
    full_path = os.path.join(save_path, fname)

    a4inpt = (img2pdf.mm_to_pt(210), img2pdf.mm_to_pt(297))
    layout_fun = img2pdf.get_layout_fun(a4inpt)

    _, img_encoded = cv2.imencode(".jpg", warped, [cv2.IMWRITE_JPEG_QUALITY, 95])
    
    with open(full_path, "wb") as f:
        f.write(img2pdf.convert(img_encoded.tobytes(), layout_fun=layout_fun))

    return cv2.cvtColor(warped, cv2.COLOR_BGR2RGB), f"A4 PDF Kaydedildi: {fname}"
