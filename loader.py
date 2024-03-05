from threading import Thread
import cv2
import tkinter as tk
from tkinter import Button, Canvas
from PIL import Image, ImageTk
from VirtualMouse import VirtualMouse

class VideoCanvas(Canvas):
    def __init__(self, master, video_path):
        self.cap = cv2.VideoCapture(video_path)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        super().__init__(master, width=width, height=height, bg="black")
        self.after(10, self.update)

    def update(self):
        success, frame = self.cap.read()
        if success:
            self.photo = self.convert_frame_to_photo(frame)
            self.create_image(0, 0, anchor=tk.NW, image=self.photo)
            self.after(25, self.update)
        else:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Reset to the beginning
            self.update()  # Continue looping

    def convert_frame_to_photo(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=pil_image)
        return img

class JarWizApp:
    def __init__(self, master):
        self.master = master
        master.title("JarWiz")
        master.configure(bg="black")  # Set the background color of the GUI

        # Use "fxVE.mp4" as the background video
        self.video_canvas = VideoCanvas(master, video_path="./fxVE.mp4")
        self.video_canvas.pack()

        # Get the dimensions of the video canvas
        canvas_width = self.video_canvas.winfo_reqwidth()
        canvas_height = self.video_canvas.winfo_reqheight()

        # Center the button in the middle of the video canvas
        self.start_button = Button(master, text="Start Video", command=self.start_video_thread, bg="black", fg="white")
        self.start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.vm = VirtualMouse()

    def start_video_thread(self):
        self.start_button.destroy()  # Remove the button when starting video
        self.master.after(10, self.play_video)

    def play_video(self):
        cap = cv2.VideoCapture("./vid.mp4")

        while cap.isOpened():  # Play the video once
            success, frame = cap.read()
            if success:
                cv2.imshow('Video Player', frame)
                if cv2.waitKey(25) & 0xFF == ord('q'):  # wait for a key press for 25 ms
                    break
            else:
                print("Video ended")
                break

        cap.release()
        cv2.destroyAllWindows()

        self.vm.run()

if __name__ == "__main__":
    root = tk.Tk() 
    app = JarWizApp(root)
    root.mainloop()

