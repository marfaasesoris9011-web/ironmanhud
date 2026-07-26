import cv2
import time
from hud import HUDOverlay
from tracker import ObjectTracker
from voice import JARVISVoice

def main():
    cap = cv2.VideoCapture(0)
    
    # Resolusi kencang & ringan
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    hud = HUDOverlay()
    tracker = ObjectTracker('yolov8n.pt')
    jarvis = JARVISVoice()

    cv2.namedWindow("J.A.R.V.I.S - Iron Man HUD", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("J.A.R.V.I.S - Iron Man HUD", 800, 600)

    print("=== J.A.R.V.I.S INSTANT HAZARD RESPONSE ACTIVE ===")

    DANGEROUS_OBJECTS = ["knife", "scissors", "fork"]

    last_spoken_time = 0
    danger_cooldown = 1.5  # Respons suara bahaya dipersingkat jadi 1.5 detik biar gercep!
    normal_cooldown = 3.0

    manual_alert = False
    last_danger_detected_time = 0
    danger_hold_duration = 3.5  # Kunci status Red Alert 3.5 detik
    detected_danger_name = ""

    cached_detections = []

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        current_time = time.time()

        # Deteksi di setiap frame tanpa menunda
        detections = tracker.process_frame(frame)

        # Cek Benda Tajam secara Instant
        has_dangerous_object = False
        for det in detections:
            label = det[4].lower()
            if label in DANGEROUS_OBJECTS:
                has_dangerous_object = True
                detected_danger_name = label
                last_danger_detected_time = current_time
                break

        # Logika Red Alert Instant
        is_danger_active = (current_time - last_danger_detected_time) < danger_hold_duration
        is_alert_active = is_danger_active or manual_alert

        # Voice Trigger yang jauh lebih responsif
        active_cooldown = danger_cooldown if is_danger_active else normal_cooldown
        
        if is_alert_active and (current_time - last_spoken_time > active_cooldown):
            if is_danger_active and detected_danger_name:
                jarvis.speak(f"Warning! Dangerous object detected: {detected_danger_name}")
            else:
                jarvis.speak("Red alert mode activated.")
            last_spoken_time = current_time

        # Render HUD Overlay
        frame = hud.draw_hud(frame, detections, is_alert=is_alert_active)

        # Tampilkan Layar
        cv2.imshow("J.A.R.V.I.S - Iron Man HUD", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('a') or key == ord('A'):
            manual_alert = not manual_alert

        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()