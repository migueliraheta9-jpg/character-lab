# Prompts base — Línea Anime

Bloque de referencia que `forge/new_character.py` lee para ensamblar el
`master prompt` y el `negative prompt` de cada personaje anime nuevo.
Estilo visual NO definido a nivel de laboratorio: estos tags generan un
anime limpio y neutro; la capa de estilo (LoRA de estudio) se decide
después de Gate 2, personaje por personaje.

## Bloque de calidad (prefijo)

```
anime illustration, clean lineart
```

## Bloque de calidad (sufijo — fondo y luz)

```
neutral grey background, soft even lighting
```

## Negative prompt (base)

```
extra accessories, jewelry, necklace, fantasy hair colors, elf ears, heavy makeup, deformed hands, extra fingers, multiple views, text, watermark
```

## Qué suele romper la consistencia (línea anime)

1. **Deriva de estilo entre generaciones** — sin LoRA de estudio fijo,
   cada generación puede variar el grosor de línea o el nivel de
   sombreado. Fijar el checkpoint/LoRA antes de generar el set de
   anchors completo.
2. **Física del cabello inconsistente** — mechones sueltos y largo
   exacto se pierden en poses dinámicas. Revisar contra el canon en
   cada anchor, no solo en el frontal.
3. **Embeddings faciales no confiables** — a diferencia de la línea
   realista, acá NO sirve medir similitud de coseno; la validación es
   checklist visual de atributos bloqueados, anchor por anchor.
