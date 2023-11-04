import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os

ctk.set_appearance_mode("dark") # tema oscuro

TAMANO_VENTANA = "1100x650"
BTN_ALTURA = 35
BTN_ANCHO = 290
TITULOS_FUENTE = "Roboto", 34
    
class VentanaOpciones:
    def __init__(self):
        self.root = ctk.CTk() # inicializa
        opciones_universales(self,"NotiAlarm")

        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)

        titulo = ctk.CTkLabel(master=frame, text="NotiAlarm", font=(TITULOS_FUENTE))
        titulo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

        btnRegistro = ctk.CTkButton(master=frame, height=BTN_ALTURA, width=BTN_ANCHO, text="Registrarse", command=self.abrir_ventana_registro) # crea el boton
        btnRegistro.place(relx=0.5, rely=0.4, anchor=tk.CENTER) # lo posiciona en la ventana

        btnLogin = ctk.CTkButton(master=frame, height=BTN_ALTURA, width=BTN_ANCHO, text="Iniciar sesión", command=self.abrir_ventana_login)
        btnLogin.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        btnInvitado = ctk.CTkButton(master=frame, height=BTN_ALTURA, width=BTN_ANCHO, text="Ingresar como invitado", command=self.abrir_ventana_invitado)
        btnInvitado.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        self.root.mainloop() # va al final, abre la ventana

    def abrir_ventana_registro(self): # cierra ventana actual y ejecuta la clase VentanaLogin, se usa en el command de btnRegistro
        self.root.destroy() # cierra la ventana actual
        ventana_registro = VentanaRegistro() # instancia la ventana nueva para que se abra

    def abrir_ventana_login(self):
        self.root.destroy()
        ventana_login = VentanaLogin()

    def abrir_ventana_invitado(self):
        self.root.destroy()
        ventana_invitado = VentanaInvitado()


class VentanaRegistro: # crea la ventana registro
    def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self,"Registrarse")
 
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)

        label = ctk.CTkLabel(master=frame, text="Registrarse", font=(TITULOS_FUENTE))
        label.place(relx=0.5, rely=0.30, anchor=tk.CENTER)

        correo = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Correo electrónico")
        correo.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        nombre = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Usuario")
        nombre.place(relx = 0.5, rely = 0.47, anchor = tk.CENTER)

        contrasena = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, show="*", placeholder_text="Contraseña")
        contrasena.place(relx=0.5, rely=0.54, anchor=tk.CENTER)

        registrar = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Registrarse")
        registrar.place(relx=0.5, rely=0.61, anchor=tk.CENTER)

        volver = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Volver", fg_color="transparent", hover=False, command=self.abrir_ventana_opciones)
        volver.place(relx=0.5, rely=0.68, anchor=tk.CENTER)

        self.root.mainloop()

    def abrir_ventana_opciones(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()


class VentanaLogin: # crea la ventana login
    def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self,"Iniciar sesión")

        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)
        
        titulo = ctk.CTkLabel(master=frame, text="Iniciar sesión", font=(TITULOS_FUENTE))
        titulo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        correo = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Correo electrónico")
        correo.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        contrasena = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Contraseña")
        contrasena.place(relx = 0.5, rely = 0.47, anchor = tk.CENTER)
        
        login = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Iniciar sesión")
        login.place(relx=0.5, rely=0.54, anchor=tk.CENTER)
        
        volver = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Volver", fg_color="transparent", hover=False, command=self.volver)
        volver.place(relx=0.5, rely=0.61, anchor=tk.CENTER)
        
        self.root.mainloop()
    
    def volver(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()


class VentanaInvitado:
     def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self,"Ingresar como invitado")

        self.root.mainloop()


def opciones_universales(self, nombre_ventana):
    self.root.geometry(TAMANO_VENTANA)
    self.root.title(nombre_ventana)
    self.root.resizable(False, False)
    
    currentPath = os.path.dirname(os.path.realpath(__file__))
    imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 650))
    imagenLabel = ctk.CTkLabel(self.root, image=imagenFondo, text="")
    imagenLabel.place(relx=0, rely=0)


ventana_opciones = VentanaOpciones() # abre la ventana principal
