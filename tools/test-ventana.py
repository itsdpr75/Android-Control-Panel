import customtkinter as ctk
import os

# configuraciones de la ventana
ventana = ctk.CTk()
ventana.geometry("400x200")
ventana.title("Test ubicacion")
ventana.configure(fg_color="#282c34")

#esto hace los cuadrados
# oscuro
cuadrado_oscuro = ctk.CTkFrame(ventana, corner_radius=10, fg_color="#36393f", width=300, height=100)
cuadrado_oscuro.place(relx=0.5, rely=0.5, anchor="center")

# claro
cuadrado_claro = ctk.CTkFrame(cuadrado_oscuro, corner_radius=5, fg_color="#454952", width=250, height=60)
cuadrado_claro.place(relx=0.5, rely=0.5, anchor="center")

# la ruta en la que estas _(pero solo el nombre de la carpeta)
ruta_archivo = os.path.abspath(__file__)
nombre_archivo = os.path.basename(ruta_archivo)

# esto obtiene el nombre de la carpeta :>
nombre_carpeta = os.path.basename(os.path.dirname(ruta_archivo))

# aqui es donde estan los campos de texto con la ubicacion en la que estas
campo_nombre_archivo = ctk.CTkEntry(cuadrado_claro, placeholder_text="Nombre del archivo", width=150, height=25)
campo_nombre_archivo.place(relx=0.1, rely=0.1)
campo_nombre_archivo.insert(0, nombre_archivo)
campo_nombre_archivo.configure(state="readonly")

campo_nombre_carpeta = ctk.CTkEntry(cuadrado_claro, placeholder_text="Nombre de la carpeta", width=150, height=25)
campo_nombre_carpeta.place(relx=0.1, rely=0.5)
campo_nombre_carpeta.insert(0, nombre_carpeta)
campo_nombre_carpeta.configure(state="readonly")

ventana.mainloop()
