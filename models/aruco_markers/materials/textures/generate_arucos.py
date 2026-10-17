import cv2
import numpy as np

try:
    # ArUco sözlüğünü al
    if hasattr(cv2.aruco, 'Dictionary_get'):
        dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_ARUCO_ORIGINAL)
    else:
        dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

    # Sistemindeki OpenCV sürümüyle uyumlu olan drawMarker fonksiyonunu kullanıyoruz
    # ID 101 oluştur (Kalkış Noktası için, 150x150 piksel)
    marker_101 = cv2.aruco.drawMarker(dictionary, 101, 150)
    cv2.imwrite('aruco_101.png', marker_101)

    # ID 102 oluştur (İniş Hedefi için, 150x150 piksel)
    marker_102 = cv2.aruco.drawMarker(dictionary, 102, 150)
    cv2.imwrite('aruco_102.png', marker_102)

    print("ArUco ID 101 ve 102 resimleri başarıyla oluşturuldu!")
except Exception as e:
    print("Hata oluştu:", e)
