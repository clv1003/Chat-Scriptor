# IMPORTS
import os.path
from web.endpoints.ProcesamientoEntidadesIntents import *

'''
TRADUCIR INTENTS
@Author: Claudia Landeira

Funciones encargadas de realizar la traduccion del bloque de intents
'''


# FUNCION --> traducirIntents
# Función encargada de traducir los datos de los intents
def traducirIntents(traductor, rootdir, chat):
    if os.path.exists(rootdir + chat + '/intents'):
        print(f'')
        print("\033[91m---------------------------- INTENTS \033[0m")
        intents = getIntents(rootdir + chat, traductor.getOriginal())

        for intent in intents:
            dirs = directoriosIntent(rootdir + chat, intent[0], traductor.getOriginal())
            datos = get_json(dirs[0], dirs[1])

            if 'speech' in datos[0]['responses'][0]['messages'][0]:
                speech = datos[0]['responses'][0]['messages'][0]['speech']

                for s in speech:
                    tr_speech = traductor.traducirFrase(s)
                    editar_messages(dirs[0], s, tr_speech)

            for i in datos[1]:
                for j in i['data']:
                    if len(j) == 2:
                        text = j['text']
                        if len(text) > 0 and text != " ":
                            tr_text = traductor.traducirFrase(text)
                            editar_data(rootdir+chat, intent[0], text, 'text', tr_text, traductor.getOriginal())
                    elif j['meta']:
                        text = j['text']
                        if len(text) > 0 and text != " ":
                            tr_text = traductor.traducirFrase(text)
                            editar_data(rootdir+chat, intent[0], text, 'text', tr_text, traductor.getOriginal())
            print(f"\033[92m-> OK! - Traducido intent {intent[0]}\033[0m")

            if intent[1].endswith('_usersays_' + traductor.getOriginal() + '.json'):
                nombreNuevo = intent[0].replace('.json', '') + '_usersays_' + traductor.getIdioma() + '.json'
                rutaNueva = rootdir + chat + '/intents/' + nombreNuevo
                print(f' -> Directorio: {nombreNuevo} --> {rutaNueva}')
                os.rename(dirs[1], rutaNueva)
