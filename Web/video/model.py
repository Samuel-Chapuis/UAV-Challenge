# model_loader.py
import torch
from ultralytics import YOLO

model_path = "runs/detect/train/weights/best.pt"
model = YOLO(model_path)

if torch.cuda.is_available():
    model.to("cuda")
    print("✅ Utilisation du GPU pour l'inférence.")
else:
    print("⚠️  Aucun périphérique CUDA trouvé ; utilisation du CPU.")
