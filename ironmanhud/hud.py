import cv2
import time
import math

class HUDOverlay:
    def __init__(self):
        self.prev_time = time.time()
        self.angle_cw = 0          # Rotasi CW
        self.angle_ccw = 360       # Rotasi CCW
        self.pulse_r = 10          # Pulse radius
        self.scan_y = 50           # Posisi Y laser scan
        self.scan_speed = 8        # Kecepatan scan
        self.scan_dir = 1          # Arah scan
        self.frame_count = 0
        self.blink = True          # Variabel teks kedap-kedip

        # Skema Warna Normal (BGR)
        self.NORMAL_CYAN = (255, 255, 0)
        self.NORMAL_DARK_CYAN = (120, 120, 0)
        self.NORMAL_GREEN = (0, 255, 0)
        self.NORMAL_NEON_GREEN = (0, 255, 128)

        # Skema Warna RED ALERT
        self.ALERT_RED = (0, 0, 255)
        self.ALERT_DARK_RED = (0, 0, 139)
        self.ALERT_ORANGE = (0, 140, 255)

        # Palette Aktif (Default: Normal)
        self.CYAN = self.NORMAL_CYAN
        self.DARK_CYAN = self.NORMAL_DARK_CYAN
        self.GREEN = self.NORMAL_GREEN
        self.NEON_GREEN = self.NORMAL_NEON_GREEN
        self.YELLOW = (0, 235, 255)
        self.WHITE = (255, 255, 255)

    def set_alert_mode(self, is_alert):
        """Mengubah skema warna HUD secara otomatis jika Red Alert aktif"""
        if is_alert:
            self.CYAN = self.ALERT_RED
            self.DARK_CYAN = self.ALERT_DARK_RED
            self.GREEN = self.ALERT_RED
            self.NEON_GREEN = self.ALERT_ORANGE
        else:
            self.CYAN = self.NORMAL_CYAN
            self.DARK_CYAN = self.NORMAL_DARK_CYAN
            self.GREEN = self.NORMAL_GREEN
            self.NEON_GREEN = self.NORMAL_NEON_GREEN

    def draw_god_crosshair(self, frame, cx, cy):
        """Pusat Targetting Multi-Ring"""
        r_outer = 110
        cv2.ellipse(frame, (cx, cy), (r_outer, r_outer), self.angle_cw, 0, 90, self.CYAN, 2)
        cv2.ellipse(frame, (cx, cy), (r_outer, r_outer), self.angle_cw, 180, 270, self.CYAN, 2)

        r_mid = 85
        cv2.ellipse(frame, (cx, cy), (r_mid, r_mid), self.angle_ccw, 45, 135, self.CYAN, 1)
        cv2.ellipse(frame, (cx, cy), (r_mid, r_mid), self.angle_ccw, 225, 315, self.CYAN, 1)

        cv2.circle(frame, (cx, cy), 50, self.CYAN, 1)
        cv2.circle(frame, (cx, cy), 25, self.DARK_CYAN, 1)
        cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        cv2.circle(frame, (cx, cy), int(self.pulse_r), self.CYAN, 1)
        self.pulse_r += 3
        if self.pulse_r > 110:
            self.pulse_r = 10

        cv2.line(frame, (cx - 160, cy), (cx - 110, cy), self.CYAN, 2)
        cv2.line(frame, (cx + 110, cy), (cx + 160, cy), self.CYAN, 2)
        cv2.line(frame, (cx, cy - 160), (cx, cy - 110), self.CYAN, 2)
        cv2.line(frame, (cx, cy + 110), (cx, cy + 160), self.CYAN, 2)

        self.angle_cw = (self.angle_cw + 5) % 360
        self.angle_ccw = (self.angle_ccw - 7) % 360

    def draw_laser_scanner(self, frame, w, h):
        """Laser Scan Line"""
        cv2.line(frame, (0, self.scan_y), (w, self.scan_y), self.CYAN, 2)
        cv2.line(frame, (0, self.scan_y), (w, self.scan_y), self.WHITE, 1)

        self.scan_y += self.scan_speed * self.scan_dir
        if self.scan_y >= h - 40 or self.scan_y <= 40:
            self.scan_dir *= -1

    def draw_cyber_grid(self, frame, w, h):
        """Grid & Viewport Frame"""
        step = 80
        for x in range(step, w, step):
            cv2.line(frame, (x, 0), (x, h), (30, 30, 0), 1)
        for y in range(step, h, step):
            cv2.line(frame, (0, y), (w, y), (30, 30, 0), 1)

        m, l = 25, 40
        cv2.line(frame, (m, m), (m + l, m), self.CYAN, 3)
        cv2.line(frame, (m, m), (m, m + l), self.CYAN, 3)
        cv2.line(frame, (w - m, m), (w - m - l, m), self.CYAN, 3)
        cv2.line(frame, (w - m, m), (w - m, m + l), self.CYAN, 3)
        cv2.line(frame, (m, h - m), (m + l, h - m), self.CYAN, 3)
        cv2.line(frame, (m, h - m), (m, h - m - l), self.CYAN, 3)
        cv2.line(frame, (w - m, h - m), (w - m - l, h - m), self.CYAN, 3)
        cv2.line(frame, (w - m, h - m), (w - m, h - m - l), self.CYAN, 3)

    def draw_god_target_box(self, frame, bbox, label="TARGET", conf=0.0):
        """Target Box Objek"""
        x1, y1, x2, y2 = map(int, bbox)
        obj_cx, obj_cy = (x1 + x2) // 2, (y1 + y2) // 2
        diag = int(math.hypot(x2 - x1, y2 - y1) / 2) + 10

        color = self.GREEN if label.lower() == "person" else self.CYAN

        cv2.circle(frame, (obj_cx, obj_cy), diag, color, 1)
        cv2.ellipse(frame, (obj_cx, obj_cy), (diag + 6, diag + 6), self.angle_cw, 0, 120, color, 2)

        length = 20
        cv2.line(frame, (x1, y1), (x1 + length, y1), color, 2)
        cv2.line(frame, (x1, y1), (x1, y1 + length), color, 2)
        cv2.line(frame, (x2, y1), (x2 - length, y1), color, 2)
        cv2.line(frame, (x2, y1), (x2, y1 + length), color, 2)
        cv2.line(frame, (x1, y2), (x1 + length, y2), color, 2)
        cv2.line(frame, (x1, y2), (x1, y2 - length), color, 2)
        cv2.line(frame, (x2, y2), (x2 - length, y2), color, 2)
        cv2.line(frame, (x2, y2), (x2, y2 - length), color, 2)

        cv2.rectangle(frame, (x1, max(0, y1 - 25)), (x1 + 180, max(25, y1)), (10, 10, 10), -1)
        cv2.rectangle(frame, (x1, max(0, y1 - 25)), (x1 + 180, max(25, y1)), color, 1)
        
        cv2.putText(frame, f"LOCK: {label.upper()} [{int(conf*100)}%]", 
                    (x1 + 5, max(15, y1 - 8)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1, cv2.LINE_AA)

    def draw_top_widgets(self, frame, w, fps, is_alert):
        """Header Widget & Banner Red Alert Kedap-Kedip"""
        # Top Left Panel
        cv2.rectangle(frame, (35, 35), (340, 100), (15, 15, 15), -1)
        cv2.rectangle(frame, (35, 35), (340, 100), self.CYAN, 1)
        
        status_txt = "DEFENSE PROTOCOL: RED ALERT!" if is_alert else "PROTOCOL: THREAT ANALYSIS ONLINE"
        cv2.putText(frame, "MARK LXXXV // J.A.R.V.I.S OS", (45, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, self.CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, status_txt, (45, 73),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, self.CYAN, 1, cv2.LINE_AA)

        # Top Right Panel
        cv2.rectangle(frame, (w - 260, 35), (w - 35, 100), (15, 15, 15), -1)
        cv2.rectangle(frame, (w - 260, 35), (w - 35, 100), self.CYAN, 1)

        cv2.putText(frame, f"SYSTEM FPS  : {fps}", (w - 245, 55),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, self.CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, f"SYSTEM STATE: {'CRITICAL' if is_alert else 'NOMINAL'}", (w - 245, 73),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, self.CYAN, 1, cv2.LINE_AA)

        # BANNER WARNING KEDAP-KEDIP SAAT RED ALERT
        if is_alert and self.blink:
            banner_w = 420
            cx = w // 2
            cv2.rectangle(frame, (cx - banner_w//2, 35), (cx + banner_w//2, 85), (0, 0, 180), -1)
            cv2.rectangle(frame, (cx - banner_w//2, 35), (cx + banner_w//2, 85), (255, 255, 255), 2)
            cv2.putText(frame, "! WARNING: THREAT DETECTED !", (cx - 180, 67),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)

    def draw_bottom_widgets(self, frame, w, h, detections, is_alert):
        """Footer Widget"""
        person_cnt = sum(1 for d in detections if d[4].lower() == "person")

        # Bottom Left
        cv2.rectangle(frame, (35, h - 105), (320, h - 35), (15, 15, 15), -1)
        cv2.rectangle(frame, (35, h - 105), (320, h - 35), self.CYAN, 1)

        cv2.putText(frame, f"TOTAL OBJECTS DETECTED : {len(detections)}", (45, h - 85),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, self.CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, f"HUMAN TARGETS COUNT   : {person_cnt}", (45, h - 65),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, self.CYAN, 1, cv2.LINE_AA)
        cv2.putText(frame, f"THREAT ASSESSMENT    : {'HIGH DANGER!' if is_alert else 'LOW / CLEAR'}", 
                    (45, h - 45), cv2.FONT_HERSHEY_SIMPLEX, 0.38, self.CYAN, 1, cv2.LINE_AA)

        # Bottom Right
        cv2.rectangle(frame, (w - 260, h - 105), (w - 35, h - 35), (15, 15, 15), -1)
        cv2.rectangle(frame, (w - 260, h - 105), (w - 35, h - 35), self.CYAN, 1)
        cv2.putText(frame, "ARC REACTOR OUTPUT: 100%", (w - 245, h - 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.38, self.CYAN, 1, cv2.LINE_AA)

    def draw_hud(self, frame, detections=[], is_alert=False):
        h, w, _ = frame.shape
        cx, cy = w // 2, h // 2
        self.frame_count += 1

        # Toggle Blink Effect tiap 10 frame
        if self.frame_count % 10 == 0:
            self.blink = not self.blink

        # Terapkan Skema Warna
        self.set_alert_mode(is_alert)

        curr_time = time.time()
        fps = int(1 / (curr_time - self.prev_time + 1e-5))
        self.prev_time = curr_time

        self.draw_cyber_grid(frame, w, h)
        self.draw_laser_scanner(frame, w, h)
        self.draw_god_crosshair(frame, cx, cy)
        self.draw_top_widgets(frame, w, fps, is_alert)
        self.draw_bottom_widgets(frame, w, h, detections, is_alert)

        for det in detections:
            x1, y1, x2, y2, label, conf = det
            obj_cx, obj_cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv2.line(frame, (cx, cy), (obj_cx, obj_cy), self.CYAN, 1)
            self.draw_god_target_box(frame, (x1, y1, x2, y2), label, conf)

        return frame