from Config.Token import *
from Config.Driver import *
import requests,shutil,os,time,threading,pickle
from bs4 import BeautifulSoup
#Librerias para el trabajo con selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

#Funcion para buscar los elementos y llenar la variable global lista
def find_title(find):
    cid = find.from_user.id
    lista_names = [];all_urls = []
    name_title = str(find.text).replace(' ','+')
    #condicional para saber que busqueda realizar dependiendo del genero
    if name_title.lower().startswith('#gay'):
        res = requests.get(URL(1)+name_title.replace('#gay+',''),headers=HEADERS)
        files.title_find(URL(1)+name_title.replace('#gay+',''),cid) 
    elif name_title.lower().startswith('#trans'):
        res = requests.get(URL(2)+name_title.replace('#trans ',''),headers=HEADERS)
        files.title_find(URL(2)+name_title.replace('#trans+',''),cid)
    else:
        res = requests.get(URL(0)+name_title,headers=HEADERS)
        files.title_find(URL(0)+name_title,cid)
    soup = BeautifulSoup(res.text,"html.parser")  
    names = soup.find_all("div",class_="thumb-under")
    for name in names:  
        url_namev1 = name.find("a").attrs.get("href")
        url_name = str(url_namev1.split('/')[2]).strip('\n')
        url_name = (url_name.replace("_"," ").replace("."," ")) 
        #Condicional para garantizar que los resultados tienen nombre correcto
        if not url_name == 'THUMBNUM' and not url_name in lista_names:
            all_urls.append(url_namev1)
            lista_names.append(url_name)
    files.save_title(lista_names,find.chat.id)
    files.save_url(all_urls,find.chat.id)

#Funcion para descargar la foto que seleccione el usuario
def find_photo(pos,cid):
    #Abrimos el archivo con el titulo para pasarselo al url
    name_title = files.show_title(cid)
    lista = files.list_names(cid)
    res = requests.get(name_title,headers=HEADERS)
    soup = BeautifulSoup(res.text,"html.parser")
    photos = soup.find_all("div",class_="thumb")
    photo_url = photos[pos].find("img").attrs.get("data-src") 
    res_photo = requests.get(photo_url,stream=True)
    with open(os.getcwd()+f'/photos/{cid}.jpg', 'wb') as file:
        res_photo.raw.decode_content = True
        shutil.copyfileobj(res_photo.raw, file) 
    title = f'<b>{lista[pos]}</b>\n<b>Descargar: </b><code>/descargar {pos+1}</code>'
    try:
        def del_mesg(cid,msg_id):
            time.sleep(15)
            bot.delete_message(cid,msg_id)
        msg = bot.send_photo(cid,open(os.getcwd()+f'/photos/{cid}.jpg', 'rb'),caption=title,parse_mode='html')
        erase_photo = threading.Thread(target=del_mesg(cid,msg.message_id))
        erase_photo.start()
    except:
        mess_aux = bot.send_message(cid,'<b>Error de conexion al cargar</b>',parse_mode='html')
        time.sleep(2)
        bot.delete_message(cid,mess_aux.message_id)

#Completar funcion
def download_video(find,cid):
    #Instanciamos el navegador
    Firefox = Driver()
    driver = Firefox.run_firefox()
    wait = WebDriverWait(driver,20)
    url = files.read_url(cid)[find]
    driver.get(url)
    download = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,'a[title="Descarga"]')))
    download.click()
    user_name = wait.until(ec.element_to_be_clickable((By.ID,'signin-form_login')))
    user_name.send_keys('astrorealbissnes@gmail.com')
    pass_name = wait.until(ec.element_to_be_clickable((By.ID,'signin-form_password')))
    pass_name.send_keys('Omega-666')
    login = wait.until(ec.element_to_be_clickable((By.CLASS_NAME,'login-submit')))
    login.click()
    cookie = driver.get_cookies()
    pickle.dump(cookie, open('cookie.cok','wb')) 

