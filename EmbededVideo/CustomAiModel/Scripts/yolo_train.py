import os
import torch
from ultralytics import YOLO

def train_yolo():
    # Verify if CUDA is available
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"🔍 Utilisation du périphérique : {device}")

    # Define dataset and model paths
    dataset_path = "C:/Devellopement/Projets/Dassault_UAV/EmbededVideo/CustomAiModel/dataset"
    model_save_path = "C:/Devellopement/Projets/Dassault_UAV/EmbededVideo/CustomAiModel/runs/detect/train/weights/best.pt"

    # Load YOLO model
    model = YOLO("yolov8n.pt")

    # Train the model
    model.train(
        data=f"{dataset_path}/data.yaml",  
        epochs=50,  
        batch=8,  
        imgsz=1280,  
        device=device,  
        workers=0  # 🔴 Important: Set this to 0 to avoid multiprocessing issues
    )

    print("✅ Training completed successfully!")

if __name__ == '__main__':
    train_yolo()
