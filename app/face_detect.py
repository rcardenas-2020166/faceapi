import os
import cv2
import numpy as np
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python as mp_python
from mediapipe.tasks.python import vision as mp_vision

from app.config import settings

_MODEL_PATH = os.path.join(os.path.dirname(__file__), "blaze_face_short_range.tflite")
_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_detector/blaze_face_short_range/float16/1/blaze_face_short_range.tflite"
)


def _ensure_model() -> None:
    if not os.path.exists(_MODEL_PATH):
        print("Descargando modelo de detección facial…", flush=True)
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)
        print(f"Modelo guardado en {_MODEL_PATH}", flush=True)


_ensure_model()

_detector = mp_vision.FaceDetector.create_from_options(
    mp_vision.FaceDetectorOptions(
        base_options=mp_python.BaseOptions(model_asset_path=_MODEL_PATH),
        min_detection_confidence=settings.min_detection_confidence,
    )
)


def decode_frame(jpeg_bytes: bytes) -> np.ndarray | None:
    arr = np.frombuffer(jpeg_bytes, np.uint8)
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def detect(frame: np.ndarray) -> dict:
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
    result = _detector.detect(mp_image)

    if not result.detections:
        return {"face_detected": False, "faces": []}

    faces = []
    for det in result.detections:
        bb = det.bounding_box
        score = det.categories[0].score if det.categories else 0.0
        faces.append({
            "confidence": round(float(score), 3),
            "bbox": {
                "x": bb.origin_x,
                "y": bb.origin_y,
                "w": bb.width,
                "h": bb.height,
            },
        })

    return {"face_detected": True, "faces": faces}
