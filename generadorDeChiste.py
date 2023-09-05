# Parte 2 del código escrito por Felipe Cravero para la prueba tecnica de la ETRR
# por parte de la Escuela de datos vivos

# utilizo el modulo langchain para poder hacer las request a Hugging face 
# con una plantilla y de forma mas cómoda
from langchain import HuggingFaceHub, LLMChain
from langchain.prompts import PromptTemplate
# Utilizo los mismos modulo que en anterior exepto por random que 
# me sirve   variar levemente el prompt y diversificar los textos de gpt-2
import random, requests

# Defino una lista con sinonimos en inglses para variar el prompt que recibe gpt-2
sinonimosMust = ["should", "must", "need to", "ought to", "requires to", "have to", "is destined to", "is driven to"]
# Acá defino la autorización y el url para usar "Opus"(creo que se llama así)
# para que me traduzca a español los textos de gpt-2
API_URL_TRADUC = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-es"
headers = {"Authorization": f"Bearer {'Poner key para la api de HuggingFace acá'}"}
# Defino una funcion para el query del traductor
def traductQuery(payload):
	response = requests.post(API_URL_TRADUC, headers=headers, json=payload)
	return response.json()
# Hago la plantilla para definir parametros y a que ia va a hacer el request 
hub_llm = HuggingFaceHub(
    repo_id = "gpt2",
    model_kwargs={"temperature": 15,
                   "max_length": 60,
                   "repetition_penalty": 50,
                   }
)
# Defino plantilla para el prompt
prompt = PromptTemplate(
    input_variables = ["sinonimos"],
    template = "A nerd joke {sinonimos} be:"
)
# Defino la funcion que voy a llamar en main.py para que me devuelva un string 
def chisteGenerar():
    hub_chain = LLMChain(prompt=prompt, llm=hub_llm)
    ding = random.choice(sinonimosMust)
    response = hub_chain.run(ding)
    
    output = traductQuery({
    	"inputs": response,
    })
    print(output)
    try:
        return output[0]["translation_text"]
    except Exception as ex:
        return "Traductor sigue cargando, pruebe en 20 segundos"
