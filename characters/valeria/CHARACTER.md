# VALERIA — Canon v1 (personaje realista de prueba)

**Estado:** BORRADOR — pendiente de firma (Gate 0)
**Función de test:** hiperrealismo de piel (anti-porcelana) + consistencia de
identidad en el perfil más difícil (rostro femenino joven).
**Línea:** Fotorrealismo comercial-editorial.

---

## Atributos bloqueados (innegociables)

| Atributo | Valor canónico |
|---|---|
| Edad | 26 (fija) |
| Etnia / piel | Latina, piel media-cálida (Fitzpatrick III–IV), textura visible: poros, brillo natural en zona T, pecas sutiles en pómulos |
| Rostro | Ovalado, pómulos marcados |
| Ojos | Marrón oscuro, almendrados |
| Cejas | Oscuras, pobladas naturales, arco suave |
| Nariz | Recta con punta suave |
| Labios | Llenos, tono natural |
| Cabello (canónico) | Castaño oscuro, largo hasta media espalda, liso, raya al centro |
| Cuerpo | Esbelto tonificado, ~168 cm |
| Marcador 1 | Lunar pequeño bajo el ojo derecho |
| Marcador 2 | Cicatriz mínima en la cola de la ceja izquierda |

## Outfit canónico (solo para el laboratorio)

Camiseta blanca de cuello redondo + jeans azul medio. Cero moda en v1:
el laboratorio valida identidad y piel, no styling. Wardrobe editorial
entra en fase de producción, después de Gate 2.

## Canon negativo (nunca tiene)

Maquillaje pesado / piel aerografiada, uñas largas decoradas, tatuajes,
piercings visibles, extensiones de pestañas dramáticas, cabello teñido.

---

## Master prompt (base, inglés)

```
photograph, 26 year old latina woman, oval face, defined cheekbones,
dark brown almond eyes, natural full eyebrows, straight nose, full lips,
warm medium skin with visible pores and subtle freckles on cheekbones,
natural skin sheen, small mole under right eye, tiny scar at tail of left
eyebrow, dark brown long straight hair center part, slim toned build,
white crew-neck t-shirt, medium blue jeans, neutral grey studio background,
soft diffused lighting, 85mm lens, shallow depth of field
```

## Negative prompt (base)

```
airbrushed skin, porcelain skin, plastic skin, wax figure, heavy makeup,
oversmoothed, doll-like, cgi render, deformed hands, extra fingers,
tattoos, piercings, text, watermark
```

---

## Protocolo de anchors (8 tomas, fondo neutro, luz difusa)

1. `a1_frontal` — retrato frontal, expresión neutra
2. `a2_3q_izq` — tres cuartos izquierda
3. `a3_3q_der` — tres cuartos derecha
4. `a4_perfil` — perfil izquierdo
5. `a5_closeup` — primer plano extremo (EL test de piel: poros o fracaso)
6. `a6_sonrisa` — frontal, sonrisa natural con dientes
7. `a7_medio` — plano medio (valida proporciones)
8. `a8_luz_dura` — frontal con luz lateral dura (la piel plástica se delata aquí)

**Validación (gate duro):** `identity_check.py --mode real` — similitud de
coseno entre pares de anchors ≥ 0.60 **y** revisión visual de textura de piel
en `a5` y `a8`. Si la piel sale porcelana, se corrige el prompt/checkpoint,
no se juega lotería de seeds.

---

## Registro

| Fecha | Evento | Resultado |
|---|---|---|
| — | Canon v1 redactado | Pendiente de firma |
