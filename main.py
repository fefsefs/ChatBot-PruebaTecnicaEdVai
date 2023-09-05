# Parte 1 del código escrito por Felipe Cravero para la prueba tecnica de la ETRR
# por parte de la Escuela de datos vivos

#importo gradio para la interfaz
import gradio as gr
# importo requests para hacer pedidos a la API de OpenWeather 
import requests
# importo mi script externo para generar el chiste de de nerds por    gpt-2
from generadorDeChiste import chisteGenerar


BASEURLWEATHER = "http://api.openweathermap.org/data/2.5/weather?"
# creo el url para la request con mi api key y a que ciudad va a consultar
urlCompleto = BASEURLWEATHER + "appid=" + "Poner key para la api de OpenWeather acá" + "&q=" + "Buenos Aires"

# defino un par de listas para que el bot "interprete"
promptBasicoHola = ["Hola", "hola"]
promptBasicoComoEstas = ["¿Cómo estás?", "¿Como estas?", "Cómo estás?"]

# defino variables especificas para el comportaminto de la funcion principal
nombreUsuario = " "
flagConseguirNombre = False
flagMain = False

# defino la funcion principal, en la cual se va a basar el comportamiento del bot
def funcComportamiento(message, history) -> str:
    global flagConseguirNombre
    global flagMain 
    global nombreUsuario
    if flagConseguirNombre:
        nombreUsuario = message
        flagMain = True
        flagConseguirNombre = False
        return "Ok a partir de ahora te dire asi"
    if flagMain:
        if message in promptBasicoHola:
            return f"Hola, {nombreUsuario} ¿Cómo puedo ayudarte hoy?"
        elif message in promptBasicoComoEstas:
            return "¡Muy bien! ¿y vos?"
        elif message == "Cuál es la temperatura en Buenos Aires?":
            respuesta = (requests.get(urlCompleto)).json()
            if respuesta["cod"] != "404":
                temp = respuesta["main"]["temp"] - 273
                return f"la temperatura actual en la ciudad es de {temp:.2f} Celsius"
            else:
                return "Tuve un problema encontrando esa ciudad"
        elif message == "Decime un chiste de nerds":
            return chisteGenerar()
        elif message == "Adiós":
            flagMain = False
            return "Nos vemos!"
        else:
            return f"No entendi lo que quisiste decir: {message}"
    else:
        flagConseguirNombre = True
        return "Hola bienvenido ¿Cual es tu nombre?"

# Aca defino la interfaz usando la funcion mas basica de gradio, 
# doy un par de ejemplos de prompts y le pongo un nombre al bot
interfaz = gr.ChatInterface(
    fn=funcComportamiento, examples=["Decime un chiste de nerds", "Hola", "Cuál es la temperatura en Buenos Aires?"], title="Chatter Bot"
)
interfaz.launch()

interfaz.close()

