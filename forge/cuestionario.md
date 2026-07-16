# Cuestionario de creación de personaje (versión papel)

Llená esto **antes** de correr `forge/new_character.py`. El CLI hace las
mismas preguntas e impone las mismas reglas de especificidad — pensarlo
offline primero ahorra vueltas.

> Regla general: no se aceptan respuestas vacías ni genéricas ("normal",
> "común", "estándar", "no sé"...). El objetivo de este laboratorio es
> que el personaje sea irrepetible, no un promedio.

---

## B1 — Identidad

- **Nombre de laboratorio:** _______________________
- **Línea estética:** ☐ Realista ☐ Anime ☐ Otro
- **Edad:** un único número entero (ej. `24`). Nada de rangos como
  `20-25`.
- **Rol / uso previsto:** para qué sirve este personaje en el
  laboratorio (texto libre, pero concreto).

## B2 — Rostro

- **Forma de cara:** (ovalada, cuadrada, redonda, corazón...)
- **Ojos:** color + forma (ej. "marrón oscuro, almendrados")
- **Cejas:** (grosor, forma, tono)
- **Nariz:** (forma, tamaño)
- **Labios:** (grosor, tono)
- **Piel:** tono + textura (ej. "media-cálida, poros visibles, pecas
  sutiles en pómulos")

## B3 — Micro-detalles (el corazón de la unicidad)

Definí **mínimo 3 de estas 5** categorías. Cada respuesta necesita al
menos 10 caracteres de detalle real — nada de "un poco distinto".

- ☐ **Asimetría facial** — ej. "el ojo izquierdo un poco más bajo que
  el derecho"
- ☐ **Textura particular** (pecas, poros marcados, cicatriz de acné...)
  — ej. "pecas dispersas en el puente de la nariz y mejillas"
- ☐ **Rasgo óseo distintivo** — ej. "mandíbula ligeramente asimétrica
  hacia el lado derecho"
- ☐ **Detalle dental o de sonrisa** — ej. "diente incisivo superior
  izquierdo levemente rotado"
- ☐ **Particularidad de mirada** — ej. "párpado izquierdo levemente
  más caído (ptosis leve)"

## B4 — Marcadores de identidad

Mínimo **2**, cada uno con ubicación exacta (lunar, cicatriz, tatuaje
pequeño, joyería fija...).

1. Tipo: _______________  Ubicación exacta: _______________
2. Tipo: _______________  Ubicación exacta: _______________
3. (opcional) Tipo: _______________  Ubicación exacta: _______________

## B5 — Cabello canónico (todos obligatorios)

- **Color:** _______________
- **Largo:** _______________
- **Textura:** (liso, ondulado, rizado, crespo...)
- **Peinado:** _______________
- **Raya:** (centro, lado, sin raya)

## B6 — Cuerpo

- **Complexión:** _______________
- **Estatura aproximada:** _______________
- **Postura característica:** _______________

## B7 — Canon negativo

Mínimo **3** cosas que el personaje NUNCA tiene:

1. _______________
2. _______________
3. _______________

**Outfit de laboratorio** (una línea, simple — sin styling; eso llega
después de Gate 2): _______________

---

## Verificación de unicidad

Antes de registrar, `new_character.py` compara línea + edad + cabello +
marcadores contra `forge/registry.json`. Si 2 o más elementos coinciden
con un personaje existente, el CLI va a pedirte diferenciar algo (edad,
cabello o marcadores) antes de continuar. Pensá esto de antemano si ya
tenés una idea de otro personaje parecido.

---

Siguiente paso: `python forge/new_character.py` — ver
`forge/GUIA_CREACION.md` para el ritual completo.
