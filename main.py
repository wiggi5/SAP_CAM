import cv2
import tkinter as tk
from tkinter import simpledialog, filedialog
from PIL import Image, ImageTk
import configparser
import os

class CameraApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PRX SAP Cam")

        # Konfiguration laden
        self.config = configparser.ConfigParser()
        self.config.read("config.ini")
        self.camera_index = int(self.config["Settings"]["camera_index"])
        
        # Menü erstellen
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)
        
        self.camera_menu = tk.Menu(self.menu, tearoff=0)
        self.menu.add_cascade(label="Kamera", menu=self.camera_menu)
        
        # Kameraauswahl hinzufügen
        self.camera_menu.add_command(label="Kamera 0", command=lambda: self.select_camera(0))
        self.camera_menu.add_command(label="Kamera 1", command=lambda: self.select_camera(1))
        self.camera_menu.add_command(label="Kamera 2", command=lambda: self.select_camera(2))
        
        self.video_capture = cv2.VideoCapture(self.camera_index)
        self.canvas = tk.Canvas(root, width=640, height=480)
        self.canvas.pack()
        self.btn_snapshot = tk.Button(root, text="Bild aufnehmen", command=self.snapshot)
        self.btn_snapshot.pack()
        self.update_frame()

    def select_camera(self, camera_index):
        self.camera_index = camera_index
        self.config['Settings']['camera_index'] = str(camera_index)
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
        self.video_capture.release()
        self.video_capture = cv2.VideoCapture(camera_index)
        self.update_frame()

    def update_frame(self):
        ret, frame = self.video_capture.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.root.after(10, self.update_frame)

    def snapshot(self):
        ret, frame = self.video_capture.read()
        if ret:
            filename = simpledialog.askstring("Materialnummer", "Geben Sie die Materialnummer ein:")
            if filename:
                    sap_bilder_path = os.path.join("../SAP_Bilder")
                    if not os.path.exists(sap_bilder_path):
                        os.makedirs(sap_bilder_path)
                    resized_1 = cv2.resize(frame, (2048, 1536))
                    resized_2 = cv2.resize(frame, (1024, 768))
                    cv2.imwrite(f"{sap_bilder_path}/{filename}.jpg", resized_1)
                    cv2.imwrite(f"{sap_bilder_path}/{filename}_SAP.jpg", resized_2)

    def __del__(self):
        self.video_capture.release()

if __name__ == "__main__":
    root = tk.Tk()
    app = CameraApp(root)
    root.mainloop()