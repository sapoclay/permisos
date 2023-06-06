#sudo apt-get install python3-tk
import tkinter as tk
from tkinter import messagebox
import subprocess

def crear_usuario():
    nombre_usuario = campo_usuario.get()
    contrasena = campo_contrasena.get()

    grupos_seleccionados = obtener_grupos_seleccionados()
    grupos_adicionales_seleccionados = obtener_grupos_adicionales_seleccionados()

    comando_usuario = f'useradd -m -p {contrasena} -G {",".join(grupos_seleccionados + grupos_adicionales_seleccionados)} {nombre_usuario}'
    comando_carpeta = f'mkdir /home/{nombre_usuario}'

    try:
        subprocess.run(comando_usuario, shell=True, check=True)
        subprocess.run(comando_carpeta, shell=True, check=True)
        messagebox.showinfo("Éxito", f"Usuario {nombre_usuario} creado con éxito")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error al crear el usuario")

def obtener_grupos_seleccionados():
    grupos_seleccionados = []
    for i, grupo in enumerate(grupos):
        if grupo.get():
            grupos_seleccionados.append(grupos_nombres[i])
    return grupos_seleccionados

def obtener_grupos_adicionales_seleccionados():
    grupos_adicionales_seleccionados = []
    for i, grupo_adicional in enumerate(grupos_adicionales):
        if grupo_adicional.get():
            grupos_adicionales_seleccionados.append(grupos_adicionales_nombres[i])
    return grupos_adicionales_seleccionados

def cargar_grupos():
    resultado = subprocess.run("cut -d: -f1 /etc/group", shell=True, capture_output=True, text=True)
    grupos_disponibles = resultado.stdout.strip().split('\n')
    return grupos_disponibles

ventana = tk.Tk()
ventana.title("Interfaz para administración de usuarios")

etiqueta_usuario = tk.Label(ventana, text="Nombre de usuario:")
etiqueta_usuario.pack()

campo_usuario = tk.Entry(ventana)
campo_usuario.pack()

etiqueta_contrasena = tk.Label(ventana, text="Contraseña:")
etiqueta_contrasena.pack()

campo_contrasena = tk.Entry(ventana, show="*")
campo_contrasena.pack()

etiqueta_grupo = tk.Label(ventana, text="Grupos:")
etiqueta_grupo.pack()

scrolled_frame = tk.Frame(ventana)
scrolled_frame.pack()

scrolled_canvas = tk.Canvas(scrolled_frame, height=200)
scrolled_canvas.pack(side=tk.LEFT, fill=tk.Y)

scrollbar = tk.Scrollbar(scrolled_frame, orient=tk.VERTICAL, command=scrolled_canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

scrolled_canvas.configure(yscrollcommand=scrollbar.set)
scrolled_canvas.bind('<Configure>', lambda e: scrolled_canvas.configure(scrollregion=scrolled_canvas.bbox("all")))

frame_grupos = tk.Frame(scrolled_canvas)
scrolled_canvas.create_window((0, 0), window=frame_grupos, anchor=tk.NW)

grupos = []
grupos_nombres = cargar_grupos()

for i, nombre in enumerate(grupos_nombres):
    grupo_var = tk.BooleanVar()
    grupo = tk.Checkbutton(frame_grupos, text=nombre, variable=grupo_var)
    grupo.grid(row=i // 5, column=i % 5, sticky=tk.W)
    grupos.append(grupo_var)

etiqueta_grupos_adicionales = tk.Label(ventana, text="Grupos adicionales:")
etiqueta_grupos_adicionales.pack()

scrolled_frame_adicionales = tk.Frame(ventana)
scrolled_frame_adicionales.pack()

scrolled_canvas_adicionales = tk.Canvas(scrolled_frame_adicionales, height=200)
scrolled_canvas_adicionales.pack(side=tk.LEFT, fill=tk.Y)

scrollbar_adicionales = tk.Scrollbar(scrolled_frame_adicionales, orient=tk.VERTICAL, command=scrolled_canvas_adicionales.yview)
scrollbar_adicionales.pack(side=tk.RIGHT, fill=tk.Y)

scrolled_canvas_adicionales.configure(yscrollcommand=scrollbar_adicionales.set)
scrolled_canvas_adicionales.bind('<Configure>', lambda e: scrolled_canvas_adicionales.configure(scrollregion=scrolled_canvas_adicionales.bbox("all")))

frame_grupos_adicionales = tk.Frame(scrolled_canvas_adicionales)
scrolled_canvas_adicionales.create_window((0, 0), window=frame_grupos_adicionales, anchor=tk.NW)

grupos_adicionales = []
grupos_adicionales_nombres = cargar_grupos()

for i, nombre in enumerate(grupos_adicionales_nombres):
    grupo_adicional_var = tk.BooleanVar()
    grupo_adicional = tk.Checkbutton(frame_grupos_adicionales, text=nombre, variable=grupo_adicional_var)
    grupo_adicional.grid(row=i // 5, column=i % 5, sticky=tk.W)
    grupos_adicionales.append(grupo_adicional_var)

boton_crear = tk.Button(ventana, text="Crear usuario", command=crear_usuario)
boton_crear.pack()

ventana.mainloop()
