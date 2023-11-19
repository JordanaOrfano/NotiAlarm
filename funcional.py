import json # para trabajar con archivos .json y guardar datos de forma permanente
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from collections import OrderedDict # trabajar con diccionarios ordenados
import os
from datetime import datetime, time
import webbrowser  # para abrir link en denunciaBtn
import time # se usará como temporizador

ctk.set_appearance_mode("dark") # tema oscuro

# diccionarios utilizados en el programa
usuarios = {}
noticias = OrderedDict()
eventos = OrderedDict()

TAMANO_VENTANA = "1100x680"
BTN_ALTURA = 36
BTN_ANCHO = 290
TITULOS_FUENTE = "Roboto", 32
ACCENT_COLOR = ("#a6a6a6","#1e1e1e")

class VentanaOpciones:
    def __init__(self):
        self.root = ctk.CTk() # inicializa
        opciones_universales(self)
     
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)
        
        currentPath = os.path.dirname(os.path.realpath(__file__))
        imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/icon.png"), size=(256, 256))
        imagenLabel = ctk.CTkLabel(master=frame, image=imagenFondo, text="")
        imagenLabel.place(relx=0.245, rely=0.11)

        titulo = ctk.CTkLabel(master=frame, text="¡Bienvenido!", font=(TITULOS_FUENTE))
        titulo.place(relx=0.5, rely=0.59, anchor=tk.CENTER)

        btnRegistro = ctk.CTkButton(master=frame, height=BTN_ALTURA, width=BTN_ANCHO, text="Registrarse", command=self.abrir_ventana_registro) # crea el botón
        btnRegistro.place(relx=0.5, rely=0.71, anchor=tk.CENTER) # lo posiciona en la ventana

        btnLogin = ctk.CTkButton(master=frame, height=BTN_ALTURA, width=BTN_ANCHO, text="Iniciar sesión", command=self.abrir_ventana_login)
        btnLogin.place(relx=0.5, rely=0.78, anchor=tk.CENTER)

        btnInvitado = ctk.CTkButton(master=frame, height=BTN_ALTURA, width=BTN_ANCHO, text="Ingresar como invitado", command=self.abrir_ventana_invitado)
        btnInvitado.place(relx=0.5, rely=0.85, anchor=tk.CENTER)

        self.root.mainloop() # va al final, abre la ventana

    def abrir_ventana_registro(self): # cierra ventana actual y ejecuta la clase VentanaLogin, se usa en el command de btnRegistro
        self.root.destroy() # cierra la ventana actual
        ventana_registro = VentanaRegistro() # instancia la ventana nueva para que se abra

    def abrir_ventana_login(self):
        self.root.destroy()
        ventana_login = VentanaLogin()

    def abrir_ventana_invitado(self):
        self.root.destroy()
        ventana_invitado = VentanaNoticias()


class VentanaRegistro: # crea la ventana registro
    global usuarios
    def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self)

        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)

        label = ctk.CTkLabel(master=frame, text="Registrarse", font=(TITULOS_FUENTE))
        label.pack(pady=(170,30), padx=0)

        self.correo = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Correo electrónico")
        self.correo.pack(pady=(0,10), padx=0)

        self.nombre = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Usuario")
        self.nombre.pack(pady=(0,10), padx=0)

        self.contrasena = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, show="*", placeholder_text="Contraseña")
        self.contrasena.pack(pady=(0,10), padx=0)
        
        frameTerminos = ctk.CTkFrame(master=frame, fg_color="transparent")
        frameTerminos.pack(pady=(0,10), padx=105, fill="x")
        
        self.terminosCheckbox = ctk.CTkCheckBox(master=frameTerminos, width=0, text="", onvalue="on", offvalue="off")
        self.terminosCheckbox.pack(pady=0, padx=0, side="left")
        
        terminosBtn = ctk.CTkButton(master=frameTerminos, width=310, fg_color="transparent", text="Acepto los términos y condiciones", anchor="w", command=self.terminos_condiciones)
        terminosBtn.pack(pady=0, padx=0, fill="x", side="left")

        registrar = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Registrarse", command = lambda: self.registro_evento(frame))
        registrar.pack(pady=(0,10), padx=0)
        
        volver = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Volver", fg_color="transparent", text_color=("#1a1a1a","#ffffff"), hover=False, command=self.abrir_ventana_opciones)
        volver.pack(pady=(0,10), padx=0, fill="x")

        self.root.mainloop()

    def abrir_ventana_opciones(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()

    def comprobar_correo(correo):
        for usuario in usuarios:
            if str(correo.lower()) == str(usuarios[usuario]["correo"].lower()):
                return False
        return True
    
    def registro_evento(self, frame): # al darle click a registrar se iniciara este método, se crea la variable alerta para luego eliminar labels
        if self.nombre.get() not in usuarios: # comprueba que el nombre no exista previamente, si no existe ejecuta
            if len(self.correo.get().strip()) != 0 and len(self.nombre.get().strip()) != 0 and len(self.contrasena.get().strip()) != 0: # chequea que ningún campo este vació
                if "@" in self.correo.get():
                    if VentanaRegistro.comprobar_correo(self.correo.get()):
                        if len(self.contrasena.get()) >= 8 and len(self.contrasena.get()) <20: # comprueba que la contraseña tenga entre 8 y 19 dígitos
                            if any(char.isdigit() for char in self.contrasena.get()): # comprueba que la contraseña tenga al menos un numero
                                if any(char in "!@#$%∧&*(._-)" for char in self.contrasena.get()): # comprueba si la contraseña tiene dígitos especiales
                                    if self.terminosCheckbox.get() == "on":
                                        usuarios[self.nombre.get()] = {"contrasena": self.contrasena.get(), "rol": "usuario", "correo": self.correo.get(), "baneado": False} # de forma predeterminada cualquier usuario nuevo tendrá el rol "usuario", donde no tiene grandes permisos
                                        Sesion.guardar_datos_usuarios()
                                        if hasattr(self, "mensaje"):
                                            self.mensaje.destroy()

                                        self.mensaje = ctk.CTkLabel(master = frame, text = "Usuario creado con éxito, espere unos instantes...")
                                        self.mensaje.place(relx = 0.2, rely = 0.72) 
                                        
                                        self.root.after(3000, self.abrir_ventana_login)
                                        
                                    else:
                                        if hasattr(self, "mensaje"):
                                            self.mensaje.destroy()
                            
                                        self.mensaje = ctk.CTkLabel(master = frame, text = "Debes aceptar los términos y condiciones para usar nuestra aplicación.")
                                        self.mensaje.place(relx = 0.11, rely = 0.72) 
                                else:
                                    
                                    if hasattr(self, "mensaje"):
                                        self.mensaje.destroy()
                            
                                    self.mensaje = ctk.CTkLabel(master = frame, text = "La contraseña debe tener al menos un carácter especial '!@#$%∧&*(._-)'. ")
                                    self.mensaje.place(relx = 0.11, rely = 0.72) 
                            else:
                                
                                if hasattr(self, "mensaje"):
                                    self.mensaje.destroy()

                                self.mensaje = ctk.CTkLabel(master = frame, text = "La contraseña debe tener al menos un número.")
                                self.mensaje.place(relx = 0.23, rely = 0.72) 
                        else:
                            
                            if hasattr(self, "mensaje"):
                                self.mensaje.destroy()

                            self.mensaje = ctk.CTkLabel(master = frame, text = "La contraseña debe tener entre 8 y 20 caracteres.")
                            self.mensaje.place(relx = 0.22, rely = 0.72) 
                    else:
                        
                        if hasattr(self, "mensaje"):
                            self.mensaje.destroy()

                        self.mensaje = ctk.CTkLabel(master = frame, text = "El correo electrónico ya está asociado a una cuenta.")
                        self.mensaje.place(relx = 0.22, rely = 0.72) 
                else:
                    
                    if hasattr(self, "mensaje"):
                        self.mensaje.destroy()

                    self.mensaje = ctk.CTkLabel(master = frame, text = "Ingrese un correo electrónico válido.")
                    self.mensaje.place(relx = 0.30, rely = 0.72) 
            else:
                
                if hasattr(self, "mensaje"):
                    self.mensaje.destroy()

                self.mensaje = ctk.CTkLabel(master = frame, text = "Ningún campo debería estar vacío.")
                self.mensaje.place(relx = 0.30, rely = 0.72)
        else:
            
            if hasattr(self, "mensaje"):
                self.mensaje.destroy()

            self.mensaje = ctk.CTkLabel(master = frame, text = "El nombre de usuario ya existe.")
            self.mensaje.place(relx = 0.32, rely = 0.72) 
    
    def terminos_condiciones(self):
        terminosVentana = ctk.CTkToplevel(master=self.root)
        terminosVentana.title("NotiAlarm | Términos y condiciones")
        centrar_ventana(terminosVentana, "600", "400")
        NotiAlarm_icono(terminosVentana)
        # terminosVentana.geometry("600x400+500+240")
        terminosVentana.resizable(False, False)
        terminosVentana.attributes("-topmost", "true")
        
        terminosLabel = ctk.CTkLabel(master=terminosVentana, font=('', 24), text="Términos y condiciones")
        terminosLabel.pack(pady=20, padx=0, fill="x")
        
        frame = ctk.CTkScrollableFrame(master=terminosVentana)
        frame.pack(pady=0, padx=30, fill="both", expand=True)
        
        terminosTxt = "\nBases y Condiciones del Software de NotiAlarm.\n\nParticipación:\nEl software está disponible para la participación de residentes locales interesados en compartir noticias de seguridad e informar sobre eventos locales relevantes. La participación es voluntaria y abierta a personas mayores de 18 años.\n\nContenido:\nSe invita a los usuarios a subir noticias relacionadas con la seguridad en la zona, incluyendo incidentes de inseguridad, medidas preventivas y eventos locales de interés comunitario.\n\nVeracidad de la Información:\nLos participantes deben proporcionar información veraz y corroborada en la medida de lo posible. La difusión de información falsa puede resultar en la exclusión del usuario del software.\n\nRespeto y Ética:\nSe prohíbe la publicación de contenido difamatorio, ofensivo o que viole los derechos de privacidad de terceros. El respeto y la ética son fundamentales para mantener un ambiente colaborativo y seguro.\n\nConfidencialidad:\nLos usuarios deben ser conscientes de no compartir información que viole la privacidad de otras personas o comprometa la seguridad de la comunidad.\n\nUso Responsable:\nEl software se proporciona con el propósito de mejorar la seguridad y la conciencia comunitaria. Su uso debe ser responsable y respetuoso. Cualquier mal uso del software puede resultar en la desactivación de la cuenta del usuario.\n\nPropiedad Intelectual:\nLos usuarios conservan los derechos de propiedad intelectual sobre el contenido que suben al software. Al subir contenido, los usuarios otorgan una licencia no exclusiva para su uso en la plataforma.\n\nColaboración Comunitaria:\nSe fomenta la colaboración y el intercambio constructivo de información entre los usuarios. La plataforma se reserva el derecho de moderar y eliminar contenido que viole las normas de colaboración.\n\nDuración:\nEl uso del software no tiene limitaciones de tiempo y estará sujeto a revisiones periódicas para garantizar su eficacia y cumplimiento de normas.\n"
        
        terminosTexto = ctk.CTkLabel(master=frame, wraplength=500, justify="left", text=terminosTxt)
        terminosTexto.pack(pady=0, padx=0, fill="x")
        
        terminosLabel = ctk.CTkLabel(master=terminosVentana, justify="left", wraplength=550, text="Al utilizar este software, los usuarios aceptan adherirse a estas bases y condiciones. La plataforma se reserva el derecho de modificar estas condiciones con notificación previa a los usuarios.")
        terminosLabel.pack(pady=20, padx=0, fill="x")

    def abrir_ventana_login(self):
        # Código para abrir la ventana de login
        self.root.destroy()
        ventana_opciones = VentanaLogin() 

usuario_actual = "desconocido"

class VentanaLogin: # crea la ventana login
    global usuarios
    def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self)

        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)
        
        titulo = ctk.CTkLabel(master=frame, text="Iniciar sesión", font=(TITULOS_FUENTE))
        titulo.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        self.correo = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Correo electrónico")
        self.correo.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.contrasena = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Contraseña", show="*")
        self.contrasena.place(relx = 0.5, rely = 0.47, anchor = tk.CENTER)
        
        login = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Iniciar sesión", command = lambda: self.login_evento(frame))
        login.place(relx=0.5, rely=0.54, anchor=tk.CENTER)
        
        volver = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Volver", fg_color="transparent", text_color=("#1a1a1a","#ffffff"), hover=False, command=self.volver)
        volver.place(relx=0.5, rely=0.61, anchor=tk.CENTER)
        
        self.root.mainloop()
    
    def volver(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()

    def login_evento(self, frame): # al tocar el botón login
        global usuario_actual
        verificar = False # por ahora, la contraseña no coincide; valor predeterminado

        for usuario in usuarios: # verifica si algún correo en el diccionario usuarios coincide con el ingresado
            if self.correo.get().lower().strip() == usuarios[usuario]['correo'].lower().strip():
                    if str(self.contrasena.get()) == str(usuarios[usuario]['contrasena']): # si encuentra un correo que coincide con el ingresado, comprueba que también coincida la contraseña
                        verificar = True # el correo y la contraseña coinciden
                        usuario_actual = usuario
                        break


        if verificar:
            if not usuarios[usuario]["baneado"]:
                if hasattr(self, "mensaje"):
                    self.mensaje.destroy()
                self.mensaje = ctk.CTkLabel(master = frame, text = "Iniciando Sesión...")
                self.mensaje.place(relx = 0.39, rely = 0.65)
                
                if usuarios[usuario]["rol"] == "usuario": # tiene el rol de usuario
                    self.root.after(3000, self.abrir_ventana_usuario)
                else:
                    self.root.after(3000, self.abrir_ventana_admin)

            else:
                if hasattr(self, "mensaje"):
                    self.mensaje.destroy()
                self.mensaje = ctk.CTkLabel(master = frame, text = "El usuario se encuentra baneado permanentemente.", text_color="red", font=('', 14))
                self.mensaje.place(relx = 0.2, rely = 0.65)
            
        else:
            if hasattr(self, "mensaje"):
                self.mensaje.destroy()
            self.mensaje = ctk.CTkLabel(master = frame, text = "Correo o contraseña inválidos.")
            self.mensaje.place(relx = 0.32, rely = 0.65) 

    def abrir_ventana_usuario(self):
        self.root.destroy() # destruye la ventana actual
        ventana_noticias = VentanaNoticias() # abre la ventana principal

    def abrir_ventana_admin(self):
        self.root.destroy() # destruye la ventana actual
        ventana_admin = VentanaAdmin() # tiene el rol de administrador
        

class VentanaNoticias:
    def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self)
        
        frame = ctk.CTkScrollableFrame(master=self.root)
        frame.pack(pady=0, padx=260, fill="both", expand=True)
        
        # ------------------- side frames -------------------
        # side frame izquierdo
        sideFrame1 = ctk.CTkFrame(master=self.root, width=240)
        sideFrame1.place(relx=0, rely=0, relheight=1)
        sideFrame1.pack_propagate(False)

        cerrarSesionLabel = ctk.CTkLabel(master=sideFrame1, text="Cerrar sesión", font=("",16,"bold"))
        cerrarSesionLabel.pack(pady=(30,0), padx=20, fill="x")
        
        volver = ctk.CTkButton(master=sideFrame1, text="<  Volver", command=self.volver)
        volver.pack(pady=10, padx=20, fill="x")
        
        denunciaLabel = ctk.CTkLabel(master=sideFrame1, text="¿Sabías que podés realizar tu denuncia de forma virtual?", wraplength=210, font=("",16,"bold"))
        denunciaLabel.pack(pady=(90,10), padx=20, fill="x")
        
        denunciaBtn = ctk.CTkButton(master=sideFrame1, text="seguridad.gba.gob.ar", command=self.abrir_link)
        denunciaBtn.pack(pady=(0), padx=20, fill="x")

        infoLabel = ctk.CTkLabel(master=sideFrame1, text="Información", justify="left", anchor="w", font=("",16,"bold"))
        infoLabel.pack(pady=(90,0), padx=66, fill="x")
        
        numEmergencia = ctk.CTkLabel(master=sideFrame1, text="911 | Policía\n100 | Bomberos\n107 | Ambulancia", justify="left", anchor="w", wraplength=205, font=("",13,"bold"))
        numEmergencia.pack(pady=0, padx=66, fill="x")

        activarAlarmaBtn = ctk.CTkButton(master=sideFrame1, text="Enviar alarma", command=lambda: self.comprobar_alarma(seleccionAlarma.get(), sideFrame1))
        activarAlarmaBtn.pack(pady=(10,30), padx=20, fill="x", side="bottom")

        seleccionAlarma = ctk.CTkOptionMenu(master=sideFrame1, values=["Elija una opción", "Robo", "Emergencia Medica", "Incendio"])
        seleccionAlarma.pack(pady=(10,0), padx=20, fill="x", side="bottom")
        
        alarmaLabel = ctk.CTkLabel(master=sideFrame1, text="Iniciar alarma", font=("",16,"bold"))
        alarmaLabel.pack(pady=(0,0), padx=20, fill="x", side="bottom")
        
        # side frame derecho
        sideFrame2 = ctk.CTkFrame(master=self.root, width=240)
        sideFrame2.place(relx=0.782, rely=0, relheight=1)
        sideFrame2.pack_propagate(False)
        
        cambiarAparienciaLabel = ctk.CTkLabel(master=sideFrame2, text="Cambiar apariencia", font=("",16,"bold"))
        cambiarAparienciaLabel.pack(pady=(30,10), padx=20, fill="x", side="top")
        
        cambiarAparienciaBtn = ctk.CTkOptionMenu(master=sideFrame2, values=["Dark", "Light"], command=self.cambiar_apariencia)
        cambiarAparienciaBtn.pack(pady=(0,30), padx=20, fill="x", side="top")
        
        sideFrame2Titulo = ctk.CTkLabel(master=sideFrame2, text="Eventos locales", font=("",16,"bold"))
        sideFrame2Titulo.pack(pady=0, padx=20, fill="x")
        
        sideFrame2Eventos = ctk.CTkScrollableFrame(master=sideFrame2, fg_color="transparent", scrollbar_button_color=("#dbdbdb","#2b2b2b"))
        sideFrame2Eventos.pack(pady=(0,20), fill="both", expand=True)
        
        # mostrar todos los eventos en el menú
        try:
            mostradas = 0
            if len(eventos) != 0:
                for titulo, det in reversed(eventos.items()):
                    if eventos[titulo]["mostrar"]: 
                        ubicacion = det["ubicacion"]
                        fecha = det["fecha"]
                        hora = det["hora"]
                        autor = det["autor"]
                        self.mostrar_evento(sideFrame2Eventos, titulo, ubicacion, fecha, hora, autor)
                        mostradas += 1
            else:
                ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack()
                mostradas += 1 
            if mostradas == 0:
                ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack() 
        except:
            ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack() 
        
        # -------------------- publicar -------------------
        notialarmLogo(frame, "NotiAlarm", 170)
        
        crearFrame = ctk.CTkFrame(master=frame)
        crearFrame.pack(pady=(0,10), padx=20, fill="x")
        
        crearLabel = ctk.CTkLabel(master=crearFrame, wraplength=520, height=40, font=("",14,"bold"), fg_color=ACCENT_COLOR, corner_radius=6, text="Crear publicación")
        crearLabel.pack(pady=0, padx=0, fill="x")
        
        crearAlarmaBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar noticia", command=self.publicar_noticia)
        crearAlarmaBtn.pack(pady=0, padx=0, fill="x", side="left")
        
        noticiaEventoBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar evento", command=self.Evento)
        noticiaEventoBtn.pack(pady=0, padx=0, fill="x", side="right")
       
        # mostrar todas las noticias en el menú 
        try:
            mostradas = 0 
            if len(noticias) != 0:
                for titulo, det in reversed(noticias.items()):
                    if noticias[titulo]["mostrar"]: 
                        ubicacion = det["ubicacion"]
                        texto = det["contenido"]
                        usuario = det["autor"]
                        fecha = det["fecha"]
                        categoria = noticias[titulo]["categoria"] 
                        self.mostrar_publicacion(frame, titulo, ubicacion, categoria, texto, usuario, fecha)
                        mostradas += 1

            else:
                ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack()
                mostradas += 1 

            if mostradas == 0:
                ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack() 
        except:
            ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack() 
        
        self.root.mainloop()

    def abrir_link(self):
        webbrowser.open_new("https://www.seguridad.gba.gob.ar/#/home")

    def comprobar_alarma(self, opcion, sideFrame1):
        print(opcion)
        if opcion=="Elija una opción":
            if hasattr(self, "errorOpcion"):
                self.errorOpcion.destroy()
            usuarios["alerta"] = {"valor": True, "correo": "x", "baneado": False}
            Sesion.guardar_datos_usuarios()
            Sesion.cargar_datos_usuarios()
            self.errorOpcion = ctk.CTkLabel(master = sideFrame1, text = "Debe elegir una opcion")
            self.errorOpcion.pack(fill="x",pady=0)
            #.place(relx=0.2, rely=0.1, fill="x") 
            #errorOpcion = ctk.CTkLabel(master=sideFrame1, text="Debe elegir una opción", font=("",16,"bold")).pack()

    def activar_alarma(self):
        # iterar sobre cada usuario y enviar un mensaje
        for usuario in usuarios:
            if usuario == "alarma":
                if usuario["valor"]:
                    # muestra mensaje

                    # cambia el valor
                    usuario["valor"] = False
                    pass
                    # si es true lanza mensaje
                else:
                    pass
                    # no lanza mensaje
        
            mensaje = f"¡ALERTA! La alarma ha sido activada. Por favor, toma las precauciones necesarias."

            print(f"Mensaje enviado a {usuarios[usuario]}: {mensaje}")

            # mostrar el mensaje en la interfaz de usuario del remitente
        self.mostrar_mensaje(usuarios[usuario], mensaje)
    
        #self.root=VentanaAlerta()

    def mostrar_mensaje(self, usuario, mensaje):
        # crear una nueva ventana para mostrar el mensaje
        ventana_mensaje = ctk.CTkToplevel()
        ventana_mensaje.title(f"Mensaje para {usuario}")
        ventana_mensaje.attributes("-topmost", "true")

        # etiqueta con el mensaje
        etiqueta_mensaje = ctk.CTkLabel(master=ventana_mensaje, text=mensaje, padx=20, pady=20)
        etiqueta_mensaje.pack()

    def cambiar_apariencia(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def publicar_noticia(self): 
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm | Crear noticia")
        centrar_ventana(publicarVentana, "650", "435")
        NotiAlarm_icono(publicarVentana)
        # publicarVentana.geometry("650x435+500+240")
        publicarVentana.resizable(False, False)
        publicarVentana.attributes("-topmost", "true")
        
        currentPath = os.path.dirname(os.path.realpath(__file__))
        imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 680))
        imagenLabel = ctk.CTkLabel(publicarVentana, image=imagenFondo, text="")
        imagenLabel.place(relx=0, rely=0)
        
        publicarFrame = ctk.CTkFrame(master=publicarVentana)
        publicarFrame.pack(pady=0, padx=90, fill="both", expand=True)
        
        publicarLabel = ctk.CTkLabel(master=publicarFrame, height=40,font=('Roboto', 24), text="Crear publicación | Noticia")
        publicarLabel.pack(pady=(20,15), padx=20, fill="x")
        
        self.publicarTitulo = ctk.CTkEntry(master=publicarFrame, height=BTN_ALTURA, placeholder_text="Título")
        self.publicarTitulo.pack(pady=5, padx=20, fill="x")
        
        self.publicarUbicacion = ctk.CTkEntry(master=publicarFrame, height=BTN_ALTURA, placeholder_text="Ubicación")
        self.publicarUbicacion.pack(pady=5, padx=20, fill="x")
        
        self.publicarTextbox = ctk.CTkTextbox(master=publicarFrame, height=140)
        self.publicarTextbox.pack(pady=5, padx=20, fill="x")

        self.categoria = ctk.CTkOptionMenu(master=publicarFrame, values=["Categoria", "Robo", "Accidentes", "Asesinatos", "Eventos Locales", "Trafico", "Incendios y Rescates", "Eventos de emergencia", "Obras Publicas", "Otras"])
        self.categoria.pack(pady=5, padx=20, fill="x")
        
        publicarBoton = ctk.CTkButton(master=publicarFrame, height=BTN_ALTURA, text="Publicar", command=lambda: self.publicar_evento(publicarFrame))
        publicarBoton.pack(pady=5, padx=20, fill="x")

    # al tocar el botón de publicar deberá guardar la noticia en el json.
    def publicar_evento(self, publicarFrame):
        global noticias
        global usuarios_actual
        if self.publicarTitulo.get() not in noticias:
            if len(self.publicarTitulo.get().strip()) != 0 and len(self.publicarUbicacion.get().strip()) != 0 and len(self.publicarTextbox.get("1.0", "end").strip()) != 0:
                if len(self.publicarTitulo.get()) < 68:
                    if len(self.publicarUbicacion.get()) <= 30:
                        if len(self.publicarTextbox.get("1.0", "end"))  <= 600:
                            if self.categoria.get().lower() != "categoria":

                                if hasattr(self, "info_evento"):
                                    self.info_evento.destroy()
                                    
                                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Noticia creada correctamente.")
                                self.info_evento.pack()
                                fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
                                noticias[self.publicarTitulo.get()] = {"contenido": self.publicarTextbox.get("1.0", "end"),
                                                            "autor": usuario_actual,
                                                            "ubicacion": self.publicarUbicacion.get(),
                                                            "mostrar": False,
                                                            "categoria": self.categoria.get(),
                                                            "fecha": fecha_actual} #Atributos de las noticias
                                Sesion.guardar_datos_noticias()

                            else:
                                if hasattr(self, "info_evento"):
                                    self.info_evento.destroy()
                                
                                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Seleccione una categoría.")
                                self.info_evento.pack()
                        else:
                            if hasattr(self, "info_evento"):
                                self.info_evento.destroy()
                        
                            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La descripción debe tener menos de 500 caracteres.")
                            self.info_evento.pack() 
                    else:
                        if hasattr(self, "info_evento"):
                            self.info_evento.destroy()
                        
                        self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La ubicación debe tener menos de 30 caracteres.")
                        self.info_evento.pack() 
                else:
                    if hasattr(self, "info_evento"):
                            self.info_evento.destroy()
                        
                    self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "El título debe de tener menos de 70 caracteres.")
                    self.info_evento.pack() 
            else:
                if hasattr(self, "info_evento"):
                            self.info_evento.destroy()

                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ningún espacio puede estar vacío.")
                self.info_evento.pack()
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()

            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ya existe una noticia con el mismo título.")
            self.info_evento.pack()       
    
    def Evento(self):
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm | Crear evento")
        centrar_ventana(publicarVentana, "650", "290")
        NotiAlarm_icono(publicarVentana)
        # publicarVentana.geometry("650x290+500+240")
        publicarVentana.resizable(False, False)  
        publicarVentana.attributes("-topmost", "true")      
        
        currentPath = os.path.dirname(os.path.realpath(__file__))
        imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 680))
        imagenLabel = ctk.CTkLabel(publicarVentana, image=imagenFondo, text="")
        imagenLabel.place(relx=0, rely=0)
        
        publicarFrame = ctk.CTkFrame(master=publicarVentana)
        publicarFrame.pack(pady=0, padx=90, fill="both", expand=True)
        
        publicarLabel = ctk.CTkLabel(master=publicarFrame, height=40,font=('Roboto', 24), text="Crear Publicación | Evento")
        publicarLabel.pack(pady=(20,15), padx=20, fill="x")
        
        self.publicarTitulo = ctk.CTkEntry(master=publicarFrame, height=BTN_ALTURA, placeholder_text="Título")
        self.publicarTitulo.pack(pady=5, padx=20, fill="x")
        
        self.publicarUbicacion = ctk.CTkEntry(master=publicarFrame, height=BTN_ALTURA, placeholder_text="Ubicación")
        self.publicarUbicacion.pack(pady=5, padx=20, fill="x")

        fechaFrame = ctk.CTkFrame(master=publicarFrame, fg_color="transparent")
        fechaFrame.pack(pady=0, padx=20, fill="x")
        
        self.publicarFecha = ctk.CTkEntry(master=fechaFrame, width=211, height=BTN_ALTURA, placeholder_text="Fecha (dd/mm/aa)")
        self.publicarFecha.pack(pady=5, padx=0, fill="x", side="left")

        self.publicarHora = ctk.CTkEntry(master=fechaFrame, width=211, height=BTN_ALTURA, placeholder_text="Hora (hh:mm)")
        self.publicarHora.pack(pady=5, padx=0, fill="x", side="right")
        
        publicarBoton = ctk.CTkButton(master=publicarFrame, height=BTN_ALTURA, text="Publicar", command= lambda: self.evento_pulsar(publicarFrame))
        publicarBoton.pack(pady=5, padx=20, fill="x")
    
    def evento_pulsar(self, publicarFrame):
        global eventos
        global usuario_actual
        if self.publicarTitulo.get() not in eventos:
            if len(self.publicarTitulo.get().strip()) != 0 and len(self.publicarUbicacion.get().strip()) and len(self.publicarFecha.get().strip()) != 0 and len(self.publicarHora.get().strip()) != 0:
                if len(self.publicarTitulo.get()) <= 22:
                    if len(self.publicarUbicacion.get()) <= 22:
                        fecha = VentanaNoticias.es_fecha_valida(self.publicarFecha.get())
                        if fecha is not None and fecha > datetime.now():
                            hora = VentanaNoticias.es_hora_valida(self.publicarHora.get())
                            if hora is not None:
                                fecha = fecha.strftime( "%d/%m/%Y") # lo pasa nuevamente a una fecha texto para guardarla correctamente en un json y que no de error
                                hora = hora.strftime( '%M/%H')
                                eventos[self.publicarTitulo.get()] = {"ubicacion": self.publicarUbicacion.get(),
                                                                    "fecha": self.publicarFecha.get(),
                                                                    "hora": self.publicarHora.get(),
                                                                    "mostrar": False,
                                                                    "autor": usuario_actual}
                                Sesion.guardar_datos_eventos()
                                if hasattr(self, "info_evento"):
                                    self.info_evento.destroy()

                                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Evento Publicado.")
                                self.info_evento.pack() 
                            else:
                                if hasattr(self, "info_evento"):
                                    self.info_evento.destroy()

                                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La hora ingresada no es valida.")
                                self.info_evento.pack() 
                        else:
                            if hasattr(self, "info_evento"):
                                self.info_evento.destroy()

                            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La fecha ingresada no es valida.")
                            self.info_evento.pack()
                    else:
                        if hasattr(self, "info_evento"):
                            self.info_evento.destroy()

                        self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La ubicacion debe tener menos de 20 caracteres.")
                        self.info_evento.pack()  
                else:
                    if hasattr(self, "info_evento"):
                        self.info_evento.destroy()

                    self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "El titulo debe tener menos de 20 caracteres.")
                    self.info_evento.pack()
            else:
                if hasattr(self, "info_evento"):
                    self.info_evento.destroy()

                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ningún campo puede estar vació.")
                self.info_evento.pack()  
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()

            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ya existe un evento con el mismo titulo.")
            self.info_evento.pack() 

    # necesitamos comprobar si la hora ingresada es valida
    def es_hora_valida(hora):
        try:
            hora = datetime.strptime(hora,"%H:%M").time()
            
            if 0 <= hora.hour < 24 and 0 <= hora.minute < 60:
                return hora
            else:
                return None
        except:
            return None
        
    # comprueba si la fecha es valida
    def es_fecha_valida(fecha):
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y")
            return fecha
        except:
            return None

    def mostrar_publicacion(self, frame, titulo, ubicacion, categoria, texto, usuario, fecha): # creación de publicación
        noticiaFrame = ctk.CTkFrame(master=frame, fg_color=("#cccccc","#262626"))
        noticiaFrame.pack(pady=10, padx=20, fill="x")
        
        noticiaTitulo = ctk.CTkLabel(master=noticiaFrame, fg_color=ACCENT_COLOR, wraplength=520, height=40, corner_radius=6, font=("",14,"bold"), text=titulo)
        noticiaTitulo.pack(pady=0, padx=0, fill="x")
        
        noticiaTexto = ctk.CTkLabel(master=noticiaFrame, justify="left", anchor="w", wraplength=482, text=f"Ubicación: {ubicacion}\n\nCategoría: {categoria}\n\n{texto}")
        noticiaTexto.pack(pady=14, padx=20, fill="x", expand=True)
        
        noticiaInfoFrame = ctk.CTkFrame(master=noticiaFrame, fg_color=ACCENT_COLOR, corner_radius=6)
        noticiaInfoFrame.pack(pady=0, padx=0, fill="x")

        noticiaInfo = ctk.CTkLabel(master=noticiaInfoFrame, justify="left", anchor="w", corner_radius=6, wraplength=520, text=f"{usuario}\n{fecha}")
        noticiaInfo.pack(pady=0, padx=20, side="left")
        
        if usuario == usuario_actual:
            noticiaBorrar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Borrar")
            noticiaBorrar.pack(pady=0, padx=0, side="right")

            noticiaEditar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Editar")
            noticiaEditar.pack(pady=0, padx=1, side="right")
    
    def mostrar_evento(self, frame, titulo, ubicacion, fecha, hora, autor):
        eventoTitulo = ctk.CTkLabel(master=frame, text=f"{titulo} \n{ubicacion}\n{fecha} | {hora}\n{autor}", justify="left", anchor="w", wraplength=180, font=("",13,"bold"))
        eventoTitulo.pack(pady=10, padx=20, fill="x")
    
    def volver(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()


class VentanaAdmin(VentanaNoticias):
    def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self)
        
        frame = ctk.CTkScrollableFrame(master=self.root)
        frame.pack(pady=0, padx=260, fill="both", expand=True)
        
        # side frame izquierdo
        sideFrame1 = ctk.CTkFrame(master=self.root, width=240)
        sideFrame1.place(relx=0, rely=0, relheight=1)
        sideFrame1.pack_propagate(False)

        cerrarSesionLabel = ctk.CTkLabel(master=sideFrame1, text="Cerrar sesión", font=("",16,"bold"))
        cerrarSesionLabel.pack(pady=(30,0), padx=20, fill="x")
        
        volver = ctk.CTkButton(master=sideFrame1, text="<  Volver", command=self.volver)
        volver.pack(pady=10, padx=20, fill="x")

        cambiarAparienciaBtn = ctk.CTkOptionMenu(master=sideFrame1, values=["Dark", "Light"], command=self.cambiar_apariencia)
        cambiarAparienciaBtn.pack(pady=(10,30), padx=20, fill="x", side="bottom")
        
        cambiarAparienciaLabel = ctk.CTkLabel(master=sideFrame1, text="Cambiar apariencia", font=("",16,"bold"))
        cambiarAparienciaLabel.pack(pady=0, padx=20, fill="x", side="bottom")
        
        # side frame derecho
        sideFrame2Eventos = ctk.CTkFrame(master=self.root, width=240)
        sideFrame2Eventos.place(relx=0.782, rely=0, relheight=1)
        sideFrame2Eventos.pack_propagate(False)
        
        sideFrame2Titulo = ctk.CTkLabel(master=sideFrame2Eventos, text="Eventos locales", font=("",16,"bold"))
        sideFrame2Titulo.pack(pady=(30,20), padx=20, fill="x")
        
        sideFrame2Eventos = ctk.CTkScrollableFrame(master=sideFrame2Eventos, fg_color="transparent")
        sideFrame2Eventos.pack(pady=(0,20), fill="both", expand=True)
        
        # mostrar todos los eventos en el menú
        try:
            mostradas = 0
            if len(eventos) != 0:
                for titulo, det in reversed(eventos.items()):
                    if eventos[titulo]["mostrar"] == False: 
                        ubicacion = det["ubicacion"]
                        fecha = det["fecha"]
                        hora = det["hora"]
                        autor = det["autor"]
                        self.mostrar_evento(sideFrame2Eventos, titulo, ubicacion, fecha, hora, autor)
                        mostradas += 1
            else:
                ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack()
                mostradas += 1 
            if mostradas == 0:
                ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack() 
        except:
            ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack() 
        
        
        # frame principal
        notialarmLogo(frame, "NotiAlarm - Admin", 110)
        
        administrarLabel = ctk.CTkLabel(master=frame, wraplength=520, height=40, font=("",14,"bold"), fg_color=ACCENT_COLOR, corner_radius=6, text="Administrar Publicaciones")
        administrarLabel.pack(pady=5, padx=20, fill="x")
        
        # mostrar todas las noticias en el menú
        try:
            mostradas = 0 
            if len(noticias) != 0:
                for titulo, det in reversed(noticias.items()):
                    if noticias[titulo]["mostrar"] == False: 
                        ubicacion = det["ubicacion"]
                        texto = det["contenido"]
                        usuario = det["autor"]
                        fecha = det["fecha"]
                        categoria = noticias[titulo]["categoria"] 
                        self.mostrar_publicacion(frame, titulo, ubicacion, categoria, texto, usuario, fecha)
                        mostradas += 1

            else:
                ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack()
                mostradas += 1 

            if mostradas == 0:
                ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack() 
        except:
            ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack() 
        
        self.root.mainloop()
    
    def mostrar_publicacion(self, frame, titulo, ubicacion, categoria, texto, usuario, fecha): # creación de publicación
        noticiaFrame = ctk.CTkFrame(master=frame, fg_color=("#cccccc","#262626"))
        noticiaFrame.pack(pady=10, padx=20, fill="x")
        
        noticiaTitulo = ctk.CTkLabel(master=noticiaFrame, fg_color=ACCENT_COLOR, wraplength=520, height=40, corner_radius=6, font=("",14,"bold"), text=titulo)
        noticiaTitulo.pack(pady=0, padx=0, fill="x")
        
        noticiaTexto = ctk.CTkLabel(master=noticiaFrame, justify="left", anchor="w", wraplength=482, text=f"Ubicación: {ubicacion}\n\nCategoría: {categoria}\n\n{texto}")
        noticiaTexto.pack(pady=14, padx=20, fill="x", expand=True)
        
        noticiaInfoFrame = ctk.CTkFrame(master=noticiaFrame, fg_color=ACCENT_COLOR, corner_radius=6)
        noticiaInfoFrame.pack(pady=0, padx=0, fill="x")

        noticiaInfo = ctk.CTkLabel(master=noticiaInfoFrame, justify="left", anchor="w", corner_radius=6, wraplength=520, text=f"{usuario}\n{fecha}")
        noticiaInfo.pack(pady=0, padx=20, side="left")

        noticiaPublicar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Publicar", command=lambda: self.AceptarNoticia(titulo, noticiaFrame))
        noticiaPublicar.pack(pady=0, padx=0, side="right")
        
        noticiaBorrar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Rechazar", command=lambda: self.RechazarNoticia(titulo, noticiaFrame))
        noticiaBorrar.pack(pady=0, padx=(1,0), side="right")
        
        noticiaBanearUsuario = ctk.CTkButton(master=noticiaInfoFrame, width=100, height=40, text="Banear usuario", command=lambda: self.confirmar_banear(usuario))
        noticiaBanearUsuario.pack(pady=0, padx=0, side="right")
        
    def confirmar_banear(self, usuario):
        confirmarToplevel = ctk.CTkToplevel(master=self.root)
        confirmarToplevel.title("NotiAlarm | Banear usuario")
        centrar_ventana(confirmarToplevel, "470", "180")
        NotiAlarm_icono(confirmarToplevel)
        # confirmarToplevel.geometry("470x180+500+240")
        confirmarToplevel.resizable(False, False)
        confirmarToplevel.attributes("-topmost", "true")
        
        banearLabel = ctk.CTkLabel(master=confirmarToplevel, height=40, font=("", 18), text=f"¿Está seguro que desea banear a {usuario}?")
        banearLabel.pack(pady=(40,0), padx=30, fill="x")
        
        btnCancelar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Cancelar", command=confirmarToplevel.destroy)
        btnCancelar.pack(pady=(0,40), padx=(70,0), side="left")
        
        btnAceptar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Aceptar", command=lambda: self.BanearUsuario(usuario, confirmarToplevel))
        btnAceptar.pack(pady=(0,40), padx=(0,70), side="right")
        
    def mostrar_evento(self, frame, titulo, ubicacion, fecha, hora, autor):
        eventoFrame = ctk.CTkFrame(master=frame, fg_color=("#cccccc","#333333"))
        eventoFrame.pack(pady=5, padx=0, fill="x")
        
        eventoTitulo = ctk.CTkLabel(master=eventoFrame, text=f"{titulo} \n{ubicacion}\n{fecha} | {hora}\n{autor}", justify="left", anchor="w", wraplength=180, font=("",13,"bold"))
        eventoTitulo.pack(pady=10, padx=20, fill="x")
        
        btnBorrar = ctk.CTkButton(master=eventoFrame, width=119, text="Rechazar", command=lambda: self.RechazarEvento(titulo, eventoFrame))
        btnBorrar.pack(pady=0, padx=0, side="left")
        
        btnPublicar = ctk.CTkButton(master=eventoFrame, width=119, text="Publicar", command=lambda: self.AceptarEvento(titulo, eventoFrame))
        btnPublicar.pack(pady=0, padx=0, side="right")

    # publica la noticia seleccionada
    def AceptarNoticia(self, titulo, noticiaFrame):
        global noticias
        try:
            noticias[titulo]["mostrar"] = True
            Sesion.guardar_datos_noticias()
            Sesion.cargar_datos_noticias()

            noticiaFrame.destroy()
        except:
            print("La noticia ya fue aceptada.")

    # rechaza la noticia 
    def RechazarNoticia(self, titulo, noticiaFrame):
        global noticias
        try:
            del noticias[titulo]
            Sesion.guardar_datos_noticias()
            Sesion.cargar_datos_noticias()
            
            noticiaFrame.destroy()
        except:
            print("La noticia ya fue rechazada.")

    # publica el evento seleccionado
    def AceptarEvento(self, titulo, eventoFrame):
        global eventos
        try:
            eventos[titulo]["mostrar"] = True
            Sesion.guardar_datos_eventos()
            Sesion.cargar_datos_eventos()
            
            eventoFrame.destroy()
        except:
            print("El evento ya fue aceptado.")

    # rechaza el evento
    def RechazarEvento(self, titulo, eventoFrame):
        global eventos
        try:
            del eventos[titulo]
            Sesion.guardar_datos_eventos()
            Sesion.cargar_datos_eventos()
            
            eventoFrame.destroy()
        except:
            print("El evento ya fue rechazado.")

    # banea usuario que publico la noticia
    def BanearUsuario(self, usuario, confirmarToplevel):
        global usuarios
        try:
            usuarios[usuario]["baneado"] = True
            Sesion.guardar_datos_usuarios()
            Sesion.cargar_datos_usuarios()
            confirmarToplevel.destroy()
        except:
            print("Usuario no encontrado.") 

def opciones_universales(self):
    # self.root.geometry("1100x680+350+240")
    NotiAlarm_icono(self.root)
    centrar_ventana(self.root, "1100", "680")
    self.root.title("NotiAlarm")
    self.root.resizable(False, False)
    
    currentPath = os.path.dirname(os.path.realpath(__file__))
    imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 680))
    imagenLabel = ctk.CTkLabel(self.root, image=imagenFondo, text="")
    imagenLabel.place(relx=0, rely=0)

def centrar_ventana(ventana, ancho, alto):

    # obten el ancho y el alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # calcula las coordenadas para centrar la ventana
    x = (ancho_pantalla - int(ancho)) // 2
    y = (alto_pantalla - int(alto)) // 2

    # establece el tamaño y posicion de la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def NotiAlarm_icono(ventana):
    carpeta_principal = os.path.dirname(__file__)
    carpeta_imagenes = os.path.join(carpeta_principal, "img")
    ventana.iconbitmap(os.path.join(carpeta_imagenes, "ventana.ico"))

def notialarmLogo(frame, texto, padLeft):
    tituloFrame = ctk.CTkFrame(master=frame)
    tituloFrame.pack(pady=0, padx=(padLeft,20), fill="x")
    
    currentPath = os.path.dirname(os.path.realpath(__file__))
    imagenIcono = ctk.CTkImage(Image.open(currentPath + "/img/icon.png"), size=(50, 50))
    imagenLabel = ctk.CTkLabel(tituloFrame, image=imagenIcono, text="")
    imagenLabel.pack(side="left")
    
    titulo = ctk.CTkLabel(master=tituloFrame, text=texto, justify="left", anchor="w", font=(TITULOS_FUENTE))
    titulo.pack(pady=20, padx=20, fill="x", side="left")


class Sesion: # maneja los datos se sesión 
    def cargar_datos_usuarios(): #Carga el archivo anterior con los usuarios existentes.
        global usuarios
        try:
            with open("usuarios.json", "r") as archivo:
                usuarios.update(json.load(archivo)) # actualiza el diccionario usuarios con los valores de usuario.json, para eso sirve el .update y load
        except:
            print("Archivo no encontrado, se creara con un usuario admin.")
            usuarios["admin"] = {"contrasena": "12345", 
                                 "rol": "admin", 
                                 "correo": "admin",
                                 "baneado": False} # creara el usuario "admin" con el rol admin y la contraseña 12345
            Sesion.guardar_datos_usuarios() # llama el metodo para guardar los datos nuevos


    def guardar_datos_usuarios(): # guarda los nuevos registros de usuarios
        try: # primero intenta escribir sobre el json de usuarios
            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo) # dump sirve para "tirar" o guardar los datos en el archivo ya leído "usuarios.json"
        except FileNotFoundError: # en caso de no encontrar el json, avisa y crea el archivo
            print("Archivo no encontrado, se creara uno nuevo para los usuarios.")
            usuarios["admin"] = {"contrasena": "12345",
                                "rol": "admin", 
                                "correo": "admin",
                                "baneado": False} # creara el usuario "admin" con el rol admin y la contraseña 12345
            
    def cargar_datos_noticias(): # carga el archivo anterior con las noticias existentes
        global noticias
        try:
            with open("noticias.json", "r") as archivo:
                noticias.update(json.load(archivo)) # actualiza el diccionario noticias con los valores de usuario.json, para eso sirve el .update y load
        except:
            print("Archivo de noticias no encontrado, se creara uno nuevo.")

    def guardar_datos_noticias(): # guarda los nuevos registros de las noticias
        try: # primero intenta escribir sobre el json de noticias
            with open("noticias.json", "w") as archivo:
                json.dump(noticias, archivo) # dump sirve para "tirar" o guardar los datos en el archivo ya leído "noticias.json"
        except FileNotFoundError: 
            print("Archivo no encontrado, se creara uno nuevo.")

    def cargar_datos_eventos(): 
        global eventos
        try:
            with open("eventos.json", "r") as archivo:
                eventos.update(json.load(archivo)) 
        except:
            print("Archivo de eventos no encontrado, se creara uno nuevo.")

    def guardar_datos_eventos(): 
        try: 
            with open("eventos.json", "w") as archivo:
                json.dump(eventos, archivo) 
        except FileNotFoundError: 
            print("Archivo no encontrado, se creara uno nuevo.")

    def comprobar_fecha_eventos():
        global eventos
        try:
            if len(eventos) != 0:

                now = datetime.now()
                eventos_copia = dict(eventos)

                for titulo, det in reversed(eventos_copia.items()):
                    fecha = datetime.strptime(det["fecha"], "%d/%m/%Y")
                    hora = datetime.strptime(det["hora"], '%H:%M').time()

                    if fecha.date() == now.date() and hora < now.time():
                        del eventos[titulo]
                    elif fecha.date() < now.date():
                        del eventos[titulo]
                Sesion.guardar_datos_eventos()
        except:
            print("¡Ocurrio un error inesperado al intentar borrar los eventos!")

# cargar datos previos
Sesion.cargar_datos_usuarios() 
Sesion.cargar_datos_noticias()
Sesion.cargar_datos_eventos()

# al iniciar el programa revisa si algun evento ya ocurrio
Sesion.comprobar_fecha_eventos()

ventana_opciones = VentanaOpciones() # abre la ventana principal

# guardar datos
Sesion.guardar_datos_usuarios()
Sesion.guardar_datos_noticias()
Sesion.guardar_datos_eventos()





print("Comprobar usuarios del json", usuarios) #FALTA borrar esto al final del programa.
