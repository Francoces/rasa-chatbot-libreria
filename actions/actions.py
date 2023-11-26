# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from asyncio.windows_events import NULL
from re import I
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json
import os
#import Cuentas
#from Cuentas import guardar_datos, cargar_datos, buscar_persona
from swiplserver import PrologMQI






# ///////////////////ARBOL//////////////////////////////

import pandas as  pd


from sklearn.tree import DecisionTreeClassifier
from sklearn import tree


import graphviz


csv = "C:/BOT LIBRERIA EXPLORATORIA/recomendar_libro_csv.csv"

df = pd.read_csv(csv)

# Imprimimos 5 filas aleatorias
print("5 EJEMPLOS DE LOS DATOS....................................................")
print(df.sample(5))
print("INFORMACION DEL DATASET....................................................")
print(df.info())


x = df.drop(columns='libro_que_le_gusta')     # features
y = df['libro_que_le_gusta'] 

print("DATASET DE LOS FEATURES....................................................")
print(x.info())

# Creamos el modelo
model = DecisionTreeClassifier(max_depth=4)
# Entrenamos el modelo
model.fit(x,y)

# pasamos las features y el target para que nos diga que tan bien predice
print("ACCURACY DEL MODELO....................................................")
print(model.score(x, y))




## PARA PODER VISUALIZAR EL ARBOL

# conda install python-graphviz

dot_data = tree.export_graphviz(model,out_file=None, 
                      feature_names=x.columns.tolist(),  
                      class_names=df['libro_que_le_gusta'].astype(str).unique().tolist(),  
                      filled=True, rounded=True,  
                      special_characters=True) 
graph = graphviz.Source(dot_data) 

# nombre del pdf a guardar
graph.render("arbolPreview") 


tengo_un_libro = False

lista_de_libros = []





#////////////////////////////////////////





archivo = 'C:/BOT LIBRERIA EXPLORATORIA/perfiles.JSON'

lista_generos = []

lee_libros_largos = False

edad = 0

cuenta_activa = False
#/////////////////////////////////////////////////////////////////////////



def guardar_datos(data , archivo):
     

    try:
        with open(archivo, 'r') as archivo_json:
            personas = json.load(archivo_json)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        # Manejar el caso donde el archivo no existe o no es un JSON válido
        personas = []


    for data2 in personas:
        if data2["Nombre"] == data["Nombre"]:
            data2["edad"] = data["edad"]
            data2["libros_largos"] = data["libros_largos"]
            data2["Generos"] = data["Generos"]
        else:
            personas.append(data)

    with open(archivo, 'w') as archivo_json:
        json.dump(personas, archivo_json, indent=4)

    


def cargar_datos(archivo):
    if(os.path.getsize(archivo) > 0):
        try:
            with open(archivo, 'r') as archivo_json:
                personas = json.load(archivo_json)
                return personas
        except FileNotFoundError:
            return []
    else:
        return None

#usa personas de cargar datos
def buscar_persona(personas,valor):
    if(personas == None):
        return None

    for data in personas:
        if data["Nombre"] == valor:
            return data
    return None






#////////////////////////////////////////////////////






class PedirSugerencia(Action):

    def name(self) -> Text:
       return "Pedir_Sugerencia"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if(cuenta_activa):


            global lista_generos


            global lee_libros_largos
            
            global edad
            
            
            df_Accion = "1" if "'Accion'" in lista_generos else "0"
            df_Aventura = "1" if "'Aventura'" in lista_generos else "0" 
            df_Fantasia = "1" if "'Fantasia'" in lista_generos else "0" 
            df_Terror = "1" if "'Terror'" in lista_generos else "0" 
            df_Policial = "1" if "'Policial'" in lista_generos else "0" 
            df_Historia = "1" if "'Historia'" in lista_generos else "0" 
            df_Drama = "1" if "'Drama'" in lista_generos else "0"
            df_Misterio = "1" if "'Misterio'" in lista_generos else "0"
            df_Romance = "1" if "'Romance'" in lista_generos else "0"
            df_Humor = "1" if "'Humor'" in lista_generos else "0"
            df_Economia = "1" if "'Economia'" in lista_generos else "0"
            df_Psicologia = "1" if "'Psicologia'" in lista_generos else "0"
            df_Cocina = "1" if "'Cocina'" in lista_generos else "0"
            df_Religion = "1" if "'Religion'" in lista_generos else "0"
            df_Poesia = "1" if "'Poesia'" in lista_generos else "0"


            

            user_data = pd.DataFrame({
            'edad': [edad],
            'lee_libros_largos': [lee_libros_largos],  
            'Accion': [df_Accion],  
            'Aventura': [df_Aventura],  
            'Fantasia': [df_Fantasia],
            'Terror': [df_Terror],  
            'Policial': [df_Policial],
            'Historia': [df_Historia],  
            'Drama': [df_Drama],  
            'Misterio': [df_Misterio],  
            'Romance': [df_Romance],  
            'Humor': [df_Humor],
            'Economia': [df_Economia],  
            'Psicologia': [df_Psicologia],  
            'Cocina': [df_Cocina],
            'Religion': [df_Religion],  
            'Poesia': [df_Poesia], 
            })
            
            print(user_data.head())

            y_pred = model.predict(user_data)
            print(y_pred)

            dispatcher.utter_message(text=f"le recomiendo el libro: {y_pred}")


        else:
            dispatcher.utter_message(text=f"no iniciaste con ningun perfil")



        return []








class MostrarPerfil(Action):

    def name(self) -> Text:
       return "mostrar_perfil"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        if(cuenta_activa):

            nombre = tracker.get_slot("nombre")


            dispatcher.utter_message(text=f"su nombre de usuario es {nombre}")

            if (lee_libros_largos):
                dispatcher.utter_message(text=f"le gusta leer libros largos")
            else:
                dispatcher.utter_message(text=f"no le gusta leer libros largos")


            dispatcher.utter_message(text=f"estos son los generos que consulto")



            for i, genero in enumerate(lista_generos, start=1):
                            dispatcher.utter_message(text=f"{i}: {genero}") 

            
        else:
            dispatcher.utter_message(text=f"no iniciaste con ningun perfil")

        return []







class PedirPerfil(Action):

    def name(self) -> Text:
       return "Pedir_Perfil"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        personas = cargar_datos(archivo) # datos del archivo

        nombre = tracker.get_slot("nombre")

        Data = buscar_persona(personas,nombre)

        if ( Data == None):
            dispatcher.utter_message(text=f"no existe un perfil con sus datos {nombre}, quiere crear un perfil?")
        else:
            global cuenta_activa
            cuenta_activa = True
            global lista_generos
            lista_generos = Data["Generos"]
            global lee_libros_largos
            lee_libros_largos = Data["libros_largos"]
            global edad
            edad = Data["edad"]
            dispatcher.utter_message(text=f"ya cargamos los datos de su perfil {nombre}")


        return []







class GuardarPerfil(Action):

    def name(self) -> Text:
       return "Guardar_Perfil"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global lista_generos
        nombre = tracker.get_slot("nombre")

        data = {
        "Nombre": nombre,
        "edad": edad,
        "libros_largos": lee_libros_largos,
        "Generos": lista_generos
    }
        guardar_datos( data , archivo) #guardo perfil
        
        lista_generos.clear()


        return []


class ObtenerDatos(Action): # tener los datos del perfil

    def name(self) -> Text:
       return "obtener_datos"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global cuenta_activa
        cuenta_activa = True
        
        global edad
        edad = int(tracker.get_slot("edad"))

        global lee_libros_largos
        intent = Tracker.get_intent_of_latest_message()

        print(f"intent es: {intent}")

        if intent  == "affirm":
            lee_libros_largos = True
            return []
        else:
            lee_libros_largos = False
            return []
        
        







class MostarLista(Action):

    def name(self) -> Text:
       return "mostrar_lista"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

       
        valor=int(tracker.get_slot("numero")) 
        if 0 < len(lista_de_libros):

            for i, titulo in enumerate(lista_de_libros, start=1):
                dispatcher.utter_message(text=f"{i}: {titulo}") 

        else:
            dispatcher.utter_message(text=f"aun no creo ninguna lista de libros. Que tipos de libros buscas?")

        return []


class PreguntaLaPosicion(Action):

    def name(self) -> Text:
       return "pregunta_la_posicion"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        valor=int(tracker.get_slot("numero")) 
        if int(valor) <= len(lista_de_libros):
            
            valor = valor - 1
            libro = str(lista_de_libros[valor])  
            titulo =  libro   # saco titulo de la lista
            
            global tengo_un_libro
            tengo_un_libro = True
            print(lista_de_libros[valor])
            print("el libro es: "+ libro)
            print(tengo_un_libro)

        else:
            dispatcher.utter_message(text=f"la posicion esta fuera del rango de la lista.")

        return [SlotSet("nombre_libro", titulo )] #guardo titulo




class ListarPorGenero(Action):

    def name(self) -> Text:
       return "listar_por_genero"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        global tengo_un_libro
        tengo_un_libro = False #si piden otra vez regresa a null
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:/Users/Usuario/Documents/Prolog/libreria.pl').")
            
                genero = tracker.get_slot("genero")
                genero = genero.capitalize()

                genero = "'" + genero + "'"

                global lista_generos
                if genero not in lista_generos:   # AGREGA EL VALOR SI NO ESTA EN LA LISTA, EVITA REPETIDOS
                    lista_generos.append(genero)

                print(lista_generos)

                print("el genero es: "+ genero)
                result = list(prolog_thread.query(f"titulos_por_genero({genero}, Titulos)"))

                global lista_de_libros
                lista_de_libros.clear()
                for r in result:
                    lista_de_libros.extend(r["Titulos"])
                # Imprime los titulos con su posicion en la lista
                for i, titulo in enumerate(lista_de_libros, start=1):
                    dispatcher.utter_message(text=f"{i}: {titulo}")     
        return []






class VerSiExisteElLibro(Action):

    def name(self) -> Text:
       return "ver_si_existe_el_libro"      # busco si el titulo dado por el usuario existe

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:/Users/Usuario/Documents/Prolog/libreria.pl').")
            
                titulo = tracker.get_slot("nombre_libro")
                titulo = titulo.capitalize()
                titulo = "'" + titulo + "'"

                result = prolog_thread.query(f"existe_libro({titulo})")
                global tengo_un_libro
                global lista_de_libros
                lista_de_libros.clear()
                if result :
                    lista_de_libros.append(titulo)
                    dispatcher.utter_message(text=f"tenemos el libro llamado {titulo}")
                    
                    tengo_un_libro = True
                    return[SlotSet("nombre_libro", titulo ),
                           SlotSet("numero", 1 )]
                     #aseguro posicion uno por si pide sin num
                else:
                    dispatcher.utter_message(text=f"no tenemos el libro llamado {titulo}")
                    
                    tengo_un_libro = False #si piden otra vez regresa a null
       
        return []




class ImprimirTodosLosLibros(Action):

    def name(self) -> Text:
       return "imprimir_todos_los_libros"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tengo_un_libro = False #si piden otra vez regresa a null
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:/Users/Usuario/Documents/Prolog/libreria.pl').")
            


                result = list(prolog_thread.query("todos_los_libros(Titulos)"))

                global lista_de_libros
                lista_de_libros.clear()

                for r in result:
                    lista_de_libros.extend(r["Titulos"])

                # Imprime los titulos con su posicion en la lista
                for i, titulo in enumerate(lista_de_libros, start=1):
                    dispatcher.utter_message(text=f"{i}: {titulo}") 

        return []



class BuscarAutorLibro(Action):

    def name(self) -> Text:
       return "buscar_autor_libro" #das un titulo y devuelve su autor

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:/Users/Usuario/Documents/Prolog/libreria.pl').")


                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")

                    result = prolog_thread.query(f"autor_por_titulo('{titulo}', Autor)")

                    if result:
                        autor = result[0]["Autor"]
                        dispatcher.utter_message(text=f"El autor de '{titulo}' es: {autor}")
                    else:
                        dispatcher.utter_message(text=f"No se encontro informacion para el titulo '{titulo}'.")
                else:
                    dispatcher.utter_message(text=f"seleccione un libro.")

        return []



class DarLaSinopsisDelLibro(Action):

    def name(self) -> Text:
       return "dar_la_sinopsis_del_libro"   #das un titulo y devuelve su sinopsis

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:/Users/Usuario/Documents/Prolog/libreria.pl').")

                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")

                    result = prolog_thread.query(f"sinopsis_por_titulo('{titulo}', Sinopsis)")

                    if result:
                        Sinopsis = result[0]["Sinopsis"]
                        dispatcher.utter_message(text=f"sinopsis de '{titulo}': {Sinopsis}")
                    else:
                        dispatcher.utter_message(text=f"No se encontro informacion para el titulo.")
                else:
                    dispatcher.utter_message(text=f"seleccione un libro.")


        return []
    

class DarCantPaginasLibro(Action):

    def name(self) -> Text:
       return "dar_cant_paginas_libro" #das un titulo y devuelve su cant de paginas

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:/Users/Usuario/Documents/Prolog/libreria.pl').")

        
                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")

                    result = prolog_thread.query(f"paginas_por_titulo('{titulo}', Paginas)")

                    if result:
                        cant_pag = result[0]["Paginas"]
                        dispatcher.utter_message(text=f"'{titulo}' tiene {cant_pag} paginas")
                    else:
                        dispatcher.utter_message(text=f"No se encontro informacion para el titulo.")
                else:
                    dispatcher.utter_message(text=f"seleccione un libro.")


        return []
    

class DarPrecioDelLibro(Action):

    def name(self) -> Text:
       return "dar_precio_del_libro" #das un titulo y devuelve su precio

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:/Users/Usuario/Documents/Prolog/libreria.pl').")

        
                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")
                    
                    result = prolog_thread.query(f"precio_por_titulo('{titulo}', Precio)")

                    if result:
                        precio = result[0]["Precio"]
                        dispatcher.utter_message(text=f"'{titulo}' cuesta ${precio}")
                    else:
                        dispatcher.utter_message(text=f"No se encontro informacion para el titulo.")
                else:
                    dispatcher.utter_message(text=f"seleccione un libro.")

        return []
