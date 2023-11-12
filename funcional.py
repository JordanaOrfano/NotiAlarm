import json #Para trabajar con archivos .json y guardar datos de forma permanente.
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os

ctk.set_appearance_mode("dark") # tema oscuro

usuarios = {}
noticias = {}

TAMANO_VENTANA = "1100x680"
BTN_ALTURA = 36
BTN_ANCHO = 290
TITULOS_FUENTE = "Roboto", 32

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
        ventana_invitado = VentanaInvitado()


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

        registrar = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Registrarse", command = self.registro_evento)
        registrar.place(relx=0.5, rely=0.61, anchor=tk.CENTER)

        volver = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Volver", fg_color="transparent", hover=False, command=self.abrir_ventana_opciones)
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
    
    def registro_evento(self): #Al darle click a registrar se iniciara este metodo, se crea la variable alerta para luego eliminar labels.
        
        if self.nombre.get() not in usuarios: #Comprueba que el nombre no exista previamente, si no existe ejecuta.
            if len(self.correo.get().strip()) != 0 and len(self.nombre.get().strip()) != 0 and len(self.contrasena.get().strip()) != 0: #chequea que ningun campo este vacio. #falta comprobar gmail
                if "@" in self.correo.get():
                    if VentanaRegistro.comprobar_correo(self.correo.get()):
                        if len(self.contrasena.get()) >= 8 and len(self.contrasena.get()) <20: #Comprueba que la contraseña tenga mas de 7 digitos y tenga al menos 20 digitos.
                            if any(char.isdigit() for char in self.contrasena.get()): #Comprueba que la contraseña tenga al menos un numero.
                                if any(char in "!@#$%∧&*(._-)" for char in self.contrasena.get()): #Comprueba si la contraseña tiene digitos especiales
                                    usuarios[self.nombre.get()] = {"contrasena": self.contrasena.get(), "rol": "usuario", "correo": self.correo.get()} #De forma predeterminada cualquier usuario nuevo tendrá el rol "usuario", donde no tiene grandes permisos.
                                    Sesion.guardar_datos_usuarios()
                                    VentanaRegistro.borrar_label(self.root)
                                    ctk.CTkLabel(master = self.root, text = "Usuario creado con éxito, espere unos instantes...").place(relx = 0.37, rely = 0.72) 
                                    #FALTA, aca deberia volver al login y iniciar sesion.
                                else:
                                    VentanaRegistro.borrar_label(self.root)
                                    ctk.CTkLabel(master = self.root, text = "La contraseña debe tener al menos un caracter especial '!@#$%∧&*(._-)'. ").place(relx = 0.31, rely = 0.72) 
                            else:
                                VentanaRegistro.borrar_label(self.root) 
                                ctk.CTkLabel(master = self.root, text = "La contraseña debe tener al menos un numero. ").place(relx = 0.385, rely = 0.72) 
                        else:
                            VentanaRegistro.borrar_label(self.root)
                            ctk.CTkLabel(master = self.root, text = "La contraseña debe tener entre 8 y 20 caracteres.. ").place(relx = 0.385, rely = 0.72) 
                    else:
                        VentanaRegistro.borrar_label(self.root)
                        ctk.CTkLabel(master = self.root, text = "El correo electronico ya esta asociado a una cuenta.").place(relx = 0.37, rely = 0.72) 
                else:
                    VentanaRegistro.borrar_label(self.root)
                    ctk.CTkLabel(master = self.root, text = "Debes ingresar un correo electronico valido.").place(relx = 0.39, rely = 0.72) 
            else:
                VentanaRegistro.borrar_label(self.root) 
                ctk.CTkLabel(master = self.root, text = "Ningun campo deberia estar vacío.").place(relx = 0.413, rely = 0.72)
        else:
            VentanaRegistro.borrar_label(self.root)
            ctk.CTkLabel(master = self.root, text = "El nombre de usuario ya existe. ").place(relx = 0.413, rely = 0.72) 

    def borrar_label(root): #Funcion para tapar un anterior label ya creado.
        borrar = ctk.CTkLabel(master = root, text = "           ", width= 412)
        borrar.place(relx = 0.31, rely = 0.72) 

    
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
        
        login = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Iniciar sesión", command = self.login_evento)
        login.place(relx=0.5, rely=0.54, anchor=tk.CENTER)
        
        volver = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Volver", fg_color="transparent", hover=False, command=self.volver)
        volver.place(relx=0.5, rely=0.61, anchor=tk.CENTER)
        
        self.root.mainloop()
    
    def volver(self):
        self.root.destroy()
        ventana_opciones = VentanaOpciones()

    def login_evento(self): #Al tocar el boton login.
        verificar = False #Por ahora, la contraseña no coincide; Valor predeterminado.

        for usuario in usuarios: #Verifica si algun correo en el diccionario usuarios coincide con el ingresado.
            if str(self.correo.get().lower()).strip() == str(usuarios[usuario]['correo'].lower()).strip():
                if str(self.contrasena.get()) == str(usuarios[usuario]['contrasena']): #Si encuentra un correo que coincide con el ingresado, comprueba que tambien coincida la contraseña.
                    verificar = True #El correo y la contraseña coinciden.
                
        if verificar:
            VentanaLogin.borrar_label(self.root)
            ctk.CTkLabel(master = self.root, text = "Iniciando Sesión...").place(relx = 0.45, rely = 0.65) #FALTA poner pantallas de admin y de usuario.

        else:
            VentanaLogin.borrar_label(self.root)
            ctk.CTkLabel(master = self.root, text = "Correo o contraseña invalidos.").place(relx = 0.42, rely = 0.65) 

    def borrar_label(root): #Funcion para tapar un anterior label ya creado.
        borrar = ctk.CTkLabel(master = root, text = "           ", width = 265)
        borrar.place(relx = 0.38, rely = 0.65) 


class VentanaInvitado:
    def __init__(self):
        self.root = ctk.CTk()
        opciones_universales(self)
        
        frame = ctk.CTkScrollableFrame(master=self.root)
        frame.pack(pady=0, padx=260, fill="both", expand=True)
        
        # frames de los costados
        # frame2 = ctk.CTkFrame(master=self.root, width=230)
        # frame2.place(relx=0.79, rely=0, relheight=1)
        
        # -------------------- publicar -------------------
        titulo = ctk.CTkLabel(master=frame, text="(icono) NotiAlarm", justify="left", anchor="w", font=(TITULOS_FUENTE))
        titulo.pack(pady=20, padx=20, fill="x")
        
        crearFrame = ctk.CTkFrame(master=frame)
        crearFrame.pack(pady=(0,10), padx=20, fill="x")
        
        crearLabel = ctk.CTkLabel(master=crearFrame, wraplength=520, height=40, font=("",14,"bold"), fg_color="#1e1e1e", corner_radius=6, text="Crear publicación")
        crearLabel.pack(pady=0, padx=0, fill="x")
        
        crearAlarmaBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar noticia", command=self.publicarNoticia)
        crearAlarmaBtn.pack(pady=0, padx=0, fill="x", side="left")
        
        noticiaEventoBtn = ctk.CTkButton(master=crearFrame, height=BTN_ALTURA, width=258, text="Publicar evento", command=self.publicarEvento)
        noticiaEventoBtn.pack(pady=0, padx=0, fill="x", side="right")
       
        #Mostrar todas las noticias en el menú.
        try:
            if len(noticias) != 0:
                for categoria, noticias_titulos in noticias.items():
                    for noticia, det in noticias_titulos.items(): 
                        ubicacion = det["ubicacion"]
                        texto = det["contenido"]
                        usuario = "Desconocido, falta ESPECIFICAR."
                        fecha = "Falta especificar." 
                        self.mostrar_publicacion(frame, noticia, ubicacion, categoria, texto, usuario, fecha)
            else:
                ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack() 

        except:
            ctk.CTkLabel(master = frame, text = "No hay noticias para mostrar.",height=400, font=ctk.CTkFont(size=20)).pack() 
                
        # titulo = "Titulo de la noticia"
        # ubicacion = "txtubicacion"
        # categoria = "txtcategoria"
        # texto = "Tkinter Label is a widget that is used to implement display boxes where you can place text or images. The text displayed by this widget can be changed by the developer at any time you want. It is also used to perform tasks such as to underline the part of the text and span the text across multiple lines. It is important to note that a label can use only one font at a time to display text. To use a label, you just have to specify what to display in it (this can be text, a bitmap, or an image). Python offers multiple options for developing a GUI (Graphical User Interface). Out of all the GUI methods, Tkinter is the most commonly used method. It is a standard Python interface to the Tk GUI toolkit shipped with Python. Python with Tkinter is the fastest and easiest way to create GUI applications. Creating a GUI using Tkinter is an easy task using widgets. Widgets are standard graphical user interfaces (GUI) elements, like buttons and menus."
        # usuario = "Fulanito123"
        # fecha = "10/10/2023 22:10"
        
        
        self.root.mainloop()


    def publicarNoticia(self): #FALTA hacer que se obtenga el nombre del que publica
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm")
        publicarVentana.geometry("650x470")
        publicarVentana.resizable(False, False)
        
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

        #Elegir entre Alarma o Noticia
        self.switch_var = ctk.StringVar(value="off")
        self.switch = ctk.CTkSwitch(master=publicarFrame, text="Alerta", variable=self.switch_var, onvalue="on", offvalue="off")
        self.switch.pack(pady=2, padx= 20, fill="x")


    #Al tocar el boton de publicar debera guardar la noticia en el json.
    def publicar_evento(self, publicarFrame):
        global noticias
        
        if len(self.publicarTitulo.get().strip()) != 0 and len(self.publicarUbicacion.get().strip()) != 0 and len(self.publicarTextbox.get("1.0", "end").strip()) != 0:
            
            if self.categoria.get().lower() != "categoria":

                if self.switch_var.get() == "on":
                    print("es una alerta") #FALTA aca va el codigo de leo como si fuera una alerta.
                else:
                    if self.categoria.get() in noticias: #Si ya existe la categoria que ingreso el usuario guardara la noticia y los datos en la misma.
                        if hasattr(self, "info_evento"):
                            self.info_evento.destroy()
                            
                        self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Noticia creada correctamente.")
                        self.info_evento.pack()
                        noticias[self.categoria.get()][self.publicarTitulo.get()] = {"contenido": self.publicarTextbox.get("1.0", "end"),
                                                    "autor": "desconocido FALTA especificar",
                                                    "ubicacion": self.publicarUbicacion.get()} #Atributos de las noticias FALTA añadir nombres
                        Sesion.guardar_datos_noticias()

                    else: #Si no existe esa categoria en el json, creara la categoria y guardara la noticia en este con los respectivos datos.
                        if hasattr(self, "info_evento"):
                            self.info_evento.destroy()
                            
                        self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Noticia creada correctamente.")
                        self.info_evento.pack()
                        noticias[self.categoria.get()] = {
                                self.publicarTitulo.get(): {"contenido": self.publicarTextbox.get("1.0", "end"),
                                        "autor": "desconocido",
                                        "ubicacion": self.publicarUbicacion.get()}}           #Atributos de las noticias.
                        Sesion.guardar_datos_noticias()
                
            else:
                if hasattr(self, "info_evento"):
                    self.info_evento.destroy()
                
                self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Debes seleccionar una categoria.")
                self.info_evento.pack() 

        else:
            if hasattr(self, "info_evento"):
                        self.info_evento.destroy()

            self.info_evento = ctk.CTkLabel(master = publicarFrame, text = "Ningun espacio puede estar vacio.")
            self.info_evento.pack() 

    
    def publicarEvento(self):
        publicarVentana = ctk.CTkToplevel(master=self.root)
        publicarVentana.title("NotiAlarm")
        publicarVentana.geometry("650x440")
        publicarVentana.resizable(False, False)        
        
        currentPath = os.path.dirname(os.path.realpath(__file__))
        imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 680))
        imagenLabel = ctk.CTkLabel(publicarVentana, image=imagenFondo, text="")
        imagenLabel.place(relx=0, rely=0)
        
        publicarFrame = ctk.CTkFrame(master=publicarVentana)
        publicarFrame.pack(pady=0, padx=90, fill="both", expand=True)
        
        publicarLabel = ctk.CTkLabel(master=publicarFrame, height=40,font=('Roboto', 24), text="Crear Publicación | Evento")
        publicarLabel.pack(pady=(20,15), padx=20, fill="x")
        
        publicarTitulo = ctk.CTkEntry(master=publicarFrame, height=BTN_ALTURA, placeholder_text="Título")
        publicarTitulo.pack(pady=5, padx=20, fill="x")
        
        publicarUbicacion = ctk.CTkEntry(master=publicarFrame, height=BTN_ALTURA, placeholder_text="Ubicación")
        publicarUbicacion.pack(pady=5, padx=20, fill="x")
        
        publicarTextbox = ctk.CTkTextbox(master=publicarFrame, height=140)
        publicarTextbox.pack(pady=5, padx=20, fill="x")

        categoria = ctk.CTkOptionMenu(master=publicarFrame, values=["Categoría", "option 1", "option 2"])
        categoria.pack(pady=5, padx=20, fill="x")
        
        publicarBoton = ctk.CTkButton(master=publicarFrame, height=BTN_ALTURA, text="Publicar")
        publicarBoton.pack(pady=5, padx=20, fill="x")
    
    
    def mostrar_publicacion(self, frame, titulo, ubicacion, categoria, texto, usuario, fecha): # creacion de publicacion
        color = "#1e1e1e"
        noticiaFrame = ctk.CTkFrame(master=frame, fg_color="#262626")
        noticiaFrame.pack(pady=10, padx=20, fill="x")
        
        noticiaTitulo = ctk.CTkLabel(master=noticiaFrame, wraplength=520, height=40, corner_radius=6, font=("",14,"bold"), fg_color=color, text=titulo)
        noticiaTitulo.pack(pady=0, padx=0, fill="x")
        
        noticiaTexto = ctk.CTkLabel(master=noticiaFrame, justify="left", anchor="w", wraplength=485, text=f"Ubicación: {ubicacion}\n\nCategoría: {categoria}\n\n{texto}")
        noticiaTexto.pack(pady=14, padx=20, fill="x", expand=True)
        
        noticiaInfoFrame = ctk.CTkFrame(master=noticiaFrame, fg_color=color, corner_radius=6)
        noticiaInfoFrame.pack(pady=0, padx=0, fill="x")

        noticiaInfo = ctk.CTkLabel(master=noticiaInfoFrame, justify="left", anchor="w", corner_radius=6, wraplength=520, text=f"{usuario}\n{fecha}")
        noticiaInfo.pack(pady=0, padx=20, side="left")
        
        noticiaBorrar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Borrar")
        noticiaBorrar.pack(pady=0, padx=0, side="right")

        noticiaEditar = ctk.CTkButton(master=noticiaInfoFrame, width=50, height=40, text="Editar")
        noticiaEditar.pack(pady=0, padx=1, side="right")


class VentanaNoticias:
    def __init__(self):
        self.root = ctk.CTk() # inicializa
        opciones_universales(self)
     
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)


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

#Cargar datos previos.
Sesion.cargar_datos_usuarios() 
Sesion.cargar_datos_noticias()

ventana_opciones = VentanaOpciones() # abre la ventana principal

#Guardar datos.
Sesion.guardar_datos_usuarios()
Sesion.guardar_datos_noticias()


print("Comprobar usuarios del json", usuarios)
