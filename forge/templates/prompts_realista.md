# Prompts base — Línea Realista

Bloque de referencia que `forge/new_character.py` lee para ensamblar el
`master prompt` y el `negative prompt` de cada personaje realista nuevo.
Si cambian los tags base acá, todo personaje que se cree después los
hereda automáticamente (los ya existentes no se tocan).

## Bloque de calidad (prefijo)

```
photograph
```

## Bloque de calidad (sufijo — fondo y luz)

```
neutral grey studio background, soft diffused lighting, 85mm lens, shallow depth of field
```

## Negative prompt (base)

```
airbrushed skin, porcelain skin, plastic skin, wax figure, heavy makeup, oversmoothed, doll-like, cgi render, deformed hands, extra fingers, text, watermark
```

## Qué suele romper la consistencia (línea realista)

1. **Piel porcelana / aerografiada** — el modelo "limpia" la piel y pierde
   poros, pecas y textura real. Si aparece, se corrige el prompt o el
   checkpoint; no se juega lotería de seeds.
2. **Iluminación plana** — la luz frontal difusa esconde la geometría real
   de la cara. Por eso el protocolo de anchors siempre incluye una toma
   con luz lateral dura: ahí se delata la piel plástica.
3. **Deriva de identidad en primer plano extremo** — cuanto más cerca la
   cámara, más fácil que el modelo "invente" rasgos. El anchor de
   closeup es el más exigente y el primero en fallar.
