import tkinter as tk
from ctypes import windll

def set_rounded_corners(window, radius):
    window.update_idletasks()
    hwnd = windll.user32.GetParent(window.winfo_id())
    windll.user32.SetWindowRgn(hwnd, windll.gdi32.CreateRoundRectRgn(0, 0, window.winfo_width(), window.winfo_height(), radius, radius), True)

def move_window(event):
    root.geometry(f'+{event.x_root}+{event.y_root}')

root = tk.Tk()
root.geometry("400x300")
root.overrideredirect(True)  # Eliminar el borde de la ventana

# Añadir un botón de cerrar
close_button = tk.Button(root, text="X", command=root.destroy)
close_button.pack(side="top", anchor="ne", padx=10, pady=10)

# Permitir mover la ventana arrastrando
root.bind("<B1-Motion>", move_window)

set_rounded_corners(root, 50)  # Esquinas redondeadas con radio de 50

label = tk.Label(root, text="Ventana con esquinas redondeadas", font=("Arial", 14))
label.pack(expand=True)

root.mainloop()
