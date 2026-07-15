# ASTRID — Canon v1 (personaje anime de prueba)

**Estado:** BORRADOR — pendiente de firma (Gate 0)
**Función de test:** complejidad media de diseño + física de cabello + rango expresivo
**Línea:** Anime. Estilo visual NO definido aún — los anchors se generan en
anime limpio y neutro; la capa de estilo (LoRA de estudio) se decide después.

---

## Atributos bloqueados (innegociables)

| Atributo | Valor canónico |
|---|---|
| Edad | 22 (fija) |
| Facciones | Nórdicas: rostro ovalado, pómulos altos, mandíbula definida suave |
| Ojos | Azul hielo, grandes, rasgados hacia arriba levemente |
| Cejas | Rubias oscuras, rectas, definidas |
| Nariz | Recta y fina |
| Labios | Medios, tono rosa natural |
| Piel | Clara fría (porcelana nórdica), mejillas con rubor leve |
| Cabello (canónico) | Rubio platino, largo hasta media espalda, liso con movimiento, raya al centro, dos mechones frontales sueltos |
| Cuerpo | Atlético curvilíneo: hombros marcados, cintura definida, caderas anchas, ~172 cm |
| Marcador 1 | Cicatriz fina vertical que corta la ceja izquierda |
| Marcador 2 | Dos ear cuffs plateados en la oreja derecha |

## Outfit canónico (solo para el laboratorio)

Bodysuit azul marino ajustado + peto ligero plateado (una sola pieza, sin
ornamentos) + brazales a juego. Herencia del test "Kael": suficiente hardware
para estresar consistencia, no tanto como para volverla imposible en v1.
Variaciones de outfit: solo después de Gate 2.

## Canon negativo (nunca tiene)

Maquillaje pesado, cabello de colores fantasía, ojos de otro color,
accesorios extra (collares, anillos), tatuajes, orejas élficas.

---

## Master prompt (base, inglés)

```
anime illustration, clean lineart, 1girl, 22 years old, nordic features,
oval face, high cheekbones, ice-blue upturned eyes, straight thin nose,
platinum blonde long straight hair, center part, two loose front strands,
thin vertical scar through left eyebrow, two silver ear cuffs on right ear,
athletic curvy build, navy fitted bodysuit, light silver chestplate and
bracers, neutral grey background, soft even lighting
```

## Negative prompt (base)

```
extra accessories, jewelry, necklace, fantasy hair colors, elf ears,
heavy makeup, deformed hands, extra fingers, multiple views, text, watermark
```

---

## Protocolo de anchors (8 tomas, fondo neutro, luz uniforme)

1. `a1_frontal` — rostro frontal, expresión neutra
2. `a2_3q_izq` — tres cuartos izquierda
3. `a3_3q_der` — tres cuartos derecha
4. `a4_perfil` — perfil izquierdo
5. `a5_fullbody` — cuerpo completo frontal (valida proporciones + outfit)
6. `a6_sonrisa` — frontal, sonrisa abierta
7. `a7_enojo` — frontal, expresión de combate/enojo
8. `a8_accion` — pose dinámica media (valida cabello en movimiento)

**Validación:** grid visual + checklist de atributos bloqueados por anchor
(cicatriz ✓, ear cuffs ✓, color de ojos ✓, raya del cabello ✓...).
Los embeddings faciales NO son confiables en anime — no usar como gate duro.

---

## Registro

| Fecha | Evento | Resultado |
|---|---|---|
| — | Canon v1 redactado | Pendiente de firma |
