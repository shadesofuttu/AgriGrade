"""
Real YOLOv8 Inference Service for Onion Quality Grading
Use this to replace inference.py after training the model
"""

from typing import Dict, List, Any
from PIL import Image
import numpy as np
import io
import os

class OnionInferenceService:
    """
    Real inference service using trained YOLOv8 model.
    Dataset classes: Class-1, Class-2, Extra Class, Reject
    """
    
    def __init__(self):
        self.model = None
        self.confidence_threshold = 0.25
        
        # Dataset class mapping (from Roboflow dataset)
        self.class_mapping = {
            0: "Class-1",      # Standard quality
            1: "Class-2",      # Lower quality
            2: "Extra Class",  # Premium quality
            3: "Reject"        # Poor quality/defective
        }
        
        # Load model if available
        model_path = os.getenv("MODEL_PATH", "models/best.pt")
        if os.path.exists(model_path):
            self.load_model(model_path)
        else:
            print(f"⚠️  Model not found at {model_path}")
            print("   Using mock mode until model is available")
    
    def load_model(self, model_path: str):
        """
        Load YOLOv8 model from path.
        """
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            print(f"✅ Model loaded successfully from {model_path}")
        except ImportError:
            print("❌ ultralytics not installed. Run: pip install ultralytics")
            self.model = None
        except Exception as e:
            print(f"❌ Error loading model: {e}")
            self.model = None
    
    def analyze_image(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        Analyze image and return detection results.
        """
        # Load image
        image = Image.open(io.BytesIO(image_bytes))
        
        # Use real model if available
        if self.model is not None:
            print(f"🔍 Running real inference on image size: {image.size}")
            results = self.model.predict(
                image, 
                conf=self.confidence_threshold,
                verbose=False
            )
            return self._parse_yolo_results(results[0])
        else:
            # Fallback to mock data
            print("⚠️  Using mock data (model not loaded)")
            return self._generate_mock_detections()
    
    def _parse_yolo_results(self, result) -> Dict[str, Any]:
        """
        Parse YOLOv8 detection results.
        """
        # Count detections per class
        class_counts = {}
        confidences = []
        
        for box in result.boxes:
            cls_id = int(box.cls)
            class_name = self.class_mapping.get(cls_id, f"Unknown-{cls_id}")
            confidence = float(box.conf)
            
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            confidences.append(confidence)
        
        # Calculate average confidence
        avg_confidence = np.mean(confidences) if confidences else 0.0
        
        # Build detections list
        detections_list = [
            {"class": cls_name, "count": count}
            for cls_name, count in class_counts.items()
        ]
        
        return {
            "total_onions": len(result.boxes),
            "detections": detections_list,
            "confidence": float(avg_confidence),
            "model_version": "yolov8-v1.0"
        }
    
    def _generate_mock_detections(self) -> Dict[str, Any]:
        """
        Generate mock detection results for testing.
        """
        import random
        
        total_onions = random.randint(80, 150)
        
        # Mock distribution based on typical results
        extra_class = int(total_onions * random.uniform(0.10, 0.20))  # Premium
        class_1 = int(total_onions * random.uniform(0.50, 0.65))      # Standard
        class_2 = int(total_onions * random.uniform(0.15, 0.25))      # Lower
        reject = total_onions - (extra_class + class_1 + class_2)     # Reject
        
        detections = {
            "total_onions": total_onions,
            "detections": [
                {"class": "Extra Class", "count": extra_class},
                {"class": "Class-1", "count": class_1},
                {"class": "Class-2", "count": class_2},
                {"class": "Reject", "count": reject}
            ],
            "confidence": random.uniform(0.85, 0.95),
            "model_version": "mock-v1.0"
        }
        
        return detections
    
    def calculate_grades(self, detections: Dict[str, Any]) -> Dict[str, Any]:
        """
        Map European grading to Indian/display categories.
        Mapping:
        - Extra Class → Grade A (Premium)
        - Class-1 → Grade A (Good)
        - Class-2 → URS (Undersized/Lower quality)
        - Reject → Damaged/Rotten/Defective
        """
        total = detections["total_onions"]
        
        extra_class_count = 0
        class_1_count = 0
        class_2_count = 0
        reject_count = 0
        
        for det in detections["detections"]:
            cls = det["class"]
            count = det["count"]
            
            if cls == "Extra Class":
                extra_class_count = count
            elif cls == "Class-1":
                class_1_count = count
            elif cls == "Class-2":
                class_2_count = count
            elif cls == "Reject":
                reject_count = count
        
        # Combine for display categories
        grade_a_count = extra_class_count + class_1_count
        urs_count = class_2_count
        damaged_count = reject_count
        rotten_count = 0  # Not separately detected in this dataset
        sprouted_count = 0  # Not separately detected in this dataset
        
        # Calculate percentages
        result = {
            "total_onions": total,
            "grade_a_count": grade_a_count,
            "urs_count": urs_count,
            "damaged_count": damaged_count,
            "rotten_count": rotten_count,
            "sprouted_count": sprouted_count,
            "grade_a_percentage": round((grade_a_count / total) * 100, 2) if total > 0 else 0,
            "urs_percentage": round((urs_count / total) * 100, 2) if total > 0 else 0,
            "damaged_percentage": round((damaged_count / total) * 100, 2) if total > 0 else 0,
            "rotten_percentage": 0.0,
            "sprouted_percentage": 0.0,
            "ai_confidence": round(detections["confidence"], 2),
            "detections": detections
        }
        
        return result

# Singleton instance
inference_service = OnionInferenceService()