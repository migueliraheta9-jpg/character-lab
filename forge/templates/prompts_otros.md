# Prompts base — Línea Otros (estilo por definir)

Comodín para estilos que no son ni fotorrealismo ni anime (pintura
digital, 3D render, cómic, pixel art...). No hay un bloque de calidad
fijo porque el estilo se define personaje a personaje, antes de Gate 0.

## Cómo definir el estilo antes de generar anchors

1. Elegí una referencia visual clara (2–3 imágenes o un checkpoint/LoRA
   concreto) antes de tocar el prompt.
2. Escribí el bloque de calidad (prefijo) igual que en
   `prompts_realista.md` o `prompts_anime.md`: 1–3 tags que fijen el
   motor/estilo (ej. `3d render, pixar style` o `digital painting,
   concept art`).
3. Actualizá el bloque de calidad (sufijo) con fondo y luz coherentes
   con ese estilo.
4. Solo entonces corré `forge/new_character.py` para un personaje de
   esta línea — el master prompt que genera va a arrastrar el
   placeholder de abajo hasta que se reemplace acá.

## Bloque de calidad (prefijo)

```
[[definir estilo antes de Gate 0 — ver instrucciones arriba]]
```

## Bloque de calidad (sufijo — fondo y luz)

```
neutral grey background
```

## Negative prompt (base)

```
deformed hands, extra fingers, bad anatomy, extra limbs, text, watermark
```

## Qué suele romper la consistencia (línea otros)

1. **Estilo no fijado antes de generar** — si el prefijo de calidad
   queda como placeholder, cada anchor puede salir en un estilo
   distinto. Gate 0 debe bloquear esto explícitamente.
2. **Mezcla de motores/checkpoints entre anchors** — el set de 8 debe
   generarse con el mismo motor y la misma versión de checkpoint.
3. **Ausencia de referencia visual** — sin 2–3 imágenes de referencia
   claras, el "canon" queda subjetivo y difícil de validar en Gate 1.
