# character-lab

Laboratorio de identidad de personajes IA. Objetivo: validar un pipeline de
**consistencia + hiperrealismo** con dos personajes de prueba antes de escalar
a producción (campañas / anime).

> Principio rector: **el personaje vive en este repo, no en ningún modelo.**
> Los anchors + el canon son el activo portable. Los modelos (FLUX.2, Qwen,
> Seedream, Wan) son motores intercambiables.

---

## Personajes de prueba

| Personaje | Línea | Función de test |
|---|---|---|
| `astrid` | Anime | Complejidad de diseño (outfit + cabello con física) y rango expresivo |
| `valeria` | Realista | Piel humana en primeros planos (anti-porcelana) y consistencia de identidad |

Los nombres son placeholders de laboratorio; el IP final se define después.

---

## Protocolo de validación (gates GO/NO-GO)

### Gate 0 — Canon firmado
`CHARACTER.md` de cada personaje revisado y aprobado por Miguel.
Nada se genera antes de esto.

### Gate 1 — Set ancla
- 8 anchors por personaje (ver protocolo de tomas en cada `CHARACTER.md`).
- **Valeria (realista):** similitud de embeddings faciales entre pares de
  anchors ≥ 0.60 de coseno (script `validation/identity_check.py`, modo `real`)
  **y** piel con textura visible en primer plano (juicio visual: poros/brillo,
  no porcelana).
- **Astrid (anime):** los embeddings faciales no son confiables en anime;
  la validación es grid visual 4×4 + checklist de atributos bloqueados
  (el script en modo `anime` da una señal débil vía CLIP, solo orientativa).

### Gate 2 — Fuera de distribución
12–16 generaciones con escenas/ropa/luz que NO están en los anchors,
sin describir rasgos faciales en el prompt. Pasa con ≥ 80% de identidad
sostenida. Si pasa → el pipeline de identidad está resuelto y se abre
la fase de producción (o el LoRA, si el volumen lo justifica).

---

## Convenciones

- **Prompts en inglés** (los modelos rinden mejor); documentación en español.
- **1 cabello canónico por personaje** durante todo el laboratorio.
  Variaciones de peinado solo después de pasar Gate 2.
- **Edad fija en un número**, nunca rango.
- Cada anchor se nombra `a{n}_{descripcion}.png` (ej. `a1_frontal.png`).
- Todo output curado lleva fecha: `outputs/YYYY-MM-DD/`.
- Los checkpoints LoRA (si se llega a esa fase) van en
  `characters/{nombre}/datasets/` → entrenan → resultado se registra en
  `CHARACTER.md` (sección Registro).

## Estructura

```
character-lab/
├── README.md
├── INSTRUCCIONES_CLAUDE_CODE.md   # Bloque listo para pegar en Claude Code
├── characters/
│   ├── astrid/    (CHARACTER.md + anchors/ + datasets/ + outputs/)
│   └── valeria/   (CHARACTER.md + anchors/ + datasets/ + outputs/)
├── workflows/     # JSONs de ComfyUI (se agregan al montar la instancia)
├── validation/    # identity_check.py + requirements.txt
└── infra/         # vast-setup.md
```
