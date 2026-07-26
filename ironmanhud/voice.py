import os
import threading
import pyttsx3
import pygame

class JARVISVoice:
    def __init__(self):
        # Inisialisasi Pygame Mixer untuk MP3
        self.use_mp3 = False
        try:
            pygame.mixer.init()
            self.sound_path = "lock.mp3"
            if os.path.exists(self.sound_path):
                self.lock_sound = pygame.mixer.Sound(self.sound_path)
                self.use_mp3 = True
                print("[VOICE] File 'lock.mp3' berhasil dimuat.")
            else:
                print(f"[VOICE] File '{self.sound_path}' tidak ditemukan. Menggunakan Text-To-Speech bawaan.")
        except Exception as e:
            print(f"[VOICE ERROR Mixer]: {e}")

    def _tts_worker(self, text):
        """Worker terpisah untuk Text-To-Speech agar tidak membekukan layar video"""
        try:
            try:
                engine = pyttsx3.init('sapi5')
            except Exception:
                engine = pyttsx3.init()
            
            engine.setProperty('rate', 160)
            engine.setProperty('volume', 1.0)
            
            voices = engine.getProperty('voices')
            for voice in voices:
                if "english" in voice.name.lower() or "david" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    break

            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"[TTS ERROR]: {e}")

    def speak(self, text):
        """Mengucapkan kalimat lisan"""
        print(f"[J.A.R.V.I.S]: {text}")
        t = threading.Thread(target=self._tts_worker, args=(text,), daemon=True)
        t.start()

    def play_target_lock(self, target_name="person"):
        """Memutar suara MP3 jika ada, jika tidak ada pakai suara lisan"""
        if self.use_mp3:
            try:
                self.lock_sound.play()
            except Exception as e:
                print(f"[MP3 ERROR]: {e}")
                self.speak(f"Target locked. {target_name} identified.")
        else:
            self.speak(f"Target locked. {target_name} identified.")


# Jalankan file ini secara langsung untuk mengetes suara!
if __name__ == "__main__":
    v = JARVISVoice()
    print("Testing Suara...")
    v.speak("Warning! Dangerous object detected.")
    input("Press Enter to exit...")