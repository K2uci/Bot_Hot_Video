import os,time
#Clase para manejar el trabajo con archivos
class Save_Files():

    def __init__(self,path=os.getcwd()+f'/data/'):
        self.path = path

    #Creamos una carpeta desiganada a ese usuario
    def mkdir_user(self,uid):
        if not os.path.isdir(self.path+f'{uid}'):
            os.mkdir(self.path+f'{uid}')

    #Funcion para guardar la busqueda de cada usuario
    def save_title(self,list_title,uid):
        #Guardamos en dicha carpeta el resultado de la busqueda de el usuario
        with open(os.getcwd()+f'/data/{uid}/names.txt','w') as file:
            for title in list_title:
                file.write(title+'\n')

    #Funcion para saber si existe el archivo de la lista del usuario
    def exist_list(self,cid):
        if os.path.isfile(path=self.path+f'{cid}/names.txt'):
            return True
        else:
            return False      

    #Funcion para retonar todos los elementos de la lista
    def list_names(self,cid):
        with open(os.getcwd()+f'/data/{cid}/names.txt','r') as file:
            list_names = file.readlines();list = []
            for name in list_names:
                correct_name = name.strip()
                list.append(correct_name)
        return list

    #Funcion para borrar busquedas anteriores
    def remove_list(self,cid):
        try:
            os.remove(path=self.path+f'{cid}/names.txt')
        except:
            pass

    #Funcion para crear la pagina de cada usuario en cero
    def ini_page(self,cid):
        with open(os.getcwd()+f'/data/{cid}/page','w') as file:
            file.write('0')

    #Funcion para conocer la pagina actual de cada usuario
    def pos_page(self,cid):
        with open(os.getcwd()+f'/data/{cid}/page','r') as file:
            return int(file.readline())
        
    #Funcion para modificar la pagina actual de cada usuario hacia arriba
    def mov_down_page(self,cid):
        actual = self.pos_page(cid)
        with open(os.getcwd()+f'/data/{cid}/page','w') as file: 
            file.write(str(actual-10))

    #Funcion para modificar la pagina actual de cada usuario hacia abajo
    def mov_up_page(self,cid):
        actual = self.pos_page(cid)
        with open(os.getcwd()+f'/data/{cid}/page','w') as file:
            file.write(str(actual+10))
    
    #Funcion para crear el titulo de busqueda
    def title_find(self,title,cid):
        with open(os.getcwd()+f'/data/{cid}/title','w') as file:
            file.write(title)

    #Funcion para leer el titulo de busqueda
    def show_title(self,cid):
        with open(os.getcwd()+f'/data/{cid}/title','r') as file:
            return str(file.readline())
        
    #Funcion para guardar todas las urls 
    def save_url(self,urls_names,cid):
        with open(os.getcwd()+f'/data/{cid}/url','w') as file:
            for url in urls_names:
                file.write('https://www.xnxx.com'+url+'\n')

    #Funcion para leer todas las urls 
    def read_url(self,cid):
        with open(os.getcwd()+f'/data/{cid}/url','r') as file:
            urls_names = file.readlines();list_ = []
            for url in urls_names:
                list_.append(url.strip())
        return list_