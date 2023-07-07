# Libreria para interactuar con la API de telegram
import telebot
# Clases que se utilizan para crear un reclado de respuesta personalizado
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from src.catalogo import catalogo
from src.ofertas import ofertas

# Define la clase de la tienda con la logica del chatbot
class ShoeStoreBot:

    # Constructor de la clase que recibe el token de acceso, carga los botones al menu
    def __init__(self, token):
        self.bot = telebot.TeleBot(token) # Intancia de la clase telebot con el token de acceso para interactuar con la API de telegram
        self.menu_markup = ReplyKeyboardMarkup(row_width=2) # Instancia para crear un teclado personalizado de respuesta
        self._create_menu() # Llamado a la función que crea el menu que carga los botones

    def _create_menu(self):
        boton_catalogo = KeyboardButton("Ver catálogo") # Creación de los botones del menu
        boton_ofertas = KeyboardButton("Ver ofertas")
        boton_contacto = KeyboardButton("Contacto")
        boton_ayuda = KeyboardButton("Ayuda")
        self.menu_markup.add(boton_catalogo, boton_ofertas, boton_contacto, boton_ayuda) # Cargando los botones al teclado personalizado


    # Función principal que se llama iniciar la clase del chatbot
    def start(self):
        # Decorador para responder al comando de inicio con el mensaje de bienvenida
        @self.bot.message_handler(commands = ["start"])
        def send_menu(message):
            welcome = "\nBienvenido a la tienda Aesthetic Shoes\n\n"
            welcome += "Contamos con los mejores precios del mercado, así que no te pierdas nuestras grandes ofertas\n\n"
            welcome += "Puedes navegar por el siguiente menú: "
            self.bot.send_message(message.chat.id, welcome, reply_markup = self.menu_markup)

        # Decorador para respondes con un mensaje al comando de finalizar
        @self.bot.message_handler(commands = ["finalizar"])
        def send_message_final(message):
            self.bot.send_message(message.chat.id, "\nGracias por visitarnos, esperamos que vuelva pronto\n")

        # Decorador para respoder a mensajes de texto
        @self.bot.message_handler(content_types="text")
        def handle_menu_options(message):
            # Opcion para enviar el catalogo de fotos
            if message.text == "Ver catálogo":
                # Funcion para indicar que el bot esta escribiendo
                self.bot.send_chat_action(message.chat.id, 'typing')
                # Enviar las fotos como respuesta
                for key, foto in catalogo.items():
                    with open(foto['ruta'], "rb") as photo_file:
                        self.bot.send_photo(message.chat.id, photo_file, caption=foto['descripcion'])
            
            # Opcion para enviar los zapatos que estan en oferta
            elif message.text == "Ver ofertas":
                self.bot.send_chat_action(message.chat.id, 'typing')
                # Enviar las fotos como respuesta
                for key, foto in ofertas.items():
                    with open(foto['ruta'], "rb") as photo_file:
                        self.bot.send_photo(message.chat.id, photo_file, caption=foto['descripcion'])

            # Opcion para enviar informacion de contacto
            elif message.text == "Contacto":
                contacto_text = "Puedes contactarnos en los siguientes medios:\n\n"
                contacto_text += "Email: info@tiendazapatos.com\n"
                contacto_text += "Teléfono: +123456789\n"
                contacto_text += "Sitio web: www.tiendazapatos.com"
                self.bot.reply_to(message, contacto_text)
            
            # Opcion para mostrar ayuda acerca de lo que el chatbor puede hacer
            elif message.text == "Ayuda":
                ayuda = "Esta es la sección de ayuda: \n\n"
                ayuda += "Para ver los zapatos disponibles debes dar clic en ver catalogo\n"
                ayuda += "Para visualizar los zapatos que estan disponibles en oferta dar clic en ver ofertas\n"
                ayuda += "Para ver la información de contacto debes dar clic en contacto"
                ayuda += "Si quieres desplegar la opción de ayuda deber dar clic en ayuda"
                self.bot.reply_to(message, ayuda)

            # Opción para responder a mensajes que no esten contemplados en el chatbor
            else:
                self.bot.reply_to(message, "No estoy preparado para responder a estas preguntas")

            
        self.bot.polling()