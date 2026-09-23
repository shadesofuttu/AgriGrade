from typing import Dict, Any
from PIL import Image
import numpy as np
import io
import os

class OnionInferenceService:
    """
    YOLOv8 inference service for onion quality detection.
    Dataset: onion_spoilage v6
    Model classes (from dataset, unchanged):
        0 = healthy
        1 = mold
        2 = rotten
        3 = sprouted
    Display mapping (prototype only):
        healthy  -> Grade A
        mold     -> Defective
        rotten   -> Rotten
        sprouted -> Sprouted
    URS is NOT implemented (not in dataset).
    """
    
    # Model class names exactly as in onion_spoilage dataset
    MODEL_CLASSES = {
        0: "healthy",
        1: "mold",
        2: "rotten",
        3: "sprouted"
    }

    # Display label mapping: model class name -> display label
    # This is a prototype mapping only, NOT official grading
    DISPLAY_LABELS = {
        "healthy": "Grade A",
        "mold": "Defective",
        "rotten": "Rotten",
        "sprouted": "Sprouted"
    }

    def __init__(self):
        self.model = None
        self.confidence_threshold = 0.25
        self.model_version = "mock-v1.0"

        # Try to load trained model
        model_path = os.getenv("MODEL_PATH", "models/best.pt")
        if os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print(f"[Inference] Model not found at '{model_path}'. Running in mock mode.")

    def load_model(self, model_path: str):
        """
        Load trained YOLOv8 model from path.
        """
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            self.model_version = "onion-spoilage-v6"
            print(f"[Inference] Model loaded from '{model_path}'")
        except ImportError:
            print("[Inference] ultralytics not installed. Run: pip install ultralytics")
            self.model = None
        except Exception as e:
            print(f"[Inference] Failed to load model: {e}")
            self.model = None

    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyze image using YOLOv8 model.
        Falls back to mock data if model is not loaded.
        """
        image = Image.open(io.BytesIO(image_bytes))
        print(f"[Inference] Image size: {image.size}")

        if self.model is not None:
            print("[Inference] Running real YOLOv8 inference...")
            results = self.model.predict(image, conf=self.confidence_threshold, verbose=False)
            return self._parse_yolo_results(results[0])
        else:
            print("[Inference] Mock mode: returning random data")
            return self._generate_mock_detections()

    def _parse_yolo_results(self, result) -> Dict[str, Any]:
        """
        Parse YOLOv8 result into standard detection dict.
        Uses MODEL_CLASSES (not display labels).
        """
        class_counts = {name: 0 for name in self.MODEL_CLASSES.values()}
        confidences = []

        for box in result.boxes:
            cls_id = int(box.cls)
            class_name = self.MODEL_CLASSES.get(cls_id)
            if class_name:
                class_counts[class_name] += 1
                confidences.append(float(box.conf))

        total = sum(class_counts.values())
        avg_confidence = float(np.mean(confidences)) if confidences else 0.0

        detections_list = [
            {"class": cls_name, "count": count}
            for cls_name, count in class_counts.items()
        ]

        return {
            "total_onions": total,
            "detections": detections_list,
            "confidence": round(avg_confidence, 4),
            "model_version": self.model_version
        }

    def _generate_mock_detections(self) -> Dict[str, Any]:
        """
        Mock fallback using onion_spoilage class names.
        """
        import random
        total = random.randint(50, 120)
        healthy  = int(total * random.uniform(0.55, 0.75))
        mold     = int(total * random.uniform(0.05, 0.15))
        sprouted = int(total * random.uniform(0.05, 0.10))
        rotten   = total - (healthy + mold + sprouted)
        rotten   = max(rotten, 0)

        return {
            "total_onions": total,
            "detections": [
                {"class": "healthy",  "count": healthy},
                {"class": "mold",     "count": mold},
                {"class": "rotten",   "count": rotten},
                {"class": "sprouted", "count": sprouted}
            ],
            "confidence": round(random.uniform(0.60, 0.85), 4),
            "model_version": "mock-v1.0"
        }
    
    def calculate_grades(self, detections: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map model class names to database fields.

        Model class  -> DB field       -> Display label (prototype)
        healthy      -> grade_a_count  -> Grade A
        mold         -> damaged_count  -> Defective
        rotten       -> rotten_count   -> Rotten
        sprouted     -> sprouted_count -> Sprouted
        (no URS - not in dataset, not trained)
        """
        total = detections["total_onions"]
        
        grade_a_count  = 0  # healthy
        damaged_count  = 0  # mold (display: Defective)
        rotten_count   = 0  # rotten
        sprouted_count = 0  # sprouted
        urs_count      = 0  # always 0, not in dataset

        for det in detections["detections"]:
            cls = det["class"]
            count = det["count"]
            if cls == "healthy":
                grade_a_count = count
            elif cls == "mold":
                damaged_count = count
            elif cls == "rotten":
                rotten_count = count
            elif cls == "sprouted":
                sprouted_count = count

        def pct(n):
            return round((n / total) * 100, 2) if total > 0 else 0.0

        return {
            "total_onions":        total,
            "grade_a_count":       grade_a_count,
            "urs_count":           urs_count,
            "damaged_count":       damaged_count,
            "rotten_count":        rotten_count,
            "sprouted_count":      sprouted_count,
            "grade_a_percentage":  pct(grade_a_count),
            "urs_percentage":      0.0,
            "damaged_percentage":  pct(damaged_count),
            "rotten_percentage":   pct(rotten_count),
            "sprouted_percentage": pct(sprouted_count),
            "ai_confidence":       detections["confidence"],
            "detections":          detections
        }


# Singleton instance
inference_service = OnionInferenceService()