import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

class CustomBlackWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.overrideredirect(True)
        self.geometry("820x570")
        self.configure(bg='black')
        
        # Create rounded corners
        self.create_rounded_window()

        # Create top-right tab
        self.create_tab()

        # Make window draggable
        self.bind("<ButtonPress-1>", self.start_move)
        self.bind("<ButtonRelease-1>", self.stop_move)
        self.bind("<B1-Motion>", self.do_move)

    def create_rounded_window(self):
        radius = 20
        width, height = 820, 570

        # Create a rounded rectangle
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle([0, 0, width, height], radius, fill='black')

        self.rounded_image = ImageTk.PhotoImage(image)
        self.canvas = tk.Canvas(self, width=width, height=height, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor='nw', image=self.rounded_image)

    def create_tab(self):
        tab_width, tab_height = 200, 80
        x_offset = 820 - tab_width

        # Create a rounded rectangle for the tab
        tab_image = Image.new('RGBA', (tab_width, tab_height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(tab_image)
        draw.rounded_rectangle([0, 0, tab_width, tab_height], 20, fill='black')

        self.tab_image = ImageTk.PhotoImage(tab_image)
        self.canvas.create_image(x_offset, 0, anchor='nw', image=self.tab_image)

        # Create close button
        close_button = tk.Button(self, text="x", font=("Arial", 16), fg='white', bg='black',
                                 command=self.quit, bd=1, relief="solid")
        close_button.place(x=x_offset+140, y=10, width=50, height=30)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def stop_move(self, event):
        self.x = None
        self.y = None

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry(f"+{x}+{y}")

if __name__ == "__main__":
    app = CustomBlackWindow()
    app.mainloop()