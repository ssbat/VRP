import tkinter as tk
from tkinter import ttk

class SecondFrame:
    def __init__(self, root, previous_frame):
        self.root = root
        self.previous_frame = previous_frame
        self.frame = ttk.Frame(self.root, width=600, height=700)
        self.frame.place(x=0, y=0)  

        ttk.Label(
            self.frame, text="Second Frame", 
            font=("Arial", 16, "bold")
        ).place(x=100, y=30, width=400, height=30)  # Adjusted position and size

        ttk.Button(
            self.frame, text="Back", command=self.go_back
        ).place(x=250, y=100, width=100, height=30)  # Adjust as needed

    def go_back(self):
        self.frame.place_forget()  # Hide current frame

        self.previous_frame.place(x=0, y=0)  # Show previous frame
