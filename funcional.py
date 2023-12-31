import json # para trabajar con archivos .json y guardar datos de forma permanente
import customtkinter as ctk  # interfaz gráfica
import tkinter as tk
import webbrowser  # para abrir link en denunciaBtn
import os  # para obtener directorio actual
from PIL import Image  # para utilizar imágenes
from collections import OrderedDict # trabajar con diccionarios ordenados
from datetime import datetime, time
from pygame import mixer #Sonidos


ctk.set_appearance_mode("dark") # tema oscuro

# diccionarios utilizados en el programa
usuarios = {} # almacenará los usuarios
noticias = OrderedDict() # almacenará las noticias de forma ordenada
eventos = OrderedDict() # almacena los eventos

# constantes
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
        ventana_invitado = VentanaInvitado()


class VentanaRegistro: # crea la ventana registro
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

    # comprueba si el correo que ingresa la persona no está asociado a otra cuenta
    def comprobar_correo(correo):
        for usuario in usuarios: # itera sobre cada usuario en el diccionario usuarios
            if str(correo.lower()) == str(usuarios[usuario]["correo"].lower()): # si el usuario actualmente iterado tiene el mismo correo, devuelve False, por lo tanto, si está asociado a otra cuenta
                return False
        return True # el correo no está asociado a ninguna cuenta
    
    def registro_evento(self, frame): # al darle click a registrar se iniciara este método, se crea la variable alerta para luego eliminar labels
        if self.nombre.get() not in usuarios: # comprueba que el nombre no exista previamente, si no existe ejecuta
            if len(self.correo.get().strip()) != 0 and len(self.nombre.get().strip()) != 0 and len(self.contrasena.get().strip()) != 0: # chequea que ningún campo este vacío
                if "@" in self.correo.get():
                    if VentanaRegistro.comprobar_correo(self.correo.get()):
                        if len(self.contrasena.get()) >= 8 and len(self.contrasena.get()) <20: # comprueba que la contraseña tenga entre 8 y 19 dígitos
                            if any(char.isdigit() for char in self.contrasena.get()): # comprueba que la contraseña tenga al menos un numero
                                if any(char in "!@#$%∧&*(._-)" for char in self.contrasena.get()): # comprueba si la contraseña tiene dígitos especiales
                                    if self.terminosCheckbox.get() == "on": # si el usuario acepta los términos
                                        usuarios[self.nombre.get()] = {"contrasena": self.contrasena.get(), "rol": "usuario", "correo": self.correo.get(), "baneado": False} # de forma predeterminada cualquier usuario nuevo tendrá el rol "usuario", donde no tiene grandes permisos
                                        Sesion.guardar_datos_usuarios() #guarda los datos del usuario en el json
                                        if hasattr(self, "mensaje"): # si existe el atributo mensaje en la pantalla actualmente lo borra para poner otro en su posicion
                                            self.mensaje.destroy()

                                        self.mensaje = ctk.CTkLabel(master = frame, text = "Usuario creado con éxito, espere unos instantes...")
                                        self.mensaje.place(relx = 0.2, rely = 0.72) 
                                        
                                        self.root.after(1200, self.abrir_ventana_login)
                                        
                                    else: # si no acepta los términos
                                        if hasattr(self, "mensaje"):
                                            self.mensaje.destroy()
                            
                                        self.mensaje = ctk.CTkLabel(master = frame, text = "Debes aceptar los términos y condiciones para usar nuestra aplicación.")
                                        self.mensaje.place(relx = 0.11, rely = 0.72) 
                                else: # si la contraseña no tiene un carácter especial
                                    if hasattr(self, "mensaje"):
                                        self.mensaje.destroy()
                            
                                    self.mensaje = ctk.CTkLabel(master = frame, text = "La contraseña debe tener al menos un carácter especial '!@#$%∧&*(._-)'. ")
                                    self.mensaje.place(relx = 0.11, rely = 0.72) 
                            else: # si la contraseña no tiene números
                                if hasattr(self, "mensaje"):
                                    self.mensaje.destroy()

                                self.mensaje = ctk.CTkLabel(master = frame, text = "La contraseña debe tener al menos un número.")
                                self.mensaje.place(relx = 0.23, rely = 0.72) 
                        else: # si la contraseña tiene menos de 8 caracteres o más de 20
                            if hasattr(self, "mensaje"):
                                self.mensaje.destroy()

                            self.mensaje = ctk.CTkLabel(master = frame, text = "La contraseña debe tener entre 8 y 20 caracteres.")
                            self.mensaje.place(relx = 0.22, rely = 0.72) 
                    else: # si el correo ya existe en una cuenta
                        if hasattr(self, "mensaje"):
                            self.mensaje.destroy()

                        self.mensaje = ctk.CTkLabel(master = frame, text = "El correo electrónico ya está asociado a una cuenta.")
                        self.mensaje.place(relx = 0.22, rely = 0.72) 
                else: # si el correo no tiene un @
                    if hasattr(self, "mensaje"):
                        self.mensaje.destroy()

                    self.mensaje = ctk.CTkLabel(master = frame, text = "Ingrese un correo electrónico válido.")
                    self.mensaje.place(relx = 0.30, rely = 0.72) 
            else: # si algun campo está vacío
                if hasattr(self, "mensaje"):
                    self.mensaje.destroy()

                self.mensaje = ctk.CTkLabel(master = frame, text = "Ningún campo debe estar vacío.")
                self.mensaje.place(relx = 0.30, rely = 0.72)
        else: # si el nombre de usuario ya existe
            if hasattr(self, "mensaje"):
                self.mensaje.destroy()

            self.mensaje = ctk.CTkLabel(master = frame, text = "El nombre de usuario ya existe.")
            self.mensaje.place(relx = 0.32, rely = 0.72) 
    
    def terminos_condiciones(self):
        terminosVentana = ctk.CTkToplevel(master=self.root)
        terminosVentana.title("NotiAlarm | Términos y condiciones")
        centrar_ventana(terminosVentana, "600", "400")
        notialarm_icono(terminosVentana)
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
                        usuario_actual = usuario # guarda el usuario en esta variable para saber el nombre del usuario conectado
                        break


        if verificar: # si el correo y la contraseña coinciden entra.
            if not usuarios[usuario]["baneado"]: # si el usuario no esta baneado
                if hasattr(self, "mensaje"):
                    self.mensaje.destroy()
                self.mensaje = ctk.CTkLabel(master = frame, text = "Iniciando Sesión...")
                self.mensaje.place(relx = 0.39, rely = 0.65)
                
                if usuarios[usuario]["rol"] == "usuario": # tiene el rol de usuario
                    self.root.after(1200, self.abrir_ventana_usuario)
                else:
                    self.root.after(1200, self.abrir_ventana_admin)

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
        ventana_noticias = VentanaNoticias(invitado=False) # abre la ventana principal

    def abrir_ventana_admin(self):
        self.root.destroy() # destruye la ventana actual
        ventana_admin = VentanaAdmin() # tiene el rol de administrador
        

class VentanaNoticias:
    def __init__(self, invitado):
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
        
        alarmaLabel = ctk.CTkLabel(master=sideFrame1, text="Iniciar alarma", font=("",16,"bold"))
        alarmaLabel.pack(pady=(70,0), padx=20, fill="x")

        seleccionAlarma = ctk.CTkOptionMenu(master=sideFrame1, values=["Elija una opción", "Robo", "Emergencia Medica", "Incendio"])
        seleccionAlarma.pack(pady=(10,0), padx=20, fill="x")

        activarAlarmaBtn = ctk.CTkButton(master=sideFrame1, text="Enviar alarma", command=lambda: self.comprobar_alarma(seleccionAlarma.get(), sideFrame1))
        activarAlarmaBtn.pack(pady=(10,10), padx=20, fill="x")

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
            mostradas = 0 # sirve como bandera para saber si algo ha sido mostrado
            if len(eventos) != 0: #si existe un evento sigue
                for titulo, det in reversed(eventos.items()):
                    if eventos[titulo]["mostrar"]: # si el evento se muestra sigue
                        ubicacion = det["ubicacion"] # obtiene todos los atributos necesarios
                        fecha = det["fecha"]
                        hora = det["hora"]
                        autor = det["autor"]
                        self.mostrar_evento(sideFrame2Eventos, titulo, ubicacion, fecha, hora, autor) # llama a la funcion mostrar_evento
                        mostradas += 1
            else: # si no existe ningun evento muestra este label
                ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack()
                mostradas += 1 
            if mostradas == 0: # si no se mostro nada muestra este label
                ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack() 
        except: # si da un error muestra este label
            ctk.CTkLabel(master = sideFrame2Eventos, text = "No hay eventos para mostrar.",height=400, font=ctk.CTkFont(size=14)).pack() 
        
        # -------------------- publicar -------------------
        notialarm_logo(frame, "NotiAlarm", 170)
        
        crearFrame = ctk.CTkFrame(master=frame)
        crearFrame.pack(pady=(0,10), padx=20, fill="x")

        crearLabel = ctk.CTkLabel(master=crearFrame, wraplength=520, height=40, font=("",14,"bold"), fg_color=ACCENT_COLOR, corner_radius=6, text="Crear publicación")
        crearLabel.pack(pady=0, padx=0, fill="x")

        crearAlarmaBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar noticia", command=self.publicar_noticia_ventana)
        crearAlarmaBtn.pack(pady=0, padx=0, fill="x", side="left")
        
        noticiaEventoBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar evento", command=self.publicar_evento_ventana)
        noticiaEventoBtn.pack(pady=0, padx=0, fill="x", side="right")
        
        # configuracion de inicio para invitado, se desactivan las funciones de publicación y alarma
        if invitado:
            crearLabel.configure(text="Inicia sesión para acceder a las funciones.", text_color="red")
            crearAlarmaBtn.configure(state="disabled")
            noticiaEventoBtn.configure(state="disabled")
            activarAlarmaBtn.configure(state="disabled")
            seleccionAlarma.configure(state="disabled")
       
        # comprueba el estado de la alerta
        self.estado_alarma() # si es True muestra un mensaje.

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
        webbrowser.open_new("https://seguridad.gba.gob.ar/#/home")

    def comprobar_alarma(self, opcion, sideFrame1):        
        if opcion != "Elija una opción":
            if opcion=="Incendio": # si en el menú desplegable el usuario selecciona alarma de tipo incendio
                ruta="bom"
                activa = "bom2"

            elif opcion=="Robo": # si en el menú desplegable el usuario selecciona alarma de tipo robo
                ruta="pol"
                activa = "pol2"

            elif opcion=="Emergencia Medica": # si en el menú desplegable el usuario selecciona alarma de tipo Emergencia Medica
                ruta="amb" # el nombre de la imagen a mostrar
                activa = "amb2" # la imagen que deberá mostrar cuando se inicie sesión con la alarma activada

            #envia el nombre de la imagen para completar la ruta
            self.mostrar_alarma(ruta)
            usuarios["alerta"] = {"valor": True, "correo": "x", "baneado": False, "rol": "desconocido", "ruta": activa, "enviada": usuario_actual} # crea el usuario "alerta" que almacene los valores necesarios
            Sesion.guardar_datos_usuarios()
            Sesion.cargar_datos_usuarios()

        else:
            if hasattr(self, "errorOpcion"):
                self.errorOpcion.destroy()
            self.errorOpcion = ctk.CTkLabel(master = sideFrame1, text = "Debe elegir una opción")
            self.errorOpcion.pack()

            # dependiendo de la opcion, se envia un mensaje de advertencia y una ruta a una imagen diferente, todo a la funcion mostrar_alarma()

    # comprueba el estado de la alarma
    def estado_alarma(self):
        for usuario in usuarios:
            if usuario == "alerta":
                if usuarios[usuario]["valor"]: # si es true lanza mensaje
                    ruta = usuarios["alerta"]["ruta"]
                    enviada = usuarios["alerta"]["enviada"]
                    self.mostrar_mensaje(ruta, enviada)                    

    def mostrar_alarma(self,ruta):
        #Ancho y Largo de la imagen, se debe cambiar tanto en el tamaño de la ventana como en el 
        anc=600
        lar=500

       # inicia el mixer
        mixer.init()

        # reproduce el sonido
        mixer.music.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "sonidos", "POLICE.mp3"))
        mixer.music.play()

        ventana_mensaje = ctk.CTkToplevel() # es una ventana secundaria
        ventana_mensaje.title(f"ALERTA ENVIADA") # titulo de la ventana
        ventana_mensaje.attributes("-topmost", "true")
        centrar_ventana(ventana_mensaje, str(anc), str(lar)) # centra la ventana
        ventana_mensaje.resizable(width=False, height=False) # no se puede cambiar los valores, agrandar o achicar
        currentPath = os.path.dirname(os.path.realpath(__file__)) # directorio de trabajo
        imagenFondo = ctk.CTkImage(Image.open(currentPath + f"/img/{ruta}.jpg"), size=(anc, lar)) # muestra la imagen
        imagenLabel = ctk.CTkLabel(ventana_mensaje, image=imagenFondo, text="")
        imagenLabel.place(relx=0, rely=0)

        # al cerrar la ventana, apaga el sonido
        ventana_mensaje.protocol("WM_DELETE_WINDOW", lambda: self.parar_sonido(ventana_mensaje))

    def parar_sonido(self, ventana_mensaje):
            mixer.music.stop()
            ventana_mensaje.destroy()

    def mostrar_mensaje(self, ruta, enviada):
        anc=600
        lar=500

       # inicia el mixer
        mixer.init()

        # reproduce el sonido
        mixer.music.load(os.path.join(os.path.dirname(os.path.realpath(__file__)), "sonidos", "POLICE.mp3"))
        mixer.music.play()

        ventana_mensaje = ctk.CTkToplevel()
        ventana_mensaje.title(f"Alerta enviada por: {enviada}")
        ventana_mensaje.attributes("-topmost", "true")
        centrar_ventana(ventana_mensaje, str(anc), str(lar))
        ventana_mensaje.resizable(width=False, height=False)
        currentPath = os.path.dirname(os.path.realpath(__file__))
        imagenFondo = ctk.CTkImage(Image.open(currentPath + f"/img/{ruta}.jpg"), size=(anc, lar))
        imagenLabel = ctk.CTkLabel(ventana_mensaje, image=imagenFondo, text="")
        imagenLabel.place(relx=0, rely=0)

        # al cerrar la ventana, apaga el sonido y desactiva la alarma
        ventana_mensaje.protocol("WM_DELETE_WINDOW", lambda: self.desactivar_alarma(ventana_mensaje))

    # si cierra la ventana desactiva la alarma y elimina todo
    def desactivar_alarma(self, ventana):
        usuarios["alerta"]["valor"] = False
        ventana.destroy()
        self.parar_sonido(ventana)
        Sesion.guardar_datos_usuarios()

    def cambiar_apariencia(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def publicar_noticia_ventana(self): 
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm | Crear noticia")
        centrar_ventana(publicarVentana, "650", "435")
        notialarm_icono(publicarVentana)
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
        
        publicarBoton = ctk.CTkButton(master=publicarFrame, height=BTN_ALTURA, text="Publicar", command=lambda: self.publicar_noticia_guardar(publicarFrame, publicarVentana))
        publicarBoton.pack(pady=5, padx=20, fill="x")

    # al tocar el botón de publicar deberá guardar la noticia en el json.
    def publicar_noticia_guardar(self, publicarFrame, ventana):
        # aclara que cambiara los valores de las variables globales
        global noticias 
        global usuarios_actual
        if self.publicarTitulo.get() not in noticias: # si el titulo de la noticia no existe previamente sigue
            if len(self.publicarTitulo.get().strip()) != 0 and len(self.publicarUbicacion.get().strip()) != 0 and len(self.publicarTextbox.get("1.0", "end").strip()) != 0: #si ningun campo esta vacio
                if len(self.publicarTitulo.get()) < 68: # si el titulo tiene menos de 68 caracteres
                    if len(self.publicarUbicacion.get()) <= 30:
                        if len(self.publicarTextbox.get("1.0", "end"))  <= 600:
                            if self.categoria.get().lower() != "categoria":
                                if hasattr(self, "info_evento"):
                                    self.info_evento.destroy()
                                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Noticia creada correctamente. Espere a que sea aprobada.")
                                self.info_evento.pack()
                                ventana.after(1300, lambda:ventana.destroy())

                                fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M') # obtiene la fecha actual
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

                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ningún campo debe estar vacío.")
                self.info_evento.pack()
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()

            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ya existe una noticia con el mismo título.")
            self.info_evento.pack()       
    
    # ventana para la creacion de eventos
    def publicar_evento_ventana(self):
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm | Crear evento")
        centrar_ventana(publicarVentana, "650", "290")
        notialarm_icono(publicarVentana)
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
        
        publicarBoton = ctk.CTkButton(master=publicarFrame, height=BTN_ALTURA, text="Publicar", command= lambda: self.publicar_evento_guardar(publicarFrame, publicarVentana))
        publicarBoton.pack(pady=5, padx=20, fill="x")
    
    # realiza comprobaciones del evento a crear y lo guarda en el JSON
    def publicar_evento_guardar(self, publicarFrame, ventana):
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

                                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Evento creado correctamente. Espere a que sea aprobado.")
                                self.info_evento.pack()
                                ventana.after(1300, lambda:ventana.destroy())
                                 
                            else:
                                if hasattr(self, "info_evento"):
                                    self.info_evento.destroy()

                                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La hora ingresada no es válida.")
                                self.info_evento.pack() 
                        else:
                            if hasattr(self, "info_evento"):
                                self.info_evento.destroy()

                            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La fecha ingresada no es válida.")
                            self.info_evento.pack()
                    else:
                        if hasattr(self, "info_evento"):
                            self.info_evento.destroy()

                        self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "La ubicación debe tener menos de 20 caracteres.")
                        self.info_evento.pack()  
                else:
                    if hasattr(self, "info_evento"):
                        self.info_evento.destroy()

                    self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "El título debe tener menos de 20 caracteres.")
                    self.info_evento.pack()
            else:
                if hasattr(self, "info_evento"):
                    self.info_evento.destroy()

                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ningún campo debe estar vacío.")
                self.info_evento.pack()  
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()

            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ya existe un evento con el mismo título.")
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
            formato = "%d/%m/%y"
            fecha = datetime.strptime(fecha, formato)
            return fecha
        except:
            return None

    # crea un frame para cada noticia
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
        noticiaInfo.pack(pady=5, padx=20, side="left")
        
        if usuario == usuario_actual:
            noticiaBorrar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Borrar", command=lambda: self.confirmar_eliminacion(titulo, noticiaFrame))
            noticiaBorrar.pack(pady=0, padx=0, side="right")

            noticiaEditar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Editar", command= lambda: self.editar_noticia(titulo, noticiaFrame))
            noticiaEditar.pack(pady=0, padx=1, side="right")

    # ventana para editar una noticia
    def editar_noticia(self, titulo, noticiaFrame): 
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm | Editar noticia")
        centrar_ventana(publicarVentana, "650", "435")
        notialarm_icono(publicarVentana)
        publicarVentana.resizable(False, False)
        publicarVentana.attributes("-topmost", "true")
        
        currentPath = os.path.dirname(os.path.realpath(__file__))
        imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 680))
        imagenLabel = ctk.CTkLabel(publicarVentana, image=imagenFondo, text="")
        imagenLabel.place(relx=0, rely=0)
        
        editarFrame = ctk.CTkFrame(master=publicarVentana)
        editarFrame.pack(pady=0, padx=90, fill="both", expand=True)
        
        publicarLabel = ctk.CTkLabel(master=editarFrame, height=40,font=('Roboto', 24), text="Editar publicación | Noticia")
        publicarLabel.pack(pady=(20,15), padx=20, fill="x")
        
        self.publicarTitulo = ctk.CTkEntry(master=editarFrame, height=BTN_ALTURA, placeholder_text="Título")
        self.publicarTitulo.pack(pady=5, padx=20, fill="x")
        
        self.publicarUbicacion = ctk.CTkEntry(master=editarFrame, height=BTN_ALTURA, placeholder_text="Ubicación")
        self.publicarUbicacion.pack(pady=5, padx=20, fill="x")
        
        self.publicarTextbox = ctk.CTkTextbox(master=editarFrame, height=140)
        self.publicarTextbox.pack(pady=5, padx=20, fill="x")

        self.categoria = ctk.CTkOptionMenu(master=editarFrame, values=["Categoria", "Robo", "Accidentes", "Asesinatos", "Eventos Locales", "Trafico", "Incendios y Rescates", "Eventos de emergencia", "Obras Publicas", "Otras"])
        self.categoria.pack(pady=5, padx=20, fill="x")
        
        publicarBoton = ctk.CTkButton(master=editarFrame, height=BTN_ALTURA, text="Publicar", command=lambda: self.editar_noticia_evento(titulo, editarFrame, noticiaFrame, publicarVentana))
        publicarBoton.pack(pady=5, padx=20, fill="x")
        
    # realiza diferentes comprobaciones para editar una noticia y guarda los cambios en un JSON
    def editar_noticia_evento(self, titulo, editarFrame, noticiaFrame, ventana):
        global noticias
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')
        bandera_modificacion = False #Sirve para saber si el usuario realizo alguna modificacion.

        if len(self.publicarTitulo.get().strip()) != 0 and len(self.publicarTitulo.get().strip()) < 68: # si el usuario ingresa un titulo y es menor a 68 caracteres
            tituloNuevo = self.publicarTitulo.get()
            bandera_modificacion = True # se modifico algo, guarda el nuevo valor
        elif len(self.publicarTitulo.get().strip()) == 0:
            tituloNuevo = titulo
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()
                        
            self.info_evento = ctk.CTkLabel(master = editarFrame, text = "El titulo debe tener menos de 68 caracteres.")
            self.info_evento.pack()

        if len(self.publicarUbicacion.get().strip()) != 0 and len(self.publicarUbicacion.get().strip()) <= 30:
            ubicacion = self.publicarUbicacion.get()
            bandera_modificacion = True
        elif len(self.publicarUbicacion.get().strip()) == 0: # si no se pone nada mantiene el valor actual
            ubicacion = noticias[titulo]["ubicacion"]
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()
                        
            self.info_evento = ctk.CTkLabel(master = editarFrame, text = "La ubicación debe tener menos de 30 caracteres.")
            self.info_evento.pack()

        if len(self.publicarTextbox.get("1.0", "end").strip()) != 0 and len(self.publicarTextbox.get("1.0", "end"))  <= 600:
            contenido = self.publicarTextbox.get("1.0", "end")
            bandera_modificacion = True
        elif len(self.publicarTextbox.get("1.0", "end").strip()) == 0:
            contenido = noticias[titulo]["contenido"]
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()
                        
            self.info_evento = ctk.CTkLabel(master = editarFrame, text = "La descripción debe tener menos de 500 caracteres.")
            self.info_evento.pack() 

        if self.categoria.get() != "Categoria":
            categoria = self.categoria.get()
            bandera_modificacion = True 
        else:
            categoria = noticias[titulo]["categoria"]

        if bandera_modificacion: # si se modifica algo guarda los datos
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()

            self.info_evento = ctk.CTkLabel(master = editarFrame, text = "Noticia modificada correctamente, actualiza para verla.")
            self.info_evento.pack()

            noticiaFrame.destroy()
            editarFrame.destroy()
            ventana.destroy()
            del noticias[titulo]
            noticias[tituloNuevo] = {"contenido": contenido,
                                "autor": usuario_actual,
                                "ubicacion": ubicacion,
                                "mostrar": False,
                                "categoria": categoria,
                                "fecha": fecha_actual} #Atributos de las noticias
            Sesion.guardar_datos_noticias()
        else: # si no se modifica nada muestra un label
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()
                        
            self.info_evento = ctk.CTkLabel(master = editarFrame, text = "Debes de realizar almenos una modificacion.")
            self.info_evento.pack() 

    # funcion para eliminar una noticia existente
    def eliminar_noticia(self, titulo, noticiaFrame, confirmarToplevel):
        global noticias
        try:
            del noticias[titulo]
            Sesion.guardar_datos_noticias()
            Sesion.cargar_datos_noticias()
            noticiaFrame.destroy()
            confirmarToplevel.destroy()

        except:
            print("La noticia fue eliminada.") # solo se muestra en consola

    # ventana para confirmar la eliminacion
    def confirmar_eliminacion(self, titulo , noticiaFrame):
        confirmarToplevel = ctk.CTkToplevel(master=self.root)
        confirmarToplevel.title("NotiAlarm | Eliminar Publicación")
        centrar_ventana(confirmarToplevel, "470", "180")
        notialarm_icono(confirmarToplevel)
        confirmarToplevel.resizable(False, False)
        confirmarToplevel.attributes("-topmost", "true")
        
        confirmarelimLabel = ctk.CTkLabel(master=confirmarToplevel, height=40, font=("", 18), text=f"¿Está seguro que desea eliminarla?")
        confirmarelimLabel.pack(pady=(40,0), padx=30, fill="x")
        
        btnCancelar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Cancelar", command=confirmarToplevel.destroy)
        btnCancelar.pack(pady=(0,40), padx=(70,0), side="left")

        btnAceptar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Aceptar", command=lambda: self.eliminar_noticia(titulo,noticiaFrame, confirmarToplevel))
        btnAceptar.pack(pady=(0,40), padx=(0,70), side="right")

    # ventana para mostrar los eventos con un frame cada uno
    def mostrar_evento(self, frame, titulo, ubicacion, fecha, hora, autor):
        eventoTitulo = ctk.CTkLabel(master=frame, text=f"{titulo} \n{ubicacion}\n{fecha} | {hora}\n{autor}", justify="left", anchor="w", wraplength=180, font=("",13,"bold"))
        eventoTitulo.pack(pady=10, padx=20, fill="x")
    
    # vuelve a la ventana de opciones
    def volver(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()


# ventana de administrador
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

        # cerrar sesión
        cerrarSesionLabel = ctk.CTkLabel(master=sideFrame1, text="Cerrar sesión", font=("",16,"bold"))
        cerrarSesionLabel.pack(pady=(30,0), padx=20, fill="x")
        
        volver = ctk.CTkButton(master=sideFrame1, text="<  Volver", command=self.volver)
        volver.pack(pady=10, padx=20, fill="x")
        
        # banear usuario
        banearLabel = ctk.CTkLabel(master=sideFrame1, text="Banear usuario", font=("",16,"bold"))
        banearLabel.pack(pady=(90,10), padx=20, fill="x")
        
        self.banearEntry = ctk.CTkEntry(master=sideFrame1, placeholder_text="Nombre de usuario")
        self.banearEntry.pack(pady=0, padx=20, fill="x")
        
        banearTxt = ctk.CTkLabel(master=sideFrame1, text="ó")
        banearTxt.pack(pady=5, padx=20, fill="x")
        
        # añadir todos los usuarios al desplegable banear_desplegable
        elementos_desplegable = []
        for usuario in usuarios:
            if usuarios[usuario]["rol"] == "admin" or usuario == "alerta" or usuarios[usuario]["baneado"] == True: # ignora la alerta, los usuarios con el rol administrador y los baneados.
                pass 
            else:
                elementos_desplegable.append(usuario)
        
        self.banearDesplegable = ctk.CTkOptionMenu(master=sideFrame1, values=["Mostrar Usuarios"] + elementos_desplegable)
        self.banearDesplegable.pack(pady=(0,10), padx=20, fill="x")
         
        banearAceptar = ctk.CTkButton(master=sideFrame1, text="Banear", command=lambda:self.BanearUsuario("", sideFrame1))
        banearAceptar.pack(pady=(0,10), padx=20, fill="x")
        
        
        # crear administrador
        nuevoAdminLabel = ctk.CTkLabel(master=sideFrame1, text="Dar permisos de admin", font=("",16,"bold"))
        nuevoAdminLabel.pack(pady=(90,10), padx=20, fill="x")
        
        self.nuevoAdminEntry = ctk.CTkEntry(master=sideFrame1, placeholder_text="Nombre de usuario")
        self.nuevoAdminEntry.pack(pady=0, padx=20, fill="x")
        
        nuevoAdminTxt = ctk.CTkLabel(master=sideFrame1, text="ó")
        nuevoAdminTxt.pack(pady=5, padx=20, fill="x")
        
        self.nuevoAdminDesplegable = ctk.CTkOptionMenu(master=sideFrame1, values=["Mostrar Usuarios"] + elementos_desplegable)
        self.nuevoAdminDesplegable.pack(pady=(0,10), padx=20, fill="x")
         
        nuevoAdminAceptar = ctk.CTkButton(master=sideFrame1, text="Crear admin", command=lambda: self.nuevoAdmin(sideFrame1))
        nuevoAdminAceptar.pack(pady=(0,10), padx=20, fill="x")
        
        
        # cambiar apariencia
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
        notialarm_logo(frame, "NotiAlarm - Admin", 110)
        
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

    # funcion para añadir un nuevo administrador
    def nuevoAdmin(self, ventana):
        global usuarios
        if len(self.nuevoAdminEntry.get().strip()) != 0:
            try:
                if self.nuevoAdminEntry.get() in usuarios: # si el usuario ingresado existe
                        usuarios[self.nuevoAdminEntry.get()]["rol"] = "admin" # el usuario ingresado recibe el rol admin
                        if hasattr(self, "mensaje"):
                            self.mensaje.destroy()
                        self.mensaje = ctk.CTkLabel(master = ventana, text = f"El usuario {self.nuevoAdminEntry.get()} ahora es administrador.")
                        self.mensaje.pack()

                else:
                    if hasattr(self, "mensaje"):
                            self.mensaje.destroy()
                    self.mensaje = ctk.CTkLabel(master = ventana, text = "Usuario no encontrado.")
                    self.mensaje.pack()

            except:
                print("Error al otorgar rol admin con el entry")

        elif self.nuevoAdminDesplegable.get() != "Mostrar Usuarios": # si selecciona un usuario en el desplegable
            try:
                if self.nuevoAdminDesplegable.get() in usuarios:
                    usuarios[self.nuevoAdminDesplegable.get()]["rol"] = "admin" # se le asigna rol admin
                    if hasattr(self, "mensaje"):
                        self.mensaje.destroy()
                    self.mensaje = ctk.CTkLabel(master = ventana, text = f"El usuario {self.nuevoAdminEntry.get()} ahora es administrador.")
                    self.mensaje.pack()
            except:
                print("Error al otorgar rol admin con el desplegable.")
        elif self.banearDesplegable.get() == "Mostrar Usuarios":

            if hasattr(self, "mensaje"):
                self.mensaje.destroy()
            self.mensaje = ctk.CTkLabel(master = ventana, text = "Debes seleccionar un usuario.")
            self.mensaje.pack()

        Sesion.guardar_datos_usuarios() # siempre se guardan y cargan todos los datos
        Sesion.cargar_datos_usuarios()

    # muestra las publicaciones para el administrador con los botones de publicar, rechazar o banear usuario
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
    
    # ventana confirmar baneo
    def confirmar_banear(self, usuario):
        confirmarToplevel = ctk.CTkToplevel(master=self.root)
        confirmarToplevel.title("NotiAlarm | Banear usuario")
        centrar_ventana(confirmarToplevel, "470", "180")
        notialarm_icono(confirmarToplevel)
        confirmarToplevel.resizable(False, False)
        confirmarToplevel.attributes("-topmost", "true")
        
        banearLabel = ctk.CTkLabel(master=confirmarToplevel, height=40, font=("", 18), text=f"¿Está seguro que desea banear a {usuario}?")
        banearLabel.pack(pady=(40,0), padx=30, fill="x")
        
        btnCancelar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Cancelar", command=confirmarToplevel.destroy)
        btnCancelar.pack(pady=(0,40), padx=(70,0), side="left")
        
        btnAceptar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Aceptar", command=lambda: self.BanearUsuario_de_noticias(usuario, confirmarToplevel))
        btnAceptar.pack(pady=(0,40), padx=(0,70), side="right")
        
    # muestra los eventos con los botones de publicar o rechazar
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

    # banea usuario que publico la noticia o ingresa el admin
    def BanearUsuario(self, usuario, confirmarToplevel):
        global usuarios
        if len(self.banearEntry.get().strip()) != 0:
            try:
                if self.banearEntry.get() in usuarios:
                    if usuarios[self.banearEntry.get()]["baneado"] == True:
                        if hasattr(self, "mensaje"):
                            self.mensaje.destroy()
                        self.mensaje = ctk.CTkLabel(master = confirmarToplevel, text = "El usuario ya se encuentra baneado.")
                        self.mensaje.pack()
                    else:
                        usuarios[self.banearEntry.get()]["baneado"] = True
                        if hasattr(self, "mensaje"):
                            self.mensaje.destroy()
                        self.mensaje = ctk.CTkLabel(master = confirmarToplevel, text = "Usuario baneado correctamente.")
                        self.mensaje.pack()

                else:
                    if hasattr(self, "mensaje"):
                            self.mensaje.destroy()
                    self.mensaje = ctk.CTkLabel(master = confirmarToplevel, text = "Usuario no encontrado.")
                    self.mensaje.pack()

            except:
                print("Error al banear usuario con el entry")
        elif self.banearDesplegable.get() != "Mostrar Usuarios":
            try:
                if usuarios[self.banearDesplegable.get()]["baneado"] == True:
                    if hasattr(self, "mensaje"):
                        self.mensaje.destroy()
                    self.mensaje = ctk.CTkLabel(master = confirmarToplevel, text = "El usuario ya se encuentra baneado.")
                    self.mensaje.pack()
                else:
                    usuarios[self.banearDesplegable.get()]["baneado"] = True
                    if hasattr(self, "mensaje"):
                        self.mensaje.destroy()
                    self.mensaje = ctk.CTkLabel(master = confirmarToplevel, text = "Usuario baneado correctamente.")
                    self.mensaje.pack()
            except:
                print("Error al banear usuario con el desplegable.")
        elif self.banearDesplegable.get() == "Mostrar Usuarios":
            if hasattr(self, "mensaje"):
                self.mensaje.destroy()
            self.mensaje = ctk.CTkLabel(master = confirmarToplevel, text = "Debes seleccionar un usuario.")
            self.mensaje.pack()

        Sesion.guardar_datos_usuarios()
        Sesion.cargar_datos_usuarios()

    def BanearUsuario_de_noticias(self, usuario, confirmarToplevel):
        try:
            usuarios[usuario]["baneado"] = True
            confirmarToplevel.destroy()
            Sesion.guardar_datos_usuarios()
            Sesion.cargar_datos_usuarios()
        except:
            print("Usuario no encontrado.") 


class VentanaInvitado(VentanaNoticias):
    def __init__(self):
        invitado = True
        super().__init__(invitado)


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


    # si algun evento ya ocurrio lo eliminara para no mostrarlo
    def comprobar_fecha_eventos():
        global eventos
        try:
            if len(eventos) != 0:

                now = datetime.now()
                eventos_copia = dict(eventos)

                for titulo, det in reversed(eventos_copia.items()):
                    fecha = datetime.strptime(det["fecha"], "%d/%m/%y")
                    hora = datetime.strptime(det["hora"], '%H:%M').time()

                    if fecha.date() == now.date() and hora < now.time():
                        del eventos[titulo]
                    elif fecha.date() < now.date():
                        del eventos[titulo]
                Sesion.guardar_datos_eventos()
        except:
            print("¡Ocurrio un error inesperado al intentar borrar los eventos!")


def opciones_universales(self):
    notialarm_icono(self.root)
    centrar_ventana(self.root, "1100", "680")
    self.root.title("NotiAlarm")
    self.root.resizable(False, False)
    
    currentPath = os.path.dirname(os.path.realpath(__file__))
    imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 680))
    imagenLabel = ctk.CTkLabel(self.root, image=imagenFondo, text="")
    imagenLabel.place(relx=0, rely=0)


def notialarm_icono(ventana):
    carpeta_principal = os.path.dirname(__file__)
    carpeta_imagenes = os.path.join(carpeta_principal, "img")
    ventana.iconbitmap(os.path.join(carpeta_imagenes, "ventana.ico"))


def notialarm_logo(frame, texto, padLeft):
    tituloFrame = ctk.CTkFrame(master=frame)
    tituloFrame.pack(pady=0, padx=(padLeft,20), fill="x")
    
    currentPath = os.path.dirname(os.path.realpath(__file__))
    imagenIcono = ctk.CTkImage(Image.open(currentPath + "/img/icon.png"), size=(50, 50))
    imagenLabel = ctk.CTkLabel(tituloFrame, image=imagenIcono, text="")
    imagenLabel.pack(side="left")
    
    titulo = ctk.CTkLabel(master=tituloFrame, text=texto, justify="left", anchor="w", font=(TITULOS_FUENTE))
    titulo.pack(pady=20, padx=20, fill="x", side="left")


def centrar_ventana(ventana, ancho, alto):
    # obten el ancho y el alto de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    # calcula las coordenadas para centrar la ventana
    x = (ancho_pantalla - int(ancho)) // 2
    y = (alto_pantalla - int(alto)) // 2 - 40

    # establece el tamaño y posicion de la ventana
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


# cargar datos previos
Sesion.cargar_datos_usuarios() 
Sesion.cargar_datos_noticias()
Sesion.cargar_datos_eventos()

# al iniciar ocurren estas cosas:
Sesion.comprobar_fecha_eventos() # comprueba las fechas de todos los eventos, si alguna ya paso la elimina

ventana_opciones = VentanaOpciones() # abre la ventana principal

# guardar datos
Sesion.guardar_datos_usuarios()
Sesion.guardar_datos_noticias()
Sesion.guardar_datos_eventos()



