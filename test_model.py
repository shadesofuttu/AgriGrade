"""
Test the trained YOLOv8 model on sample images
"""

from ultralytics import YOLO
from PIL import Image
import os

def test_model(model_path='runs/train/onion_grading/weights/best.pt', test_image=None):
    """
    Test the trained model on an image
    """
    print("=" * 60)
    print("Testing Onion Quality Grading Model")
    print("=" * 60)
    
    # Load trained model
    print(f"\n📦 Loading model from: {model_path}")
    model = YOLO(model_path)
    
    # Get test image
    if test_image is None:
        # Use a random image from validation set
        val_images = os.listdir('dataset/onion_grading/valid/images')
        if val_images:
            test_image = os.path.join('dataset/onion_grading/valid/images', val_images[0])
        else:
            print("❌ No validation images found!")
            return
    
    print(f"🖼️  Testing on: {test_image}")
    
    # Run inference
    results = model.predict(test_image, conf=0.25, save=True, project='runs/predict')
    
    # Parse results
    result = results[0]
    
    print("\n" + "=" * 60)
    print("Detection Results")
    print("=" * 60)
    
    if len(result.boxes) == 0:
        print("❌ No onions detected in image!")
    else:
        class_counts = {}
        for box in result.boxes:
            cls_id = int(box.cls)
            class_name = result.names[cls_id]
            confidence = float(box.conf)
            
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            print(f"  • {class_name}: {confidence:.2%} confidence")
        
        print("\n📊 Summary:")
        print(f"  Total onions detected: {len(result.boxes)}")
        for cls, count in class_counts.items():
            print(f"  {cls}: {count} onions")
    
    print(f"\n💾 Results saved to: runs/predict/")
    print("=" * 60)

if __name__ == '__main__':
    import sys
    
    # Check if model exists
    model_path = 'runs/train/onion_grading/weights/best.pt'
    if not os.path.exists(model_path):
        print(f"❌ Model not found at: {model_path}")
        print("\nPlease train the model first:")
        print("  python train_model.py")
        sys.exit(1)
    
    # Get test image from command line or use default
    test_image = sys.argv[1] if len(sys.argv) > 1 else None
    
    test_model(model_path, test_image)