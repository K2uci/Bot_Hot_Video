from Config.Token import *
from Config.Scrap import *
import time
from telebot.types import ForceReply,InlineKeyboardButton,InlineKeyboardMarkup

"""

Bot encargado de recolectar toda la informacion que el usuario desee buscar en la pagina XNXX
Desarrollo al 60%
Problemas por resolver:
1-Como descargar videos de internet
2-Agregar mas funcionalidades

"""

#Funcion para mostrar resultados de la busqueda
def show_find(page_ini,cid,msg_old=None):
    lista = files.list_names(cid)
    #Muestra un error si en la busqueda se encuentra un comando
    if files.show_title(cid).startswith('/'):
        mes_aux = bot.send_message(cid,'<b>Error interno:Comando detectado en la busqueda</b>',parse_mode='html')
        time.sleep(3)
        bot.delete_message(cid,mes_aux.message_id)
        return 1
    #Muestra un error si los resultados son inferires a 10
    elif len(lista) < 10:
        mes_aux = bot.send_message(cid,'<b>Error interno:Resultados Insuficientes</b>',parse_mode='html')
        time.sleep(3)
        bot.delete_message(cid,mes_aux.message_id)
        return 1    
    mensaje = f'<b>Resultados de la busqueda: {int(len(lista)/10)*10}</b>\n'
    mensaje+= f'<b>Pagina {page_ini+1} a la {page_ini+10}:</b>\n'
    for item in lista[page_ini:page_ini+10]:
        #Condicional para buscar solamente hasta el elemento 30 de la pagina
        if int(page_ini) <= 30:
            try:
                mensaje+=f'<b>{lista.index(item)+1}</b>. {item}\n'
            except:
                continue
        else:
            break
    #Botones para visualizar paginas
    markup = InlineKeyboardMarkup(row_width=5)
    atras = InlineKeyboardButton("⏪",callback_data='atras')
    adelante = InlineKeyboardButton("⏩",callback_data='adelante')
    cerrar = InlineKeyboardButton("❌",callback_data='cerrar')
    b1 = InlineKeyboardButton(f'{page_ini+1}',callback_data=f'chose_{page_ini+1}')
    b2 = InlineKeyboardButton(f'{page_ini+2}',callback_data=f'chose_{page_ini+2}')
    b3 = InlineKeyboardButton(f'{page_ini+3}',callback_data=f'chose_{page_ini+3}')
    b4 = InlineKeyboardButton(f'{page_ini+4}',callback_data=f'chose_{page_ini+4}')
    b5 = InlineKeyboardButton(f'{page_ini+5}',callback_data=f'chose_{page_ini+5}')
    b6 = InlineKeyboardButton(f'{page_ini+6}',callback_data=f'chose_{page_ini+6}')
    b7 = InlineKeyboardButton(f'{page_ini+7}',callback_data=f'chose_{page_ini+7}')
    b8 = InlineKeyboardButton(f'{page_ini+8}',callback_data=f'chose_{page_ini+8}')
    b9 = InlineKeyboardButton(f'{page_ini+9}',callback_data=f'chose_{page_ini+9}')
    b10 = InlineKeyboardButton(f'{page_ini+10}',callback_data=f'chose_{page_ini+10}')  
    markup.add(b1,b2,b3,b4,b5,b6,b7,b8,b9,b10,atras,cerrar,adelante)    
    if not msg_old:
        bot.send_message(cid,mensaje,parse_mode='html',reply_markup=markup)
        time.sleep(10)
    else:
        bot.edit_message_text(message_id=msg_old,chat_id=cid,text=mensaje,parse_mode='html',reply_markup=markup)     

#Funcion para manejar las respuestas de los botones atras,adelante y cerrar
@bot.callback_query_handler(func=lambda val:True)
def bottoms_aux(call):
    cid = call.from_user.id
    mid = call.message.id

    #Funcion para respuesta del boton cerrar
    if call.data == "cerrar":
        files.ini_page(cid)
        bot.delete_message(cid,mid)
        files.remove_list(cid)
    #Funcion para respuesta del boton adelante
    elif call.data == "adelante":
        if int(int(len(files.list_names(cid))/10)*10 - (files.pos_page(cid)+10)) < 10:
            info = '<b>🤤Prueba realizar otra busqueda para mas resultados🤤</b>'
            mid_aux = bot.send_message(cid,info,parse_mode='html')
            time.sleep(3)
            bot.delete_message(cid,mid_aux.message_id)
            return               
        files.mov_up_page(cid)
        show_find(files.pos_page(cid),cid,mid)
    #Funcion para respuesta del boton atras
    elif call.data == "atras":
        if files.pos_page(cid) == 0:
            info = '<b>🫤Estas en la pagina inicial🫤</b>'
            mid_aux = bot.send_message(cid,info,parse_mode='html')
            time.sleep(3)
            bot.delete_message(cid,mid_aux.message_id)
            return 
        files.mov_down_page(cid)
        show_find(files.pos_page(cid),cid,mid)
    #Funcion para respuesta a las elecciones
    elif str(call.data).startswith('chose_'):
        chose = int(str(call.data).split('_')[-1])-1
        find_photo(chose,cid)
        
#Funcion para descargar los videos INCOMPLETA
@bot.message_handler(commands=['descargar'])
def descargar(message):
    #Condicional para saber si existe la lista
    if files.exist_list(message.chat.id):
        #Exepcion para capturar el numero del video a descargar
        try:
            ans = int(str(message.text).split()[1])
            #Condicional para saber si el usuario usa buscar fuera de rango
            if 0 > ans or ans > 30:
                mes_aux = bot.send_message(message.chat.id,'Error intero:Fuera de rango')
                time.sleep(3)
                bot.delete_message(message.chat.id,mes_aux.message_id)
                return
            else:
                download_video(ans-1,message.chat.id)
        #Condicional para saber si el usuario usa buscar con un caracter extrano
        except:
            mes_aux = bot.send_message(message.chat.id,'Error intero:Valor Incorrecto')
            time.sleep(3)
            bot.delete_message(message.chat.id,mes_aux.message_id) 
            return  
    #Condicional para saber si el usuario quiere descargar sin antes buscar
    else:
        mes_aux = bot.send_message(message.chat.id,'Debes realizar primero una busqueda')
        time.sleep(3)
        bot.delete_message(message.chat.id,mes_aux.message_id)
        return

#Funcion para inicializar el bot
@bot.message_handler(commands=['start'])
def start(message):
    messa_ini = '<b>   🇨🇺 !!Bienvenido a FreePorn!! 🇨🇺</b>\n\nSoy tu bot '
    messa_ini += 'de descargas calientes y mi unica mision es lograr tu extasis,para ello te '
    messa_ini += 'explico como:\n\n1-> Usa /buscar para filtrar tu peticion\n2-> Una vez tengas '
    messa_ini += 'lo que buscas utiliza /descargar <b>#</b> para bajartelo de forma gratuita.'
    messa_ini += '\nTambien puedo realizar busquedas no convencionales por ti 😉,si usas '
    messa_ini += '<i>#gay</i> o <i>#trans</i> te puedo sorprender.\n'
    messa_ini += '<b>Ejemplo:</b><code> #gay Chicos coquetos</code>'
    bot.send_message(message.chat.id,messa_ini,parse_mode='html')
    
#Funcion para buscar videos en la pagina XNXX
@bot.message_handler(commands=["buscar"])
def cmd(message):
    #Creamos la carpeta para el usuario trabajar
    files.mkdir_user(message.chat.id)
    files.remove_list(message.chat.id)
    markup = ForceReply()
    info = '😈<b>Dejame saber en que piensa esa mente sucia</b>😈'
    msg = bot.send_message(message.chat.id,info,reply_markup=markup,parse_mode='html')
    bot.register_next_step_handler(msg,find_title)
    #Comprobamos si ha realizado busqueda ese usuario 
    while not files.exist_list(message.chat.id):
        time.sleep(1)
    time.sleep(2)
    files.ini_page(message.chat.id)
    show_find(files.pos_page(message.chat.id),message.chat.id)
        

if __name__ == "__main__":
    bot.infinity_polling()





