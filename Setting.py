import cv2
import time
from Landmark import Landmark
import tkinter as tk
from PIL import Image, ImageTk

class EyeTracker:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv2.CAP_PROP_FPS, 30)

        self.landmark = Landmark()
        self.min_eye = float('inf')
        self.max_eye = float('-inf')
        self.start_time = None
        self.running = True
        self.window = tk.Tk()
        self.img_label = tk.Label(self.window)
        self.img_label.pack()
        self.text1 = tk.Label(self.window, text="顔が認識されることを確認してください",font=("Arial",15))
        self.text1.pack()
        self.quit_button = tk.Button(self.window, text="次へ", command = self.start_set_count)
        self.quit_button.pack()
        self.show_frame()

    def set_fname(self, name):
        self.fname = name

    def set_count(self):
        _, img = self.cap.read()
        eye, img = self.landmark.face_landmark_find(img)
        if eye != 10:  # Exclude eye value 10 from max calculation
            self.max_eye = max(self.max_eye, eye)
        self.min_eye = min(self.min_eye, eye)
        img = cv2.flip(img, 1)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.img_label.imgtk = imgtk
        self.img_label.configure(image=imgtk)
        if time.time()-self.start_time < 60:  # Call itself after 10 milliseconds if time limit not reached.
            self.window.after(10, self.set_count)
        else:
            self.on_closing()

    def on_closing(self):
        print("Max eye: ", self.max_eye)
        print("Min eye: ", self.min_eye)
        with open('user/'+self.fname+'.data', 'w') as f:
            f.write(f'{self.max_eye} {self.min_eye}\n')
        print("exit success")
        self.cap.release()
        self.window.destroy()  # Finally destroy the window

    def show_frame(self):
        if self.running:
            _, frame = self.cap.read()
            _, frame = self.landmark.face_landmark_find(frame)
            frame = cv2.flip(frame, 1)
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            self.img_label.imgtk = imgtk
            self.img_label.configure(image=imgtk)
            self.window.after(10, self.show_frame)  # Call itself after 10 milliseconds to get the next frame.

    def start_set_count(self):
        self.running = False
        self.quit_button.pack_forget()
        self.text1["text"]="サンプルを収集しています"
        self.start_time = time.time()  # Save the start time
        self.set_count()  # Start the counting process

if __name__ == "__main__":
    e = EyeTracker()
    e.window.mainloop()