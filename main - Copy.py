import tkinter as tk
import utils
import cv2
from PIL import Image, ImageTk
import os
import subprocess
import datetime


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1200x520+350+100")
        self.main_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.login_button_main_window = utils.get_button(
            self.main_window, 'Login', 'green', self.login
        )
        self.login_button_main_window.place(x=750, y=250)

        self.register_new_user_button = utils.get_button(
            self.main_window, 'Register New User', 'gray',
            self.register_new_user, fg='black'
        )
        self.register_new_user_button.place(x=750, y=320)

        self.webcam_label = utils.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)

        self.add_webcam(self.webcam_label)

        self.db_dir = "./db"
        os.makedirs(self.db_dir, exist_ok=True)

        self.log_path = "./log.txt"

    # ---------------- CAMERA ---------------- #
    def add_webcam(self, label):
        if hasattr(self, 'cap'):
            return
        self.cap = cv2.VideoCapture(0)
        self.label = label
        self.process_webcam()

    def process_webcam(self):
        ret, frame = self.cap.read()
        if ret:
            self.most_recent_capture = frame.copy()
            img = utils.cv2_to_tk(frame)
            self.label.imgtk = img
            self.label.configure(image=img)

        self.label.after(10, self.process_webcam)

    # ---------------- LOGIN ---------------- #
    def login(self):
        if not hasattr(self, 'most_recent_capture'):
            utils.msg_box("Error", "Camera not ready")
            return

        unknown_img_path = "temp.jpg"
        cv2.imwrite(unknown_img_path, self.most_recent_capture)

        try:
            output = subprocess.check_output(
                ["face_recognition", self.db_dir, unknown_img_path],
                stderr=subprocess.STDOUT
            ).decode("utf-8").strip()

            if "," in output:
                name = output.split(",")[1].strip()
                utils.msg_box("Result", f"Recognized: {name}")
            else:
                name = "UNKNOWN"
                utils.msg_box("Result", "Unknown person")

            with open(self.log_path, "a") as f:
                f.write(f"{name},{datetime.datetime.now()}\n")

        except Exception as e:
            utils.msg_box("Error", str(e))

        finally:
            if os.path.exists(unknown_img_path):
                os.remove(unknown_img_path)

    # ---------------- REGISTER ---------------- #
    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = utils.get_button(
            self.register_new_user_window, 'Accept', 'green',
            self.accept_register_new_user
        )
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = utils.get_button(
            self.register_new_user_window, 'TRY AGAIN', 'red',
            self.try_again_register_new_user
        )
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = utils.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.add_img_to_label(self.capture_label)

        self.text_label_register_new_user = utils.get_text_label(
            self.register_new_user_window, "Enter Username"
        )
        self.text_label_register_new_user.place(x=750, y=40)

        self.entry_text_register_new_user = utils.get_entry_text(
            self.register_new_user_window
        )
        self.entry_text_register_new_user.place(x=750, y=120)

    def add_img_to_label(self, label):
        if not hasattr(self, 'most_recent_capture'):
            return

        frame = cv2.cvtColor(self.most_recent_capture, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)

        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture.copy()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get().strip()

        if not name:
            utils.msg_box("Error", "Please enter a name")
            return

        path = os.path.join(self.db_dir, f"{name}.jpg")
        cv2.imwrite(path, self.register_new_user_capture)

        utils.msg_box("Success", "User registered successfully!")
        self.register_new_user_window.destroy()

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    # ---------------- CLOSE ---------------- #
    def on_close(self):
        if hasattr(self, 'cap'):
            self.cap.release()
        self.main_window.destroy()

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
