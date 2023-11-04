import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# -------------------------- raiz --------------------------
root = ctk.CTk()  # inicializacion raiz
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
root.title("NotiAlarm")  # nombre de ventana


# -------------------------- funcionalidad para boton --------------------------
def button_function():
    print("button pressed")

# def registrarse():


# -------------------------- label --------------------------
label = ctk.CTkLabel(master=root, text="Primera pantalla", font=("Roboto",40))
label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)


# -------------------------- boton --------------------------
btnHeight = 45
btnWidth = 300

btn1 = ctk.CTkButton(master=root, height=btnHeight, width=btnWidth, font=("", 14), text="Registrarse", command=button_function)
btn1.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

btn2 = ctk.CTkButton(master=root, height=btnHeight, width=btnWidth, font=("", 14), text="Iniciar sesión", command=button_function)
btn2.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

root.mainloop()
