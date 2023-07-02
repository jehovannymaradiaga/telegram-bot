# Importación de la variable que contiene el TOKEN DE acceso al bot de Telegram
from src.config import *
from src.jm_shoes_bot import ShoeStoreBot
# Importación de la libreria de telebot para darle funcionalidad al bot

bot_token = TELEGRAM_TOKEN


if __name__ == '__main__':
    print('Bot Iniciado')
    # Crear una instancia del bot y pasar el token del bot de Telegram
    bot = ShoeStoreBot(bot_token)

    # Iniciar el bot
    bot.start()

    print('Fin')