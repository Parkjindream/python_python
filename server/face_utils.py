import face_recognition
import numpy as np

def encode_face_from_image(image):
    """
    รับ frame ของ OpenCV (BGR) แล้วส่งกลับเป็น bytes ของ face encoding
    """
    rgb_image = image[:, :, ::-1]  # BGR -> RGB
    encodings = face_recognition.face_encodings(rgb_image)
    if len(encodings) == 0:
        return None
    # แปลงเป็น bytes
    return encodings[0].tobytes()
