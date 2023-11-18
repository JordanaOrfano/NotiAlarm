import json #Para trabajar con archivos .json y guardar datos de forma permanente.
import customtkinter as ctk
import tkinter as tk
from PIL import Image
from collections import OrderedDict #Trabajar con diccionarios ordenados.
import os
from datetime import datetime, time

ctk.set_appearance_mode("dark") # tema oscuro

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

        btnRegistro = ctk.CTkButton(master=frame, height=BTN_ALTURA, width=BTN_ANCHO, text="Registrarse", command=self.abrir_ventana_registro) # crea el boton
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
        label.place(relx=0.5, rely=0.30, anchor=tk.CENTER)

        self.correo = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Correo electrónico")
        self.correo.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.nombre = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, placeholder_text="Usuario")
        self.nombre.place(relx = 0.5, rely = 0.47, anchor = tk.CENTER)

        self.contrasena = ctk.CTkEntry(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, show="*", placeholder_text="Contraseña")
        self.contrasena.place(relx=0.5, rely=0.54, anchor=tk.CENTER)

        registrar = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Registrarse", command = lambda: self.registro_evento(frame))
        registrar.place(relx=0.5, rely=0.61, anchor=tk.CENTER)

        volver = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Volver", fg_color="transparent", text_color=("#1a1a1a","#ffffff"), hover=False, command=self.abrir_ventana_opciones)
        volver.place(relx=0.5, rely=0.68, anchor=tk.CENTER)

        self.root.mainloop()

    def abrir_ventana_opciones(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()

    def comprobar_correo(correo):
        for usuario in usuarios:
            if str(correo.lower()) == str(usuarios[usuario]["correo"].lower()):
                return False
        return True
    
    def registro_evento(self, frame): #Al darle click a registrar se iniciara este metodo, se crea la variable alerta para luego eliminar labels.
        
        if self.nombre.get() not in usuarios: #Comprueba que el nombre no exista previamente, si no existe ejecuta.
            if len(self.correo.get().strip()) != 0 and len(self.nombre.get().strip()) != 0 and len(self.contrasena.get().strip()) != 0: #chequea que ningun campo este vacio.
                if "@" in self.correo.get():
                    if VentanaRegistro.comprobar_correo(self.correo.get()):
                        if len(self.contrasena.get()) >= 8 and len(self.contrasena.get()) <20: #Comprueba que la contraseña tenga mas de 7 digitos y tenga al menos 20 digitos.
                            if any(char.isdigit() for char in self.contrasena.get()): #Comprueba que la contraseña tenga al menos un numero.
                                if any(char in "!@#$%∧&*(._-)" for char in self.contrasena.get()): #Comprueba si la contraseña tiene digitos especiales
                                    usuarios[self.nombre.get()] = {"contrasena": self.contrasena.get(), "rol": "usuario", "correo": self.correo.get()} #De forma predeterminada cualquier usuario nuevo tendrá el rol "usuario", donde no tiene grandes permisos.
                                    Sesion.guardar_datos_usuarios()
                                    if hasattr(self, "mensaje"):
                                        self.mensaje.destroy()

                                    self.mensaje = ctk.CTkLabel(master = frame, text = "Usuario creado con éxito, espere unos instantes...")
                                    self.mensaje.place(relx = 0.2, rely = 0.72) 
                                    
                                    self.root.destroy()
                                    ventana_opciones = VentanaLogin()
                                else:
                                    
                                    if hasattr(self, "mensaje"):
                                        self.mensaje.destroy()
                            
                                    self.mensaje = ctk.CTkLabel(master = frame, text = "La contraseña debe tener al menos un caracter especial '!@#$%∧&*(._-)'. ")
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
                    self.mensaje.place(relx = 0.25, rely = 0.72) 
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

    def login_evento(self, frame): #Al tocar el boton login.
        global usuario_actual
        verificar = False #Por ahora, la contraseña no coincide; Valor predeterminado.

        for usuario in usuarios: #Verifica si algun correo en el diccionario usuarios coincide con el ingresado.
            if self.correo.get().lower().strip() == usuarios[usuario]['correo'].lower().strip():
                if str(self.contrasena.get()) == str(usuarios[usuario]['contrasena']): #Si encuentra un correo que coincide con el ingresado, comprueba que tambien coincida la contraseña.
                    verificar = True #El correo y la contraseña coinciden.
                    usuario_actual = usuario
                    break
        if verificar:
            if hasattr(self, "mensaje"):
                self.mensaje.destroy()
            self.mensaje = ctk.CTkLabel(master = frame, text = "Iniciando Sesión...")
            self.mensaje.place(relx = 0.39, rely = 0.65)
            

            if usuarios[usuario]["rol"] == "usuario": #Tiene el rol de usuario
                self.root.destroy() # destruye la ventana actual
                ventana_noticias = VentanaNoticias() # abre la ventana principal
            else:
                self.root.destroy() # destruye la ventana actual
                ventana_admin = VentanaAdmin() #Tiene el rol de administrador
            
        else:
            if hasattr(self, "mensaje"):
                self.mensaje.destroy()
            self.mensaje = ctk.CTkLabel(master = frame, text = "Correo o contraseña inválidos.")
            self.mensaje.place(relx = 0.32, rely = 0.65) 


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

        sideFrame1Titulo = ctk.CTkLabel(master=sideFrame1, text="Información", justify="left", anchor="w", font=("",16,"bold"))
        sideFrame1Titulo.pack(pady=(100,0), padx=66, fill="x")
        
        numEmergencia = ctk.CTkLabel(master=sideFrame1, text="911 | Policía\n100 | Bomberos\n107 | Ambulancia", justify="left", anchor="w", wraplength=205, font=("",13,"bold"))
        numEmergencia.pack(pady=0, padx=66, fill="x")
        
        volver = ctk.CTkButton(master=sideFrame1, text="Hacer denuncia online", command=self.volver)
        volver.pack(pady=(100,10), padx=20, fill="x")

        activarAlarmaBtn = ctk.CTkButton(master=sideFrame1, text="Enviar Alarma", command=lambda: self.comprobar_alarma(seleccionAlarma.get(), sideFrame1))
        activarAlarmaBtn.pack(pady=(10,30), padx=20, fill="x", side="bottom")

        seleccionAlarma = ctk.CTkOptionMenu(master=sideFrame1, values=["Elija una opción", "Robo", "Emergencia Medica", "Incendio"])
        seleccionAlarma.pack(pady=(10,0), padx=20, fill="x", side="bottom")
        
        alarmaLabel = ctk.CTkLabel(master=sideFrame1, text="Iniciar Alarma", font=("",16,"bold"))
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
        
        #Mostrar todos los eventos en el menú.
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
        titulo = ctk.CTkLabel(master=frame, text="(icono) NotiAlarm", justify="left", anchor="w", font=(TITULOS_FUENTE))
        titulo.pack(pady=20, padx=20, fill="x")
        
        crearFrame = ctk.CTkFrame(master=frame)
        crearFrame.pack(pady=(0,10), padx=20, fill="x")
        
        crearLabel = ctk.CTkLabel(master=crearFrame, wraplength=520, height=40, font=("",14,"bold"), fg_color=ACCENT_COLOR, corner_radius=6, text="Crear publicación")
        crearLabel.pack(pady=0, padx=0, fill="x")
        
        crearAlarmaBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar noticia", command=self.publicar_noticia)
        crearAlarmaBtn.pack(pady=0, padx=0, fill="x", side="left")
        
        noticiaEventoBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar evento", command=self.Evento)
        noticiaEventoBtn.pack(pady=0, padx=0, fill="x", side="right")
       
        #Mostrar todas las noticias en el menú.
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


    def comprobar_alarma(self, opcion, sideFrame1):
        print(opcion)
        if opcion=="Elija una opción":
            if hasattr(self, "errorOpcion"):
                self.errorOpcion.destroy()
            usuarios["alerta"] = {"valor": True, "correo": "x"}
            self.errorOpcion = ctk.CTkLabel(master = sideFrame1, text = "Debe elegir una opcion")
            self.errorOpcion.pack(fill="x",pady=0)
            #.place(relx=0.2, rely=0.1, fill="x") 
            #errorOpcion = ctk.CTkLabel(master=sideFrame1, text="Debe elegir una opción", font=("",16,"bold")).pack()


    def activar_alarma(self):
        # Iterar sobre cada usuario y enviar un mensaje
        for usuario in usuarios:
            if usuario == "alarma":
                if usuario["valor"]:
                    #Muestra mensaje

                    #Cambia el valor
                    usuario["valor"] = False
                    pass
                    #si es true lanza mensaje
                else:
                    pass
                    #no lanza mensaje
        
            mensaje = f"¡ALERTA! La alarma ha sido activada. Por favor, toma las precauciones necesarias."

            print(f"Mensaje enviado a {usuarios[usuario]}: {mensaje}")

            #Mostrar el mensaje en la interfaz de usuario del remitente
        self.mostrar_mensaje(usuarios[usuario], mensaje)
    
        #self.root=VentanaAlerta()


    def mostrar_mensaje(self, usuario, mensaje):
        # Crear una nueva ventana para mostrar el mensaje
        ventana_mensaje = ctk.CTkToplevel()
        ventana_mensaje.title(f"Mensaje para {usuario}")
        ventana_mensaje.attributes("-topmost", "true")

        # Etiqueta con el mensaje
        etiqueta_mensaje = ctk.CTkLabel(master=ventana_mensaje, text=mensaje, padx=20, pady=20)
        etiqueta_mensaje.pack()

    
    def cambiar_apariencia(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)
        

    def publicar_noticia(self): 
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm")
        publicarVentana.geometry("650x435")
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


    #Al tocar el boton de publicar debera guardar la noticia en el json.
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
        publicarVentana.title("NotiAlarm")
        publicarVentana.geometry("650x290")
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
                                fecha = fecha.strftime( "%d/%m/%Y") #Lo pasa nuevamente a una fecha texto para guardarla correctamente en un json y que no de error.
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

                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ningun campo puede estar vacio.")
                self.info_evento.pack()  
        else:
            if hasattr(self, "info_evento"):
                self.info_evento.destroy()

            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ya existe un evento con el mismo titulo.")
            self.info_evento.pack() 

    #Necesitamos comprobar si la hora ingresada es valida.
    def es_hora_valida(hora):
        try:
            hora = datetime.strptime(hora,"%H:%M").time()
            
            if 0 <= hora.hour < 24 and 0 <= hora.minute < 60:
                return hora
            else:
                return None
        except:
            return None
        
    #Comprueba si la fecha es valida.
    def es_fecha_valida(fecha):
        try:
            fecha = datetime.strptime(fecha, "%d/%m/%Y")
            return fecha
        except:
            return None

    def mostrar_publicacion(self, frame, titulo, ubicacion, categoria, texto, usuario, fecha): # creacion de publicacion
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
        
        #Mostrar todos los eventos en el menú.
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
        titulo = ctk.CTkLabel(master=frame, text="(icono) NotiAlarm | Administrador", justify="left", anchor="w", font=(TITULOS_FUENTE))
        titulo.pack(pady=20, padx=20, fill="x")
        
        administrarLabel = ctk.CTkLabel(master=frame, wraplength=520, height=40, font=("",14,"bold"), fg_color=ACCENT_COLOR, corner_radius=6, text="Administrar Publicaciones")
        administrarLabel.pack(pady=5, padx=20, fill="x")
        
        #Mostrar todas las noticias en el menú.
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
    
    
    def mostrar_publicacion(self, frame, titulo, ubicacion, categoria, texto, usuario, fecha): # creacion de publicacion
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

        noticiaPublicar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Publicar", command=lambda: self.AceptaPublicar(titulo))
        noticiaPublicar.pack(pady=0, padx=0, side="right")
        
        noticiaBorrar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Rechazar", command=lambda: self.RechazarNoticia(titulo))
        noticiaBorrar.pack(pady=0, padx=(1,0), side="right")
        
        noticiaBanearUsuario = ctk.CTkButton(master=noticiaInfoFrame, width=100, height=40, text="Banear usuario", command=lambda: self.confirmar_banear("test12345"))
        noticiaBanearUsuario.pack(pady=0, padx=0, side="right")
        
    
    def confirmar_banear(self, usuario):
        confirmarToplevel = ctk.CTkToplevel(master=self.root)
        confirmarToplevel.title("NotiAlarm")
        confirmarToplevel.geometry("470x180")
        confirmarToplevel.resizable(False, False)
        confirmarToplevel.attributes("-topmost", "true")
        
        banearLabel = ctk.CTkLabel(master=confirmarToplevel, height=40, font=("", 18), text=f"¿Está seguro que desea banear a {usuario}?")
        banearLabel.pack(pady=(40,0), padx=30, fill="x")
        
        btnCancelar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Cancelar", command=confirmarToplevel.destroy)
        btnCancelar.pack(pady=(0,40), padx=(70,0), side="left")
        
        btnAceptar = ctk.CTkButton(master=confirmarToplevel, height=35, width=162, text="Aceptar")
        btnAceptar.pack(pady=(0,40), padx=(0,70), side="right")
        
    
    def mostrar_evento(self, frame, titulo, ubicacion, fecha, hora, autor):
        eventoFrame1 = ctk.CTkFrame(master=frame, fg_color=("#cccccc","#333333"))
        eventoFrame1.pack(pady=5, padx=0, fill="x")
        
        eventoTitulo = ctk.CTkLabel(master=eventoFrame1, text=f"{titulo} \n{ubicacion}\n{fecha} | {hora}\n{autor}", justify="left", anchor="w", wraplength=180, font=("",13,"bold"))
        eventoTitulo.pack(pady=10, padx=20, fill="x")
        
        btnBorrar = ctk.CTkButton(master=eventoFrame1, width=119, text="Rechazar")
        btnBorrar.pack(pady=0, padx=0, side="left")
        
        btnPublicar = ctk.CTkButton(master=eventoFrame1, width=119, text="Publicar")
        btnPublicar.pack(pady=0, padx=0, side="right")


    #Publica la noticia seleccionada.
    def AceptaPublicar(self, titulo):
        global noticias
        try:
            noticias[titulo]["mostrar"] = True
            Sesion.guardar_datos_noticias()
            Sesion.cargar_datos_noticias()

        except:
            print("La noticia ya fue rechazada o aceptada.") #FALTA UN LABEL O ALGO

    #Rechaza la noticia.
    def RechazarNoticia(self, titulo):
        global noticias
        try:
            del noticias[titulo]
            Sesion.guardar_datos_noticias()
            Sesion.cargar_datos_noticias()
        except:
            print("La noticia ya fue rechaza o aceptada.") #FALTA UN LABEL

    #Publica el evento seleccionado.
    def AceptaEvento(self, titulo):
        global eventos
        try:
            eventos[titulo]["mostrar"] = True
            Sesion.guardar_datos_eventos()
            Sesion.cargar_datos_eventos()
        except:
            print("El evento ya fue rechazado o aceptado.") #FALTA un label

    #Rechaza el Evento.
    def RechazarEvento(self, titulo):
        global eventos
        try:
            del noticias[titulo]
            Sesion.guardar_datos_eventos()
            Sesion.cargar_datos_eventos()

        except:
            print("El evento ya fue rechazado o aceptado.") #Falta un label


    #Banea usuario que publico la noticia.
    def BanearUsuario(self, usuario, frame):
        global usuarios
        try:
            del usuarios[usuario] #Tal vez sea mejor crear un registro para saber si el usuario ya esta baneado y que le salte una alerta.
            Sesion.guardar_datos_usuarios()
            Sesion.guardar_datos_usuarios()
        except:
            print("Usuario no encontrado.") #Falta un label.



def opciones_universales(self):
    self.root.geometry(TAMANO_VENTANA)
    self.root.title("NotiAlarm")
    self.root.resizable(False, False)
    
    currentPath = os.path.dirname(os.path.realpath(__file__))
    imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 680))
    imagenLabel = ctk.CTkLabel(self.root, image=imagenFondo, text="")
    imagenLabel.place(relx=0, rely=0)


class Sesion: #Maneja los datos se Sesión.
    def cargar_datos_usuarios(): #Carga el archivo anterior con los usuarios existentes.
        global usuarios
        try:
            with open("usuarios.json", "r") as archivo:
                usuarios.update(json.load(archivo)) #Actualiza el diccionario usuarios con los valores de usuario.json, para eso sirve el .update y load
        except:
            print("Archivo no encontrado, se creara con un usuario admin.")
            usuarios["admin"] = {"contrasena": "12345", 
                                 "rol": "admin", 
                                 "correo": "admin"} #Creara el usuario "admin" con el rol admin y la contraseña 12345.
            Sesion.guardar_datos_usuarios() #Llama el metodo para guardar los datos nuevos.


    def guardar_datos_usuarios(): #Guarda los nuevos registros de usuarios.
        try: #Primero intenta escribir sobre el json de usuarios.
            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo) #Dump sirve para "tirar" o guardar los datos en el archivo ya leído "usuarios.json"
        except FileNotFoundError: #En caso de no encontrar el json, avisa y crea el archivo.
            print("Archivo no encontrado, se creara uno nuevo para los usuarios.")
            usuarios["admin"] = {"contrasena": "12345",
                                "rol": "admin", 
                                "correo": "admin"} #Creara el usuario "admin" con el rol admin y la contraseña 12345.
            
    def cargar_datos_noticias(): #Carga el archivo anterior con las noticias existentes.
        global noticias
        try:
            with open("noticias.json", "r") as archivo:
                noticias.update(json.load(archivo)) #Actualiza el diccionario noticias con los valores de usuario.json, para eso sirve el .update y load
        except:
            print("Archivo de noticias no encontrado, se creara uno nuevo.")

    def guardar_datos_noticias(): #Guarda los nuevos registros de las noticias
        try: #Primero intenta escribir sobre el json de noticias
            with open("noticias.json", "w") as archivo:
                json.dump(noticias, archivo) #Dump sirve para "tirar" o guardar los datos en el archivo ya leído "noticias.json"
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

#Cargar datos previos.
Sesion.cargar_datos_usuarios() 
Sesion.cargar_datos_noticias()
Sesion.cargar_datos_eventos()

#Al iniciar el programa revisa si algun evento ya ocurrio.
Sesion.comprobar_fecha_eventos()

ventana_opciones = VentanaOpciones() # abre la ventana principal

#Guardar datos.
Sesion.guardar_datos_usuarios()
Sesion.guardar_datos_noticias()
Sesion.guardar_datos_eventos()





print("Comprobar usuarios del json", usuarios) #FALTA borrar esto al final del programa.
