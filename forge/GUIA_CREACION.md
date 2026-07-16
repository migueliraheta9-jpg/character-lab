# Guía de creación — ritual completo

`forge/` es el único camino para que nazca un personaje nuevo en este
laboratorio. Ver convención en el `README.md` raíz: *"Todo personaje
nuevo nace por `forge/new_character.py`, nunca a mano."*

---

## Paso 1 — Pensar el concepto

Antes de abrir nada: ¿qué está probando este personaje? Mirá la tabla
"Personajes de prueba" del `README.md` raíz — cada personaje existe
para estresar algo puntual del pipeline (piel realista, complejidad de
outfit, rango expresivo...). Definí esa función de test primero; todo
lo demás sale de ahí.

## Paso 2 — Llenar el cuestionario

Completá `forge/cuestionario.md` en papel (o en un editor, offline).
Prestá especial atención al **Bloque 3 (micro-detalles)** — es lo que
hace que el personaje no se confunda con ningún otro del laboratorio ni
con un rostro genérico del modelo.

## Paso 3 — Correr `new_character.py`

```
python forge/new_character.py
```

Es 100% interactivo, en español, sin dependencias externas. Vas a
pasar por los mismos 7 bloques del cuestionario. El CLI:

- rechaza respuestas vacías o genéricas ("normal", "no sé"...) con un
  ejemplo del nivel de detalle esperado,
- exige los mínimos de cada bloque (3 micro-detalles, 2 marcadores, 3
  ítems de canon negativo),
- compara el personaje nuevo contra `forge/registry.json` y frena si
  hay demasiado parecido con uno existente,
- genera `characters/{slug}/` (con `anchors/`, `datasets/`, `outputs/`)
  y `characters/{slug}/CHARACTER.md` ya completo, con master prompt y
  negative prompt ensamblados,
- registra el personaje en `forge/registry.json`.

## Paso 4 — Firmar Gate 0

El `CHARACTER.md` generado nace en **estado BORRADOR**. Revisalo a
mano: el master prompt viene de una traducción simple/literal de tus
respuestas (sin dependencias de traducción real) — es el momento de
corregir cualquier frase que haya quedado en español o mal fraseada en
inglés. Cuando estés conforme, cambiá el estado a **FIRMADO** y anotá
la fecha en la tabla de Registro del propio `CHARACTER.md`.

Ver protocolo de gates completo en el `README.md` raíz — nada se
genera antes de que Gate 0 esté firmado.

## Paso 5 — Generar anchors

Seguí el "Protocolo de anchors" de la sección correspondiente en el
`CHARACTER.md` del personaje (8 tomas). Los tags base de calidad y el
negative prompt salen de `forge/templates/prompts_{linea}.md` — si el
personaje es de línea "otro", primero hay que fijar el estilo ahí (ver
ese archivo) antes de generar nada.

## Paso 6 — Validar

Gate 1 según la línea del personaje (ver `README.md` raíz y
`validation/identity_check.py`):

- **Realista:** `identity_check.py --mode real` + revisión visual de
  textura de piel en los anchors de closeup y luz dura.
- **Anime:** grid visual + checklist de atributos bloqueados anchor
  por anchor (los embeddings no son confiables acá).
- **Otro:** checklist visual; el modo de `identity_check.py` a usar (si
  aplica alguno) se decide junto con el estilo, en
  `templates/prompts_otros.md`.

Si pasa Gate 1 → Gate 2 (fuera de distribución), tal como está descrito
en el `README.md` raíz.
