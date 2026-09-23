#!/usr/bin/env python3
"""
YOLOv8 Training Script for Onion Quality Grading
Dataset: onion_spoilage v6 - 772 images, 4 classes: healthy, mold, rotten, sprouted
"""

from ultralytics import YOLO
import torch

def main():
    print("=" * 60)
    print("YOLOv8 Onion Quality Grading Model Training")
    print("=" * 60)
    
    # Check if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"\n✅ Using device: {device}")
    
    # Load pretrained YOLOv8 model
    print("\n📦 Loading YOLOv8 nano model...")
    model = YOLO('yolov8n.pt')  # nano model - fastest, good for mobile
    
    # Train the model
    print("\n🚀 Starting training...")
    results = model.train(
        data='dataset/onion_spoilage/data.yaml',  # Path to dataset config
        epochs=100,                               # Number of training epochs
        imgsz=640,                                # Image size
        batch=16,                                 # Batch size (adjust based on GPU memory)
        patience=20,                              # Early stopping patience
        save=True,                                # Save checkpoints
        device=device,                            # CPU or GPU
        project='runs/train',                     # Save directory
        name='onion_spoilage',                    # Experiment name
        exist_ok=True,                            # Overwrite existing
        plots=True,                               # Save plots
        verbose=True,                             # Verbose output
        
        # Hyperparameters
        lr0=0.01,                                 # Initial learning rate
        lrf=0.01,                                 # Final learning rate
        momentum=0.937,                           # SGD momentum
        weight_decay=0.0005,                      # Weight decay
        warmup_epochs=3,                          # Warmup epochs
        
        # Augmentation
        hsv_h=0.015,                              # HSV-Hue augmentation
        hsv_s=0.7,                                # HSV-Saturation augmentation
        hsv_v=0.4,                                # HSV-Value augmentation
        degrees=0.0,                              # Rotation augmentation
        translate=0.1,                            # Translation augmentation
        scale=0.5,                                # Scale augmentation
        flipud=0.0,                               # Flip up-down augmentation
        fliplr=0.5,                               # Flip left-right augmentation
        mosaic=1.0,                               # Mosaic augmentation
    )
    
    # Validate the model
    print("\n📊 Validating model...")
    metrics = model.val()
    
    # Print results
    print("\n" + "=" * 60)
    print("Training Complete!")
    print("=" * 60)
    print(f"📈 mAP50: {metrics.box.map50:.4f}")
    print(f"📈 mAP50-95: {metrics.box.map:.4f}")
    print(f"💾 Best model saved to: runs/train/onion_spoilage/weights/best.pt")
    print("=" * 60)
    
    return model

if __name__ == '__main__':
    # Install requirements first
    print("\n⚠️  Make sure you have installed ultralytics:")
    print("    pip install ultralytics")
    print()
    
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Install ultralytics: pip install ultralytics")
        print("2. Check dataset path: dataset/onion_spoilage/data.yaml")
        print("3. Ensure images are in correct folders")