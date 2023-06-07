#sudo apt-get install python3-tk
import tkinter as tk
from tkinter import messagebox
import subprocess

def crear_usuario():
    username = username_entry.get()
    if username:
        try:
            subprocess.run(["sudo", "useradd", "-m", username])
            messagebox.showinfo("Éxito", f"El usuario {username} ha sido creado correctamente.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "No se pudo crear el usuario.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre de usuario.")

def eliminar_usuario():
    username = users_dropdown.get()
    if username:
        confirmar = messagebox.askyesno("Confirmar", f"¿Estás seguro de que deseas eliminar al usuario {username} y su carpeta de inicio?")
        if confirmar:
            try:
                subprocess.run(["sudo", "userdel", "-r", username])
                messagebox.showinfo("Éxito", f"El usuario {username} y su carpeta de inicio han sido eliminados correctamente.")
                # Actualizar los checkboxes después de eliminar al usuario
                mostrar_grupos()
            except subprocess.CalledProcessError:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")
        else:
            messagebox.showinfo("Información", "La eliminación del usuario ha sido cancelada.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario.")

def crear_grupo():
    groupname = group_entry.get()
    if groupname:
        try:
            subprocess.run(["sudo", "groupadd", groupname])
            messagebox.showinfo("Éxito", f"El grupo {groupname} ha sido creado correctamente.")
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "No se pudo crear el grupo.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre de grupo.")

def agregar_a_grupos():
    username = users_dropdown_groups.get()
    selected_groups = []
    for group, var in group_checkboxes.items():
        if var.get():
            selected_groups.append(group)
    if username and selected_groups:
        try:
            subprocess.run(["sudo", "usermod", "-aG", ",".join(selected_groups), username])
            messagebox.showinfo("Éxito", f"El usuario {username} ha sido agregado a los grupos seleccionados.")
            # Actualizar los checkboxes después de agregar al usuario a los grupos
            mostrar_grupos()
        except subprocess.CalledProcessError:
            messagebox.showerror("Error", "No se pudo agregar al usuario a los grupos.")
    elif not username:
        messagebox.showwarning("Advertencia", "Por favor, selecciona un usuario.")
    else:
        messagebox.showwarning("Advertencia", "Por favor, selecciona al menos un grupo.")

def mostrar_grupos(*args):
    selected_user = users_dropdown.get() if args == () else users_dropdown_groups.get()
    if selected_user:
        user_groups = subprocess.check_output(["id", "-Gn", selected_user]).decode("utf-8").strip().split(" ")
        for group, var in group_checkboxes.items():
            if group in user_groups:
                var.set(True)
            else:
                var.set(False)
    else:
        for var in group_checkboxes.values():
            var.set(False)

# Obtener la lista de usuarios y grupos del sistema
usuarios = subprocess.check_output(["cut", "-d:", "-f1", "/etc/passwd"]).decode("utf-8").splitlines()
grupos = subprocess.check_output(["cut", "-d:", "-f1", "/etc/group"]).decode("utf-8").splitlines()

# Crear la ventana principal
window = tk.Tk()
window.title("Administración de usuarios y grupos")
window.geometry("850x850")

# Etiqueta y campo de entrada para el nombre de usuario
username_label = tk.Label(window, text="Nombre de usuario:")
username_label.pack()
username_entry = tk.Entry(window)
username_entry.pack()

# Botón para crear usuarios
crear_button = tk.Button(window, text="Crear usuario", command=crear_usuario)
crear_button.pack(pady=5)

# Menú desplegable para seleccionar un usuario existente y eliminarlo
username_label = tk.Label(window, text="Seleccionar usuario:")
username_label.pack()
users_dropdown = tk.StringVar(window)
users_dropdown.set(usuarios[0])  # Establecer el valor inicial del menú
users_menu = tk.OptionMenu(window, users_dropdown, *usuarios, command=mostrar_grupos)
users_menu.pack()

eliminar_button = tk.Button(window, text="Eliminar usuario", command=eliminar_usuario)
eliminar_button.pack(pady=5)

# Etiqueta y campo de entrada para el nombre del grupo
group_label = tk.Label(window, text="Nombre del grupo:")
group_label.pack()
group_entry = tk.Entry(window)
group_entry.pack()

# Botón para crear un grupo
crear_grupo_button = tk.Button(window, text="Crear grupo", command=crear_grupo)
crear_grupo_button.pack(pady=5)

# Listado de checkboxes para seleccionar grupos
groups_frame = tk.Frame(window)
groups_frame.pack(pady=10)
group_checkboxes = {}
row = 0
col = 0
for group in grupos:
    var = tk.BooleanVar()
    checkbox = tk.Checkbutton(groups_frame, text=group, variable=var)
    checkbox.grid(row=row, column=col, padx=5, pady=2, sticky="w")
    group_checkboxes[group] = var
    col += 1
    if col == 5:
        col = 0
        row += 1

# Menú desplegable para seleccionar un usuario existente para agregar a los grupos
username_label_groups = tk.Label(window, text="Seleccionar usuario:")
username_label_groups.pack()
users_dropdown_groups = tk.StringVar(window)
users_dropdown_groups.set(usuarios[0])  # Establecer el valor inicial del menú
users_menu_groups = tk.OptionMenu(window, users_dropdown_groups, *usuarios, command=mostrar_grupos)
users_menu_groups.pack()

# Botón para agregar al usuario a los grupos seleccionados
agregar_grupos_button = tk.Button(window, text="Añadir a grupos", command=agregar_a_grupos)
agregar_grupos_button.pack(pady=5)

# Ejecutar el bucle principal de la interfaz de usuario
window.mainloop()
