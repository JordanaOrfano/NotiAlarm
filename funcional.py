import json #Para trabajar con archivos .json y guardar datos de forma permanente.
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import os

ctk.set_appearance_mode("dark") # tema oscuro

usuarios = {}

TAMANO_VENTANA = "1100x650"
BTN_ALTURA = 36
BTN_ANCHO = 290
TITULOS_FUENTE = "Roboto", 34

class VentanaOpciones:
    def __init__(self):
        self.root = ctk.CTk() # inicializa
        opciones_universales(self,"NotiAlarm")
     
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
        opciones_universales(self,"Registrarse")

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
    
    def registro_evento(self): #Al darle click a registrar se iniciara este metodo.
        alerta = ctk.CTkLabel(master = self.root, text = "")
        alerta.place(relx = 0.45, rely = 0.70)
        
        if self.nombre.get() not in usuarios: #Comprueba que el nombre no exista previamente, si no existe ejecuta.
            if len(self.correo.get().strip()) != 0 and len(self.nombre.get().strip()) != 0 and len(self.contrasena.get().strip()) != 0: #chequea que ningun campo este vacio. #falta comprobar gmail
                if "@" in self.correo.get():
                    if VentanaRegistro.comprobar_correo(self.correo.get()):
                        if len(self.contrasena.get()) >= 8 and len(self.contrasena.get()) <20: #Comprueba que la contraseña tenga mas de 7 digitos y tenga al menos 20 digitos.
                            if any(char.isdigit() for char in self.contrasena.get()): #Comprueba que la contraseña tenga al menos un numero.
                                if any(char in "!@#$%∧&*(._-)" for char in self.contrasena.get()): #Comprueba si la contraseña tiene digitos especiales
                                    usuarios[self.nombre.get()] = {"contrasena": self.contrasena.get(), "rol": "usuario", "correo": self.correo.get()} #De forma predeterminada cualquier usuario nuevo tendrá el rol "usuario", donde no tiene grandes permisos.
                                    Sesion.guardar_datos_usuarios()
                                    
                                    alerta.configure(text="Usuario creado con éxito, espere unos instantes...")
                                    #FALTA aca deberia volver al login y iniciar sesion.
                                else:
                                    alerta.configure(text="La contraseña debe tener al menos un caracter especial: '!@#$%∧&*(._-)'")
                            else:
                                alerta.configure(text="La contraseña debe tener al menos un número.")
                        else:
                            alerta.configure(text="La contraseña debe tener entre 8 y 20 caracteres.")
                    else:
                        alerta.configure(text="El correo electrónico ya está asociado a una cuenta.")
                else:
                    alerta.configure(text="Ingrese un correo electrónico válido.")
            else:
                alerta.configure(text="Ningún campo debe estar vacío.")
        else:
            alerta.configure(text="El nombre de usuario ya existe.")
        
    
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

        frame = ctk.CTkScrollableFrame(master=self.root, fg_color="transparent")
        frame.pack(pady=0, padx=120, fill="both", expand=True)
        
        titulo = ctk.CTkLabel(master=frame, text="acá iría sección para publicar como en fb", font=(TITULOS_FUENTE))
        titulo.pack(pady=10, padx=0)
        
        noticiaFrame = ctk.CTkFrame(master=frame)
        noticiaFrame.pack(pady=0, padx=100, fill="x")
        
        noticiaTitulo = ctk.CTkLabel(master=noticiaFrame, text="Titulo")
        noticiaTitulo.pack(pady=0, padx=0)
        
        # el texto no se muestra completo
        noticiaTexto = ctk.CTkLabel(master=noticiaFrame, justify="left", anchor="w", text="Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent ultrices est et nisi ultricies, ac congue justo commodo. Sed magna neque, posuere nec sem non, venenatis accumsan purus. Duis dictum tincidunt ipsum, nec sollicitudin eros condimentum ornare. In condimentum, nunc nec convallis varius, sapien nisi condimentum tortor, ac porta ligula felis vitae velit. Aenean placerat augue lorem, sed aliquam mi vulputate ullamcorper. Fusce a ligula quis leo volutpat varius. Nunc mattis maximus eros, ut tristique ante euismod vitae. Suspendisse dapibus laoreet velit, vitae volutpat enim ultrices vel. Donec in faucibus tellus, sit amet finibus orci. Cras dapibus arcu vel orci mattis, vitae ullamcorper magna hendrerit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;")
        noticiaTexto.pack(pady=10, padx=10, fill="both")

        # modificar
        noticiaEditar = ctk.CTkButton(master=noticiaFrame, width=BTN_ANCHO, height=BTN_ALTURA, text="Editar")
        noticiaEditar.pack(padx=0, side="left", fill="both", expand=True)
        noticiaBorrar = ctk.CTkButton(master=noticiaFrame, width=BTN_ANCHO, height=BTN_ALTURA, text="Borrar")
        noticiaBorrar.pack(padx=0, side="right", fill="both", expand=True)
        
        # noticiaEditar = ctk.CTkButton(master=noticiaFrame, width=50, height=BTN_ALTURA, text="Editar")
        # noticiaEditar.pack(padx=0, side="right", fill="both")
        # noticiaBorrar = ctk.CTkButton(master=noticiaFrame, width=50, height=BTN_ALTURA, text="Borrar")
        # noticiaBorrar.pack(padx=0, side="right", fill="both")
        
        login = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Iniciar sesión")
        login.pack(pady=120, padx=120, fill="both", expand=True)
        login = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Iniciar sesión")
        login.pack(pady=120, padx=120, fill="both", expand=True)
        login = ctk.CTkButton(master=frame, width=BTN_ANCHO, height=BTN_ALTURA, text="Iniciar sesión")
        login.pack(pady=120, padx=120, fill="both", expand=True)

        self.root.mainloop()


class VentanaNoticias:
    def __init__(self):
        self.root = ctk.CTk() # inicializa
        opciones_universales(self,"NotiAlarm")
     
        frame = ctk.CTkFrame(master=self.root)
        frame.pack(pady=0, padx=300, fill="both", expand=True)


def opciones_universales(self, nombre_ventana):
    self.root.geometry(TAMANO_VENTANA)
    self.root.title(nombre_ventana)
    self.root.resizable(False, False)
    
    currentPath = os.path.dirname(os.path.realpath(__file__))
    imagenFondo = ctk.CTkImage(Image.open(currentPath + "/img/bg_gradient.jpg"), size=(1100, 650))
    imagenLabel = ctk.CTkLabel(self.root, image=imagenFondo, text="")
    imagenLabel.place(relx=0, rely=0)




class Sesion: #IGNORAR, debe modificarse la mayoria.
    def __init__(self,nombre,contrasena): #Todo lo ingresado debera ser cambiado para que funcione con la interfaz. FALTA
        self.nombre = nombre
        self.contrasena = contrasena #FALTA MODIFICAR ESTO, al menos que creemos un objeto no es necesario el nombre y contrasena.

    # def registro():
    #     global usuarios
    #     intentos = 3

    #     while intentos != 0:
    #         nombre = input("Ingresa tu nombre: ") #FALTA INTERFAZ
    #         if not nombre.strip() or nombre in usuarios:
    #             intentos -= 1 #Resta un intento.
    #             print(f"Error, introduce un nombre valido.\nIntentos Restantes: {intentos}") #El usuario no puede introducir nombres vacíos. FALTA INTERFAZ

    #         elif intentos == 0: #Si se queda sin intentos vuelve al menu de iniciar sesión.
    #             print("Demasiados intentos erróneos, volviendo al menu...") #adaptar a interfaz FALTA
    #             return

    #         else:
    #             while intentos != 0: #Si no presenta ninguno de los errores anteriores, el programa continuara.
    #                 contrasena = input("Ingresa tu contraseña: ")
    #                 if len(contrasena) >=5 and intentos != 0: #La contraseña debe tener mas de 4 caracteres.
    #                     usuarios[nombre] = {"contrasena": contrasena, "rol": "usuario"} #De forma predeterminada cualquier usuario nuevo tendrá el rol "usuario", donde no tiene grandes permisos.
    #                     print("Usuario registrado correctamente, inicia sesión.")
    #                     Sesion.guardar_datos_usuarios()
    #                     return

    #                 else:
    #                     print(f"La contraseña debe tener 5 o mas caracteres.") #Da un mensaje de error.
    #                     intentos -= 1
    #                     print(f"Intentos restantes: {intentos}")

    # def login():
    #     global usuarios #Se usara para saber los usuarios existentes con sus respectivos roles y contraseñas.
    #     intentos = 3
    #     while intentos != 0:
    #         ingresa_usuario = input("\nIngresa tu nombre de usuario: ")
    #         if ingresa_usuario in usuarios: #Si el nombre ingresado por el usuario se encuentra en usuarios continuara con el código.
    #             ingresa_contrasena = input("Ingresa tu contraseña: ")
    #             if usuarios[ingresa_usuario]["contrasena"] == ingresa_contrasena: #¿La contraseña coincide con el nombre de usuario? si es asi el usuario accede.
    #                 rol = usuarios[ingresa_usuario]["rol"]
    #                 return rol #Devolvemos el rol para hacer otra verificación en el programa principal, para evitar que si iniciaste y luego cerras sesión otro usuario pueda ingresar como administrador.

    #             elif intentos == 0:
    #                 print("Demasiados intentos fallidos, volverás al menu.")
    #                 print("Si el problema persiste contacta a un operador.")
    #                 break

    #             else: #La contraseña es invalida.
    #                 print()
    #                 print("Contraseña invalida, vuelve a introducirla.")
    #                 intentos -= 1
    #                 print(f"Intentos restantes: {intentos}")

    #         else: #Si no se encuentra el usuario pedirá otro.
    #             print("Usuario no encontrado, introduce uno valido.")
    #             intentos -= 1
    #             print(f"Intentos restantes: {intentos}")

    def invitado(self): #FALTA
        self.permisos = ["ver"] #SE QUITAN ESTOS PERMISOS

    def cargar_datos_usuarios(): #Carga el archivo anterior con los usuarios existentes.
        global usuarios
        try:
            with open("usuarios.json", "r") as archivo:
                usuarios.update(json.load(archivo)) #Actualiza el diccionario usuarios con los valores de usuario.json, para eso sirve el .update y load
        except:
            print("Archivo no encontrado, se creara con un usuario admin.")
            usuarios["admin"] = {"contrasena": "12345", 
                                 "rol": "admin", 
                                 "correo": "Unknown"} #Creara el usuario "admin" con el rol admin y la contraseña 12345.
            Sesion.guardar_datos_usuarios() #Llama el metodo para guardar los datos nuevos.

    def guardar_datos_usuarios(): #Guarda los nuevos registros de usuarios.
        try: #Primero intenta escribir sobre el json de usuarios.
            with open("usuarios.json", "w") as archivo:
                json.dump(usuarios, archivo) #Dump sirve para "tirar" o guardar los datos en el archivo ya leído "usuarios.json"
        except FileNotFoundError: #En caso de no encontrar el json, avisa y crea el archivo.
            print("Archivo no encontrado, se creara uno nuevo para los usuarios.")
            usuarios["admin"] = {"contrasena": "12345",
                                "rol": "admin", 
                                "correo": "Unknown"} #Creara el usuario "admin" con el rol admin y la contraseña 12345.


Sesion.cargar_datos_usuarios()

ventana_opciones = VentanaOpciones() # abre la ventana principal

print("Comprobar usuarios del json", usuarios)