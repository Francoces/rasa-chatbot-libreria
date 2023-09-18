# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions



from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from swiplserver import progolMQI  
#from pyswip import Prolog   # instalar    pip install pyswip

tengo_un_libro = False

lista_de_libros = []





class PreguntaLaPosicion(Action):

    def name(self) -> Text:
       return "pregunta_la_posicion"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        
        last_message_entities = tracker.latest_message['entities']

        # Inicializamos el valor de la entidad 'numero' a None por si no se encuentra
        

        # Buscamos la entidad 'numero' en el ultimo mensaje
        for entity in last_message_entities:
            if entity['entity'] == 'numero':
                valor = entity['value']
        if valor <= len(lista_de_libros):
            self.set_slot("numero", valor) 
            valor = valor - 1
            titulo = lista_de_libros[valor]       # saco titulo de la lista
            self.set_slot("nombre_libro", titulo) #guardo titulo
            tengo_un_libro = True
            
        else:
            dispatcher.utter_message(text=f"la posicion esta fuera del rango de la lista.")

        return []




class ListarPorGenero(Action):

    def name(self) -> Text:
       return "listar_por_genero"

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        tengo_un_libro = False #si piden otra vez regresa a null
        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:\Users\Usuario\Documents\Prolog\libreria.pl')")
            
                genero = tracker.get_slot("genero")
                genero = genero.capitalize()
                genero = "'" + genero + "'"

                result = list(prolog_thread.query(f"titulos_por_genero('{genero}', Titulos)"))

                lista_de_libros.clear()
                for r in result:
                    lista_de_libros.extend(r["Titulos"])
                # Imprime los titulos con su posicion en la lista
                for i, titulo in enumerate(lista_de_libros, start=1):
                    dispatcher.utter_message(text=f"{i}: {titulo}\n")     
        return []






class VerSiExisteElLibro(Action):

    def name(self) -> Text:
       return "ver_si_existe_el_libro"      # busco si el titulo dado por el usuario existe

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:\Users\Usuario\Documents\Prolog\libreria.pl')")
            
                titulo = tracker.get_slot("nombre_libro")
                titulo = titulo.capitalize()
                titulo = "'" + titulo + "'"

                result = list(prolog_thread.query("todos_los_libros('{titulo}')"))

                lista_de_libros.clear()
                if result:
                    lista_de_libros.append(titulo)
                    dispatcher.utter_message(text=f"tenemos el libro llamado'{titulo}'")
                    tengo_un_libro = True
                    self.set_slot("nombre_libro", titulo)
                    self.set_slot("numero", 1) #aseguro posicion uno por si pide sin num
                else:
                    dispatcher.utter_message(text=f"no tenemos el libro llamado'{titulo}'")
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
                prolog_thread.query("consult('D:\Users\Usuario\Documents\Prolog\libreria.pl')")
            


                result = list(prolog_thread.query("todos_los_libros(Titulos)"))

                lista_de_libros.clear()

                for r in result:
                    lista_de_libros.extend(r["Titulos"])

                # Imprime los titulos con su posicion en la lista
                for i, titulo in enumerate(lista_de_libros, start=1):
                    dispatcher.utter_message(text=f"{i}: {titulo}\n") 

        return []



class BuscarAutorLibro(Action):

    def name(self) -> Text:
       return "buscar_autor_libro" #das un titulo y devuelve su autor

    def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        with PrologMQI(port=8000) as mqi:
            with mqi.create_thread() as prolog_thread:
                prolog_thread.query("consult('D:\Users\Usuario\Documents\Prolog\libreria.pl')")

                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")

                    result = list(prolog_thread.query(f"autor_por_titulo('{titulo}', Autor)"))

                    if result:
                        autor = list(result[0]["Autor"])
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
                prolog_thread.query("consult('D:\Users\Usuario\Documents\Prolog\libreria.pl')")

                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")

                    result = list(prolog_thread.query(f"sinopsis_por_titulo('{titulo}', Sinopsis)"))

                    if result:
                        Sinopsis = list(result[0]["Sinopsis"])
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
                prolog_thread.query("consult('D:\Users\Usuario\Documents\Prolog\libreria.pl')")

        
                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")

                    result = list(prolog_thread.query(f"paginas_por_titulo('{titulo}', Paginas)"))

                    if result:
                        cant_pag = list(result[0]["Paginas"])
                        dispatcher.utter_message(text=f"'{titulo}' tiene {cant_pag}")
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
                prolog_thread.query("consult('D:\Users\Usuario\Documents\Prolog\libreria.pl')")

        
                if tengo_un_libro == True:
                    titulo = tracker.get_slot("nombre_libro")
                    
                    result = list(prolog_thread.query(f"precio_por_titulo('{titulo}', Precio)"))

                    if result:
                        precio = list(result[0]["Precio"])
                        dispatcher.utter_message(text=f"'{titulo}' cuesta {precio}")
                    else:
                        dispatcher.utter_message(text=f"No se encontro informacion para el titulo.")
                else:
                    dispatcher.utter_message(text=f"seleccione un libro.")

        return []
