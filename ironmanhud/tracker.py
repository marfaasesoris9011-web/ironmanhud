from ultralytics import YOLO

class ObjectTracker:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)

    def process_frame(self, frame):
        # imgsz=320 tetep dipakai biar kenceng & ultra responsif
        results = self.model(frame, imgsz=320, verbose=False)[0]
        detections = []

        SENSITIVE_OBJECTS = ["knife", "scissors", "fork", "spoon"]

        for box in results.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = float(box.conf[0].cpu().numpy())
            cls_id = int(box.cls[0].cpu().numpy())
            label = self.model.names[cls_id]

            # Benda tajam dibuat SANGAT sensitif (0.12) biar kilat kebaca
            min_conf = 0.12 if label.lower() in SENSITIVE_OBJECTS else 0.35

            if conf > min_conf:
                detections.append([int(x1), int(y1), int(x2), int(y2), label, conf])

        return detections