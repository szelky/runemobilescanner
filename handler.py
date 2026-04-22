import cv2
import os
import datetime
from scanner import get_best_scan
from transform import four_point_transform

def process_and_save_handler(image):
    if image is None: return None, "Görüntü alınamadı."

    orig = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    screenCnt, ratio, target_img = get_best_scan(orig)

    if screenCnt is None:
        return None, "Kağıt kenarı bulunamadı. Lütfen arka planla zıt bir açıyla çekin."

    warped = four_point_transform(target_img, screenCnt.reshape(4, 2) * ratio)

    # Klasör ve Dosya İşlemleri
    save_path = "Taramalar"
    os.makedirs(save_path, exist_ok=True)
    fname = f"Scan_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    full_path = os.path.join(save_path, fname)
    
    cv2.imwrite(full_path, warped) # Islak imzayı korumak için direkt renkli kayıt

    return cv2.cvtColor(warped, cv2.COLOR_BGR2RGB), f"Kaydedildi: {fname}"
