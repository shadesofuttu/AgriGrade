# YOLOv8 Training Guide - Onion Quality Grading

**Dataset**: 508 images (405 train, 103 validation)  
**Classes**: 4 (Class-1, Class-2, Extra Class, Reject)  
**Date**: September 23, 2026

---

## 📊 Dataset Overview

```
dataset/onion_grading/
├── data.yaml           # Dataset configuration
├── train/
│   ├── images/         # 405 training images
│   └── labels/         # 405 YOLO format labels
└── valid/
    ├── images/         # 103 validation images
    └── labels/         # 103 YOLO format labels
```

**Class Distribution**:
- Class-1: Standard quality onions
- Class-2: Lower quality onions
- Extra Class: Premium quality onions
- Reject: Poor quality/defective onions

---

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
# Install ultralytics (YOLOv8)
pip install ultralytics

# Or install all backend requirements
cd backend
pip install -r requirements.txt
```

### Step 2: Train the Model

```bash
# From project root
python train_model.py
```

This will:
- Load YOLOv8 nano pretrained weights
- Train on your onion dataset for 100 epochs
- Save the best model to `runs/train/onion_grading/weights/best.pt`
- Generate training plots and metrics

**Expected Training Time**:
- CPU: 4-8 hours
- GPU (CUDA): 30-60 minutes

### Step 3: Test the Model

```bash
# Test on a sample image
python test_model.py

# Or test on specific image
python test_model.py path/to/your/image.jpg
```

### Step 4: Integrate with Backend

```bash
# 1. Copy trained model to backend
mkdir backend/models
copy runs/train/onion_grading/weights/best.pt backend/models/best.pt

# 2. Replace inference service
copy backend/app/services/inference_real.py backend/app/services/inference.py

# 3. Update .env file
echo MODEL_PATH=models/best.pt >> backend/.env

# 4. Restart backend server
cd backend
python run.py
```

---

## 📈 Expected Results

With 508 images, you should achieve:

- **mAP@50**: 85-92% (good)
- **mAP@50-95**: 70-85% (acceptable)
- **Inference Speed**: 20-50ms per image (on GPU)
- **Precision**: 80-90% per class
- **Recall**: 75-88% per class

---

## 🔧 Training Configuration

The `train_model.py` script uses these settings:

```python
epochs=100              # Training iterations
imgsz=640               # Image size (640x640)
batch=16                # Batch size
patience=20             # Early stopping
lr0=0.01                # Initial learning rate
weight_decay=0.0005     # Regularization
```

**To adjust for your hardware**:

```python
# If you have limited GPU memory
batch=8  # or batch=4

# If training is too slow
epochs=50

# For better accuracy (if you have time)
epochs=200
patience=50
```

---

## 📊 Monitoring Training

During training, watch for:

1. **Loss curves** should decrease steadily
2. **mAP** should increase over epochs
3. **Validation loss** shouldn't diverge from training loss (overfitting)

**Training outputs**:
```
runs/train/onion_grading/
├── weights/
│   ├── best.pt         # Best model checkpoint
│   └── last.pt         # Last epoch checkpoint
├── results.png         # Loss and metric curves
├── confusion_matrix.png
├── F1_curve.png
└── PR_curve.png
```

---

## 🧪 Validation & Testing

### Validate Model Performance

```python
from ultralytics import YOLO

model = YOLO('runs/train/onion_grading/weights/best.pt')
metrics = model.val()

print(f"mAP@50: {metrics.box.map50}")
print(f"mAP@50-95: {metrics.box.map}")
```

### Test on New Images

```python
from ultralytics import YOLO
from PIL import Image

model = YOLO('runs/train/onion_grading/weights/best.pt')
results = model.predict('path/to/onion_image.jpg', conf=0.25)

# Get detections
for result in results:
    boxes = result.boxes
    for box in boxes:
        class_id = int(box.cls)
        confidence = float(box.conf)
        class_name = result.names[class_id]
        print(f"Detected: {class_name} ({confidence:.2%})")
```

---

## 🔄 Model Improvement Tips

### If Accuracy is Low (<80% mAP):

1. **Collect more data**
   - Aim for 1000+ images
   - Balance class distribution

2. **Improve labeling quality**
   - Check for missed annotations
   - Fix incorrect labels
   - Ensure consistent labeling

3. **Try data augmentation**
   - Already included in training script
   - Add more variation if images are too similar

4. **Use larger model**
   ```python
   model = YOLO('yolov8s.pt')  # Small model (better accuracy)
   # or
   model = YOLO('yolov8m.pt')  # Medium model (even better)
   ```

5. **Train longer**
   ```python
   epochs=200
   patience=50
   ```

### If Inference is Too Slow:

1. **Use smaller model**
   ```python
   model = YOLO('yolov8n.pt')  # Nano (fastest)
   ```

2. **Reduce image size**
   ```python
   imgsz=416  # or 320 for mobile
   ```

3. **Export to optimized format**
   ```python
   model.export(format='onnx')  # Or 'tflite' for mobile
   ```

---

## 🐛 Troubleshooting

### Error: "ultralytics not found"
```bash
pip install ultralytics
```

### Error: "CUDA out of memory"
```python
# Reduce batch size in train_model.py
batch=8  # or batch=4
```

### Error: "No module named 'torch'"
```bash
pip install torch torchvision
```

### Warning: "Dataset not found"
```bash
# Check paths in data.yaml
cd dataset/onion_grading
cat data.yaml

# Ensure paths are correct relative to data.yaml location
```

### Model not detecting onions
1. Check confidence threshold (try lower: 0.1)
2. Verify model loaded correctly
3. Test on training images first
4. Check if image format is compatible

---

## 🔄 Integration Checklist

- [ ] Train model (`python train_model.py`)
- [ ] Validate results (check mAP > 80%)
- [ ] Test on sample images
- [ ] Copy model to `backend/models/best.pt`
- [ ] Install ultralytics in backend venv
- [ ] Replace `inference.py` with `inference_real.py`
- [ ] Update MODEL_PATH in `.env`
- [ ] Restart backend server
- [ ] Test upload from mobile app
- [ ] Verify real detections (not mock data)
- [ ] Check inference speed (<1 second)
- [ ] Test error handling (non-onion images)

---

## 📱 Production Deployment

### For Mobile Optimization

```python
# Export to TensorFlow Lite
model.export(format='tflite')

# Or ONNX for cross-platform
model.export(format='onnx')
```

### For Server Deployment

```python
# Keep PyTorch format (.pt)
# Or use ONNX for faster inference
model.export(format='onnx')
```

---

## 📚 Additional Resources

- [YOLOv8 Documentation](https://docs.ultralytics.com/)
- [Roboflow Universe](https://universe.roboflow.com/)
- [Model Training Tips](https://docs.ultralytics.com/guides/)
- [Performance Optimization](https://docs.ultralytics.com/guides/model-optimization/)

---

## 🎯 Success Metrics

**Minimum Viable Model**:
- mAP@50 > 80%
- Inference < 1 second
- Works on new images

**Production Ready**:
- mAP@50 > 90%
- mAP@50-95 > 75%
- Inference < 500ms
- Handles edge cases
- Robust to lighting variations

---

## 🚀 Next Steps After Training

1. **Collect more diverse data** (different lighting, angles, varieties)
2. **Fine-tune on Indian grading standards** if needed
3. **Add defect-specific classes** (sprouted, rotten, damaged)
4. **Implement active learning** (collect misclassified samples)
5. **A/B test different model versions**
6. **Monitor real-world performance**

---

**Ready to train? Run:**
```bash
python train_model.py
```

**Questions?** Check the documentation or open an issue.

---

*Last updated: September 23, 2026*