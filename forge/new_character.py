#!/usr/bin/env python3
"""CLI interactiva para crear un personaje nuevo en character-lab.

Solo stdlib. 100% determinista y offline: no llama a ningún modelo de
IA, solo ensambla texto a partir de las respuestas del cuestionario.

Uso:
    python forge/new_character.py

Ver forge/GUIA_CREACION.md para el ritual completo y
forge/cuestionario.md para la versión en papel del cuestionario.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

FORGE_DIR = Path(__file__).resolve().parent
ROOT_DIR = FORGE_DIR.parent
CHARACTERS_DIR = ROOT_DIR / "characters"
TEMPLATES_DIR = FORGE_DIR / "templates"
TEMPLATE_PATH = TEMPLATES_DIR / "CHARACTER_TEMPLATE.md"
REGISTRY_PATH = FORGE_DIR / "registry.json"

PROMPTS_FILES = {
    "realista": TEMPLATES_DIR / "prompts_realista.md",
    "anime": TEMPLATES_DIR / "prompts_anime.md",
    "otro": TEMPLATES_DIR / "prompts_otros.md",
}

LINEA_ETIQUETA = {"realista": "Realista", "anime": "Anime", "otro": "Otro"}

BANNED_GENERIC = {
    "normal", "normal.", "comun", "común", "estandar", "estándar",
    "standard", "no se", "no sé", "nose", "cualquiera", "cualquier",
    "tipico", "típico", "nada", "ninguno", "ninguna", "default",
    "generico", "genérico", "x", "xd", "na", "n/a", "-", "cualquier cosa",
}

# Diccionario de traducción simple y literal palabra/frase por palabra.
# No es un traductor real: es un mapeo de términos frecuentes en este
# cuestionario. Lo que no está acá queda en español a propósito — Gate 0
# es el lugar para pulir el master prompt a mano.
TRADUCCION = {
    "rubio platino": "platinum blonde", "castaño oscuro": "dark brown",
    "castano oscuro": "dark brown", "raya al centro": "center part",
    "raya al lado": "side part", "raya lateral": "side part",
    "sin raya": "no part", "hasta media espalda": "down to mid-back",
    "hasta los hombros": "shoulder-length", "media melena": "medium-length",
    "postura erguida": "upright posture",
    "postura relajada": "relaxed posture",
    "hombros caidos": "slouched shoulders",
    "hombros caídos": "slouched shoulders",
    "rubio": "blonde", "rubia": "blonde", "castaño": "brown",
    "castana": "brown", "castaña": "brown", "negro": "black",
    "negra": "black", "pelirrojo": "red-haired", "pelirroja": "red-haired",
    "canoso": "grey", "cano": "grey", "largo": "long", "larga": "long",
    "corto": "short", "corta": "short", "liso": "straight",
    "lisa": "straight", "ondulado": "wavy", "ondulada": "wavy",
    "rizado": "curly", "rizada": "curly", "crespo": "coily",
    "crespa": "coily", "ovalado": "oval", "ovalada": "oval",
    "redondo": "round", "redonda": "round", "cuadrado": "square",
    "cuadrada": "square", "alargado": "elongated", "alargada": "elongated",
    "corazon": "heart-shaped", "corazón": "heart-shaped",
    "marron": "brown", "marrón": "brown", "marrones": "brown",
    "azul": "blue", "azules": "blue", "verde": "green", "verdes": "green",
    "gris": "grey", "grises": "grey", "ambar": "amber", "ámbar": "amber",
    "avellana": "hazel", "almendrados": "almond-shaped",
    "almendrado": "almond-shaped", "rasgados": "upturned",
    "rasgado": "upturned", "grandes": "large", "pequeños": "small",
    "pequenos": "small", "caidos": "downturned", "caídos": "downturned",
    "pobladas": "full", "poblado": "full", "finas": "thin",
    "fino": "thin", "arqueadas": "arched", "rectas": "straight",
    "recta": "straight", "respingada": "upturned", "aguileña": "aquiline",
    "aguilena": "aquiline", "ancha": "wide", "fina": "thin",
    "llenos": "full", "finos": "thin", "delgados": "thin",
    "carnosos": "full", "clara": "fair", "oscura": "dark",
    "morena": "tan", "media": "medium", "calida": "warm", "cálida": "warm",
    "fria": "cool", "fría": "cool", "pecas": "freckles", "poros": "pores",
    "cicatriz": "scar", "lunar": "mole", "tatuaje": "tattoo",
    "esbelto": "slim", "esbelta": "slim", "atletico": "athletic",
    "atlético": "athletic", "curvilineo": "curvy", "curvilíneo": "curvy",
    "curvilinea": "curvy", "robusto": "heavyset", "robusta": "heavyset",
    "delgado": "thin", "delgada": "thin", "musculoso": "muscular",
    "musculosa": "muscular", "izquierda": "left", "izquierdo": "left",
    "derecha": "right", "derecho": "right", "ceja": "eyebrow",
    "cejas": "eyebrows", "ojo": "eye", "ojos": "eyes", "mejilla": "cheek",
    "nariz": "nose", "boca": "mouth", "mandibula": "jaw",
    "mandíbula": "jaw", "frente": "forehead", "oreja": "ear",
    "bajo": "under", "sobre": "above", "cerca de": "near",
    "junto a": "next to", "años": "years old", "año": "year old",
    "piel": "skin", "tono": "tone", "textura": "texture",
    "camiseta": "t-shirt", "blanca": "white", "blanco": "white",
    "jean": "jeans", "jeans": "jeans", "vestido": "dress",
}

CATEGORIAS_MICRO = [
    ("asimetria_facial", "Asimetría facial",
     "el ojo izquierdo un poco más bajo que el derecho"),
    ("textura_particular",
     "Textura particular (pecas, poros marcados, cicatriz de acné...)",
     "pecas dispersas en el puente de la nariz y mejillas"),
    ("rasgo_oseo", "Rasgo óseo distintivo",
     "mandíbula ligeramente asimétrica hacia el lado derecho"),
    ("detalle_dental", "Detalle dental o de sonrisa",
     "diente incisivo superior izquierdo levemente rotado"),
    ("particularidad_mirada", "Particularidad de mirada",
     "párpado izquierdo levemente más caído (ptosis leve)"),
]

ANCHORS = {
    "realista": {
        "protocolo": (
            "1. `a1_frontal` — retrato frontal, expresión neutra\n"
            "2. `a2_3q_izq` — tres cuartos izquierda\n"
            "3. `a3_3q_der` — tres cuartos derecha\n"
            "4. `a4_perfil` — perfil izquierdo\n"
            "5. `a5_closeup` — primer plano extremo (EL test de piel: poros o fracaso)\n"
            "6. `a6_sonrisa` — frontal, sonrisa natural con dientes\n"
            "7. `a7_medio` — plano medio (valida proporciones)\n"
            "8. `a8_luz_dura` — frontal con luz lateral dura (la piel plástica se delata aquí)"
        ),
        "validacion": (
            "`identity_check.py --mode real` — similitud de coseno entre pares "
            "de anchors ≥ 0.60 **y** revisión visual de textura de piel en `a5` "
            "y `a8`. Si la piel sale porcelana, se corrige el prompt/checkpoint, "
            "no se juega lotería de seeds."
        ),
    },
    "anime": {
        "protocolo": (
            "1. `a1_frontal` — rostro frontal, expresión neutra\n"
            "2. `a2_3q_izq` — tres cuartos izquierda\n"
            "3. `a3_3q_der` — tres cuartos derecha\n"
            "4. `a4_perfil` — perfil izquierdo\n"
            "5. `a5_fullbody` — cuerpo completo frontal (valida proporciones + outfit)\n"
            "6. `a6_sonrisa` — frontal, sonrisa abierta\n"
            "7. `a7_enojo` — frontal, expresión de combate/enojo\n"
            "8. `a8_accion` — pose dinámica media (valida cabello en movimiento)"
        ),
        "validacion": (
            "Grid visual + checklist de atributos bloqueados por anchor. Los "
            "embeddings faciales NO son confiables en anime — no usar "
            "`identity_check.py` como gate duro, solo como señal orientativa "
            "(`--mode anime`)."
        ),
    },
    "otro": {
        "protocolo": (
            "1. `a1_frontal` — retrato/plano frontal, expresión neutra\n"
            "2. `a2_3q_izq` — tres cuartos izquierda\n"
            "3. `a3_3q_der` — tres cuartos derecha\n"
            "4. `a4_perfil` — perfil izquierdo\n"
            "5. `a5_closeup` — primer plano (detalle de textura/estilo)\n"
            "6. `a6_expresion` — frontal, expresión secundaria (sonrisa u otra)\n"
            "7. `a7_medio` — plano medio (valida proporciones + outfit)\n"
            "8. `a8_variacion` — pose o luz alternativa (valida estabilidad del estilo)"
        ),
        "validacion": (
            "Checklist visual de atributos bloqueados anchor por anchor. "
            "Definir si aplica `identity_check.py` (y en qué modo) recién "
            "cuando el estilo esté fijado — ver `templates/prompts_otros.md`."
        ),
    },
}


# --------------------------------------------------------------------------
# Utilidades
# --------------------------------------------------------------------------

def forzar_utf8_stdout() -> None:
    """En consolas Windows con codepage cp1252, acentos/guiones salen mal
    (y la entrada tipeada por el usuario se decodifica mal). Reconfigura
    stdin/stdout/stderr a UTF-8; si el runtime no lo soporta (Python
    viejo, stream no interactivo raro), se ignora en silencio.
    """
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def slugify(texto: str) -> str:
    texto = texto.strip().lower()
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^a-z0-9]+", "-", texto).strip("-")
    return texto or "personaje"


def traducir(texto: str) -> str:
    resultado = texto
    for es, en in sorted(TRADUCCION.items(), key=lambda kv: -len(kv[0])):
        patron = re.compile(r"(?<!\w)" + re.escape(es) + r"(?!\w)", re.IGNORECASE)
        resultado = patron.sub(en, resultado)
    return resultado


def preguntar(etiqueta: str, ejemplo: str, min_len: int = 3) -> str:
    while True:
        resp = input(f"{etiqueta}: ").strip()
        if not resp:
            print(f"  ✗ No puede quedar vacío. Nivel de detalle esperado, ej.: «{ejemplo}»")
            continue
        if resp.lower() in BANNED_GENERIC:
            print(f"  ✗ «{resp}» es demasiado genérico — el objetivo es que el "
                  f"personaje sea irrepetible. Ejemplo: «{ejemplo}»")
            continue
        if len(resp) < min_len:
            print(f"  ✗ Necesito más detalle (mínimo {min_len} caracteres). Ejemplo: «{ejemplo}»")
            continue
        return resp


def preguntar_si_no(etiqueta: str) -> bool:
    while True:
        resp = input(f"{etiqueta} (s/n): ").strip().lower()
        if resp.startswith("s"):
            return True
        if resp.startswith("n"):
            return False
        print("  ✗ Respondé s o n.")


def preguntar_edad() -> int:
    while True:
        resp = input("Edad (entero único, ej. 24 — nada de rangos como 20-25): ").strip()
        if re.fullmatch(r"\d{1,3}", resp):
            edad = int(resp)
            if 1 <= edad <= 120:
                return edad
        print("  ✗ Edad inválida. Tiene que ser un único número entero (ej. 24), sin rangos ni texto.")


def preguntar_linea() -> str:
    print("Línea estética:\n  1) Realista\n  2) Anime\n  3) Otro")
    opciones = {"1": "realista", "2": "anime", "3": "otro"}
    while True:
        resp = input("Elegí 1/2/3: ").strip().lower()
        if resp in opciones:
            return opciones[resp]
        if resp in opciones.values():
            return resp
        print("  ✗ Elegí una opción válida: 1 (realista), 2 (anime) o 3 (otro).")


# --------------------------------------------------------------------------
# Bloques del cuestionario
# --------------------------------------------------------------------------

def bloque1_identidad(slugs_existentes: set[str]):
    print("\n== Bloque 1 — Identidad ==")
    while True:
        nombre = preguntar("Nombre de laboratorio", "Nova", min_len=2)
        slug = slugify(nombre)
        if slug in slugs_existentes:
            print(f"  ✗ Ya existe un personaje con el slug «{slug}». Elegí otro nombre.")
            continue
        break
    linea = preguntar_linea()
    edad = preguntar_edad()
    funcion_test = preguntar(
        "Rol / uso previsto de este personaje en el laboratorio",
        "test de expresividad facial en primeros planos", min_len=8,
    )
    return {"nombre": nombre, "slug": slug, "linea": linea, "edad": edad, "funcion_test": funcion_test}


def bloque2_rostro():
    print("\n== Bloque 2 — Rostro ==")
    rostro = preguntar("Forma de cara", "ovalada, pómulos marcados", min_len=5)
    ojos_color = preguntar("Ojos — color", "marrón oscuro", min_len=3)
    ojos_forma = preguntar("Ojos — forma", "almendrados", min_len=3)
    cejas = preguntar("Cejas", "oscuras, pobladas naturales, arco suave", min_len=5)
    nariz = preguntar("Nariz", "recta con punta suave", min_len=4)
    labios = preguntar("Labios", "llenos, tono natural", min_len=4)
    piel_tono = preguntar("Piel — tono", "media-cálida", min_len=3)
    piel_textura = preguntar("Piel — textura", "poros visibles, pecas sutiles en pómulos", min_len=5)
    return {
        "rostro": rostro,
        "ojos": f"{ojos_color}, {ojos_forma}",
        "cejas": cejas,
        "nariz": nariz,
        "labios": labios,
        "piel": f"{piel_tono}, {piel_textura}",
    }


def bloque3_microdetalles():
    print("\n== Bloque 3 — Micro-detalles (el corazón de la unicidad) ==")
    print("Mínimo 3 de las 5 categorías. Cada respuesta necesita al menos 10 caracteres de detalle real.")
    resultados: dict[str, tuple[str, str]] = {}
    pendientes = list(CATEGORIAS_MICRO)
    for clave, nombre, ejemplo in list(pendientes):
        if preguntar_si_no(f"¿Definir micro-detalle «{nombre}»?"):
            valor = preguntar(f"  Descripción de «{nombre}»", ejemplo, min_len=10)
            resultados[clave] = (nombre, valor)
            pendientes.remove((clave, nombre, ejemplo))
    while len(resultados) < 3 and pendientes:
        clave, nombre, ejemplo = pendientes.pop(0)
        print(f"Necesitás al menos 3 micro-detalles (tenés {len(resultados)}). Vamos con «{nombre}».")
        valor = preguntar(f"  Descripción de «{nombre}»", ejemplo, min_len=10)
        resultados[clave] = (nombre, valor)
    return resultados


def bloque4_marcadores():
    print("\n== Bloque 4 — Marcadores de identidad ==")
    print("Mínimo 2, cada uno con ubicación exacta (lunar, cicatriz, tatuaje pequeño, joyería fija...).")
    marcadores = []
    i = 1
    while True:
        tipo = preguntar(f"Marcador {i} — tipo", "cicatriz fina", min_len=3)
        ubicacion = preguntar(f"Marcador {i} — ubicación exacta", "bajo el ojo derecho, a 1cm del lagrimal", min_len=5)
        marcadores.append({"tipo": tipo, "ubicacion": ubicacion})
        i += 1
        if len(marcadores) >= 2 and not preguntar_si_no("¿Agregar otro marcador?"):
            break
    return marcadores


def bloque5_cabello():
    print("\n== Bloque 5 — Cabello canónico (todos obligatorios) ==")
    color = preguntar("Color", "castaño oscuro", min_len=3)
    largo = preguntar("Largo", "hasta media espalda", min_len=3)
    textura = preguntar("Textura", "liso", min_len=3)
    peinado = preguntar("Peinado", "suelto", min_len=3)
    raya = preguntar("Raya", "al centro", min_len=3)
    return {"color": color, "largo": largo, "textura": textura, "peinado": peinado, "raya": raya}


def bloque6_cuerpo():
    print("\n== Bloque 6 — Cuerpo ==")
    complexion = preguntar("Complexión", "esbelta tonificada", min_len=4)
    estatura = preguntar("Estatura aproximada", "168 cm", min_len=3)
    postura = preguntar("Postura característica", "hombros relajados, mentón ligeramente elevado", min_len=6)
    return {"complexion": complexion, "estatura": estatura, "postura": postura}


def bloque7_canon_negativo():
    print("\n== Bloque 7 — Canon negativo ==")
    print("Mínimo 3 cosas que el personaje NUNCA tiene.")
    negativos = []
    i = 1
    while True:
        val = preguntar(f"Cosa #{i} que el personaje NUNCA tiene", "tatuajes visibles", min_len=4)
        negativos.append(val)
        i += 1
        if len(negativos) >= 3 and not preguntar_si_no("¿Agregar otra cosa al canon negativo?"):
            break
    outfit = preguntar(
        "Outfit de laboratorio (una línea, simple — sin styling, eso llega después de Gate 2)",
        "camiseta blanca de cuello redondo + jeans azul medio", min_len=8,
    )
    return negativos, outfit


# --------------------------------------------------------------------------
# Registry / unicidad
# --------------------------------------------------------------------------

def cargar_registry() -> list[dict]:
    if REGISTRY_PATH.exists():
        contenido = REGISTRY_PATH.read_text(encoding="utf-8").strip()
        if contenido:
            return json.loads(contenido)
    return []


def elementos_comparables(linea: str, edad: int, cabello: dict, marcadores: list[dict]) -> set[tuple]:
    elems = {("linea", linea), ("edad", edad)}
    for campo, valor in cabello.items():
        elems.add((f"cabello_{campo}", valor.strip().lower()))
    for m in marcadores:
        elems.add(("marcador", m["tipo"].strip().lower(), m["ubicacion"].strip().lower()))
    return elems


def verificar_unicidad(linea: str, edad: int, cabello: dict, marcadores: list[dict], registry: list[dict]):
    while True:
        nuevos = elementos_comparables(linea, edad, cabello, marcadores)
        colision = None
        for personaje in registry:
            existentes = {tuple(e) for e in personaje.get("elementos_comparables", [])}
            interseccion = nuevos & existentes
            if len(interseccion) >= 2:
                colision = (personaje, interseccion)
                break
        if not colision:
            return linea, edad, cabello, marcadores
        personaje, interseccion = colision
        print(f"\n⚠ Este personaje se parece demasiado a «{personaje['slug']}» "
              f"— comparten {len(interseccion)} elementos:")
        for e in interseccion:
            print(f"   - {e}")
        print("Necesitás diferenciar antes de continuar.\n")
        print("¿Qué querés cambiar? 1) Edad  2) Cabello  3) Marcadores  4) Línea")
        opcion = input("Elegí 1/2/3/4: ").strip()
        if opcion == "1":
            edad = preguntar_edad()
        elif opcion == "2":
            cabello = bloque5_cabello()
        elif opcion == "3":
            marcadores = bloque4_marcadores()
        elif opcion == "4":
            linea = preguntar_linea()
        else:
            print("Opción inválida, probemos de nuevo.")


# --------------------------------------------------------------------------
# Parsing de templates/prompts_{linea}.md
# --------------------------------------------------------------------------

def parsear_prompts(linea: str) -> dict:
    path = PROMPTS_FILES[linea]
    texto = path.read_text(encoding="utf-8")

    def extraer(heading: str) -> str:
        patron = re.compile(re.escape(heading) + r"\s*\n\n```\n(.*?)\n```", re.S)
        match = patron.search(texto)
        return match.group(1).strip() if match else ""

    return {
        "prefijo": extraer("## Bloque de calidad (prefijo)"),
        "sufijo": extraer("## Bloque de calidad (sufijo — fondo y luz)"),
        "negative": extraer("## Negative prompt (base)"),
    }


# --------------------------------------------------------------------------
# Ensamblado de master prompt
# --------------------------------------------------------------------------

def construir_master_prompt(datos: dict, prompts_data: dict) -> str:
    partes = []
    if prompts_data["prefijo"]:
        partes.append(prompts_data["prefijo"])
    partes.append(f"{datos['edad']} years old")
    partes.append(traducir(datos["rostro"]))
    partes.append(traducir(datos["ojos"]))
    partes.append(traducir(datos["cejas"]))
    partes.append(traducir(datos["nariz"]))
    partes.append(traducir(datos["labios"]))
    partes.append(traducir(datos["piel"]))
    for _, valor in datos["microdetalles"].values():
        partes.append(traducir(valor))
    cabello = datos["cabello"]
    partes.append(traducir(
        f"{cabello['color']} {cabello['largo']} {cabello['textura']} hair, "
        f"{cabello['peinado']}, {cabello['raya']}"
    ))
    for m in datos["marcadores"]:
        partes.append(traducir(f"{m['tipo']} {m['ubicacion']}"))
    cuerpo = datos["cuerpo"]
    partes.append(traducir(f"{cuerpo['complexion']}, {cuerpo['estatura']}, {cuerpo['postura']}"))
    partes.append(traducir(datos["outfit"]))
    if prompts_data["sufijo"]:
        partes.append(prompts_data["sufijo"])
    return ", ".join(p.strip() for p in partes if p.strip())


# --------------------------------------------------------------------------
# Generación de CHARACTER.md
# --------------------------------------------------------------------------

def construir_character_md(datos: dict, master_prompt: str, negative_prompt: str) -> str:
    plantilla = TEMPLATE_PATH.read_text(encoding="utf-8")

    marcadores_filas = "\n".join(
        f"| Marcador {i} | {m['tipo']} — {m['ubicacion']} |"
        for i, m in enumerate(datos["marcadores"], start=1)
    )
    microdetalles_linea = "<br>".join(
        f"{nombre}: {valor}" for nombre, valor in datos["microdetalles"].values()
    )
    cabello = datos["cabello"]
    cabello_txt = f"{cabello['color']}, largo {cabello['largo']}, textura {cabello['textura']}, {cabello['peinado']}, raya {cabello['raya']}"
    cuerpo = datos["cuerpo"]
    cuerpo_txt = f"{cuerpo['complexion']}, ~{cuerpo['estatura']}, postura: {cuerpo['postura']}"
    canon_negativo_txt = ", ".join(datos["canon_negativo"]) + "."
    anchors = ANCHORS[datos["linea"]]
    linea_descripcion = (
        f"{LINEA_ETIQUETA[datos['linea']]}. Ver forge/templates/{PROMPTS_FILES[datos['linea']].name} "
        f"para bloques base de calidad y negative prompt."
    )

    reemplazos = {
        "{{nombre_upper}}": datos["nombre"].upper(),
        "{{linea_etiqueta}}": LINEA_ETIQUETA[datos["linea"]],
        "{{funcion_test}}": datos["funcion_test"],
        "{{linea_descripcion}}": linea_descripcion,
        "{{edad}}": str(datos["edad"]),
        "{{rostro}}": datos["rostro"],
        "{{ojos}}": datos["ojos"],
        "{{cejas}}": datos["cejas"],
        "{{nariz}}": datos["nariz"],
        "{{labios}}": datos["labios"],
        "{{piel}}": datos["piel"],
        "{{microdetalles_linea}}": microdetalles_linea,
        "{{cabello}}": cabello_txt,
        "{{cuerpo}}": cuerpo_txt,
        "{{marcadores_filas}}": marcadores_filas,
        "{{outfit}}": datos["outfit"],
        "{{canon_negativo}}": canon_negativo_txt,
        "{{master_prompt}}": master_prompt,
        "{{negative_prompt}}": negative_prompt,
        "{{protocolo_anchors}}": anchors["protocolo"],
        "{{validacion_anchors}}": anchors["validacion"],
        "{{fecha_creacion}}": date.today().isoformat(),
    }
    for placeholder, valor in reemplazos.items():
        plantilla = plantilla.replace(placeholder, valor)
    return plantilla


def crear_estructura_personaje(slug: str) -> Path:
    carpeta = CHARACTERS_DIR / slug
    for sub in ("anchors", "datasets", "outputs"):
        (carpeta / sub).mkdir(parents=True, exist_ok=True)
        (carpeta / sub / ".gitkeep").touch()
    return carpeta


def registrar_personaje(datos: dict, hash_combinacion: str, registry: list[dict]) -> None:
    entrada = {
        "slug": datos["slug"],
        "nombre": datos["nombre"],
        "fecha": date.today().isoformat(),
        "linea": datos["linea"],
        "edad": datos["edad"],
        "funcion_test": datos["funcion_test"],
        "marcadores": [f"{m['tipo']} — {m['ubicacion']}" for m in datos["marcadores"]],
        "cabello": datos["cabello"],
        "hash_combinacion": hash_combinacion,
        "elementos_comparables": [
            list(e) for e in elementos_comparables(datos["linea"], datos["edad"], datos["cabello"], datos["marcadores"])
        ],
        "creado_por": "forge/new_character.py",
    }
    registry.append(entrada)
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def calcular_hash(datos: dict) -> str:
    combinacion = {
        "linea": datos["linea"],
        "edad": datos["edad"],
        "cabello": datos["cabello"],
        "marcadores": datos["marcadores"],
    }
    combinacion_str = json.dumps(combinacion, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(combinacion_str.encode("utf-8")).hexdigest()[:16]


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------

def main() -> None:
    print("=== forge — creación de personaje ===")
    print("7 bloques. Ctrl+C para abortar en cualquier momento.\n")

    registry = cargar_registry()
    slugs_existentes = {p["slug"] for p in registry}
    if CHARACTERS_DIR.exists():
        slugs_existentes |= {d.name for d in CHARACTERS_DIR.iterdir() if d.is_dir()}

    identidad = bloque1_identidad(slugs_existentes)
    rostro = bloque2_rostro()
    microdetalles = bloque3_microdetalles()
    marcadores = bloque4_marcadores()
    cabello = bloque5_cabello()
    cuerpo = bloque6_cuerpo()
    canon_negativo, outfit = bloque7_canon_negativo()

    linea, edad, cabello, marcadores = verificar_unicidad(
        identidad["linea"], identidad["edad"], cabello, marcadores, registry
    )
    identidad["linea"] = linea
    identidad["edad"] = edad

    datos = {
        **identidad,
        **rostro,
        "microdetalles": microdetalles,
        "marcadores": marcadores,
        "cabello": cabello,
        "cuerpo": cuerpo,
        "canon_negativo": canon_negativo,
        "outfit": outfit,
    }

    prompts_data = parsear_prompts(datos["linea"])
    master_prompt = construir_master_prompt(datos, prompts_data)
    negative_prompt = prompts_data["negative"]

    contenido_md = construir_character_md(datos, master_prompt, negative_prompt)
    carpeta = crear_estructura_personaje(datos["slug"])
    (carpeta / "CHARACTER.md").write_text(contenido_md, encoding="utf-8")

    hash_combinacion = calcular_hash(datos)
    registrar_personaje(datos, hash_combinacion, registry)

    print(f"\n✔ Personaje «{datos['nombre']}» creado en characters/{datos['slug']}/")
    print("  CHARACTER.md generado (estado BORRADOR).")
    print(f"  Registrado en forge/registry.json (hash {hash_combinacion}).")
    print("\nGate 0: revisar y firmar CHARACTER.md antes de generar anchors")


if __name__ == "__main__":
    forzar_utf8_stdout()
    try:
        main()
    except KeyboardInterrupt:
        print("\nAbortado.")
        sys.exit(1)
