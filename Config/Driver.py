from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

class Driver():
    path = '/home/rool/.wdm/drivers/geckodriver/linux64/v0.33.0/geckodriver' 
    def __init__(self,visual=False) -> None:
        self.__visual = visual

    def run_firefox(self):  
        #Direccion del driver de Firefox
        options = Options()
        options.add_argument('--disable-extensions')#Desabilita las extenciones del navegador
        options.add_argument('--disable-notifications')#Desabilita las notificaciones
        options.add_argument('--ignore-certificate-errors')#Ignora los certificados de error
        options.add_argument('--no-sandbox')#Ni puta idea
        options.add_argument('--allow-running-insecure-contet')#Abre sin verificar la seguridad de la pagina
        options.add_argument('--no-first-run')#Evitar las tareas de inicializacion
        options.add_argument('--no-proxy-server')#Confirma que no existe un server proxi intermedio
        options.add_argument('--lang=es')#Selecciona el idioma del navegador
        if self.__visual:
            options.add_argument('--headless')#No muestra el navegador
        service = Service(executable_path=self.path)
        driver = webdriver.Firefox(service=service,options=options)
        return driver
