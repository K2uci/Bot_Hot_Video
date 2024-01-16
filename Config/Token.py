import telebot
from Config.Files import Save_Files

#Token del Bot actual
token = '6819418638:AAEJRUAItiUPixtt9N-T5TwMDkfqc5POsXc'

#Mi ID actual de telegram
MY_ID = '5170682276'

#Cabezeras definidas para poder navegar con requests
HEADERS = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
           "Accept-Language":"es-419,es;q=0.9"
           }
def URL(chose=0) -> str:
#Principal fuente de usqueda
    if chose == 0:
        return 'https://www.xnxx.com/search/'
    elif chose == 1:
        return 'https://www.xnxx.com/search/gay/'
    elif chose == 2:
        return 'https://www.xnxx.com/search/shemale/'


#Instancia del bot en telegram
bot = telebot.TeleBot(token)

#Clase para trabajar con los Ficheros
files = Save_Files()
