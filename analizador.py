from flask import Flask, request, render_template
import ply.lex as lex

app = Flask(__name__)

sinonimos = {
    "rápido": "veloz",
    "lento": "pausado",
    "hermoso": "bello",
    "feo": "desagradable",
    "fuerte": "robusto",
    "débil": "frágil",
    "grande": "enorme",
    "pequeño": "diminuto",
    "inteligente": "listo",
    "tonto": "necio",
    "alegre": "feliz",
    "triste": "melancólico",
    "valiente": "audaz",
    "cobarde": "miedoso",
    "rico": "adinerado",
    "pobre": "indigente",
    "caliente": "ardiente",
    "frío": "helado",
    "amigo": "camarada",
    "enemigo": "adversario",
    "fácil": "sencillo",
    "difícil": "complicado",
    "oscuro": "tenebroso",
    "claro": "luminoso",
    "corto": "breve",
    "largo": "extenso",
    "nuevo": "reciente",
    "viejo": "antiguo",
    "carro": "coche",
    "casa": "hogar",
    "libro": "texto",
    "comida": "alimento",
    "trabajo": "empleo",
    "escuela": "colegio",
    "niño": "infante",
    "adulto": "mayor",
    "paz": "tranquilidad",
    "guerra": "conflicto",
    "amor": "afecto",
    "odio": "rencor",
    "peligro": "riesgo",
    "seguridad": "protección",
    "felicidad": "dicha",
    "sufrimiento": "dolor",
    "interesante": "fascinante",
    "aburrido": "tedioso",
    "bueno": "bondadoso",
    "malo": "malvado",
    "rápido": "veloz",  
    "lápiz": "pluma",   
    "soleado": "radiante",   
    "oscuro": "negro",  
    "azul": "celeste",  
    "rojo": "carmesí",  
    "naranja": "anaranjado", 
    "amarillo": "dorado", 
    "verde": "esmeralda",  
    "morado": "púrpura",  
    "blanco": "albo",  
    "negro": "ebúrneo",  
    "gris": "plateado",  
    "mariposa": "papillon",  
    "estrella": "lucero", 
    "agua": "líquido",  
    "cielo": "firmamento",  
    "pájaro": "ave",  
    "flor": "geranio",  
    "árbol": "arbusto",  
    "montaña": "colina",  
    "río": "torrente",  
    "mar": "océano",  
    "playa": "costa",  
    "arena": "polvo",  
    "viento": "brisa",  
    "fuego": "llama",  
    "hierro": "metal",  
    "oro": "metal precioso",  
    "plata": "metal noble",  
    "cobalto": "metal azul",  
    "cobre": "metal rojo",  
    "estrella": "luminaria",  
    "sol": "astro rey",  
    "luna": "astro satélite",  
    "planeta": "mundo",  
    "galaxia": "universo",  
    "cometa": "astro errante",  
    "asteroide": "astro menor",  
    "nebulosa": "nube cósmica",  
    "constelación": "grupo estelar",  
    "satélite": "astro secundario",  
    "telescopio": "lente astronómico",  
    "meteorito": "astro rocoso",  
    "oriente": "este",  
    "occidente": "oeste",  
    "norte": "nórdico",  
    "sur": "meridional",  
    "arriba": "encima",  
    "abajo": "debajo",  
    "adelante": "delante",  
    "atrás": "detrás",  
    "derecha": "diestra",  
    "izquierda": "siniestra",  
    "cerca": "próximo",  
    "lejos": "distante",  
}

tokens = (
    'PALABRA',
    'NUMERO',
    'SIMBOLO',
)

def t_NUMERO(t):
    r'\d+'
    t.original = t.value
    return t

def t_SIMBOLO(t):
    r'[^\w\s]'
    t.original = t.value
    return t

def t_PALABRA(t):
    r'\b\w+\b'
    t.original = t.value
    t.value = sinonimos.get(t.value.lower(), t.value)
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

def reemplazar_palabras(texto):
    lexer.input(texto)
    detalles = []
    line_num = 1
    for linea in texto.split('\n'):
        lexer.input(linea)
        for tok in lexer:
            entrada = tok.original
            if tok.type == 'PALABRA':
                resultante = sinonimos.get(entrada.lower(), entrada)
            else:
                resultante = ""
            palabra_cambiada = "X" if entrada.lower() in sinonimos else ""
            numero = "X" if tok.type == 'NUMERO' else ""
            simbolo = "X" if tok.type == 'SIMBOLO' else ""
            detalles.append((entrada, resultante, palabra_cambiada, numero, simbolo, line_num))
        line_num += 1
    return detalles



@app.route('/', methods=['GET', 'POST'])
def index():
    detalles = []
    texto = ""
    if request.method == 'POST':
        texto = request.form['texto']
        detalles = reemplazar_palabras(texto)
    return render_template('index.html', detalles=detalles, texto=texto)

if __name__ == '__main__':
    app.run(debug=True)
