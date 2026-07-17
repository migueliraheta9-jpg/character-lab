# RUNBOOK — Sesión 1: Generación de anchors (Gate 1)

**Objetivo:** salir de la sesión con los 8 anchors de Valeria y los 8 de
Astrid, validados y commiteados. Nada más. No es sesión de exploración.

**Presupuesto:** máx. $10 (corte duro). Estimado real: $4–7.
**Duración estimada:** 2.5–4 h (incluye descargas de modelos, solo la 1ª vez).
**Estado de licencia:** fase de laboratorio cubierta por la licencia no
comercial de FLUX.2 dev (testing/evaluación/I+D en no-producción está
permitido para entidades comerciales). Producción comercial = decisión
post-Gate 2 (tier BFL / API licenciada / Qwen asume realista). Los LoRA
entrenados sobre FLUX.2 dev heredan licencia no comercial — no entrenar
LoRAs de producción sobre dev.

---

## 0 · Pre-vuelo (antes de encender nada)

- [ ] Cuenta Vast.ai con ≥ $15 de crédito.
- [ ] Cuenta Hugging Face: aceptar los términos del repo gated
      `black-forest-labs/FLUX.2-dev` (se hace una vez, en la web).
- [ ] Token HF **real** de lectura creado (Settings → Access Tokens).
      ⚠️ Nunca commitearlo al repo ni pegarlo en archivos: se exporta como
      variable de entorno en la instancia y muere con ella.
- [ ] Repo `character-lab` accesible (URL + PAT de GitHub si es privado).
- [ ] Los dos CHARACTER.md releídos: el master prompt de cada uno es la
      única fuente de verdad de la sesión.

## 1 · Instancia

**Recomendada: 48 GB VRAM (L40S / RTX A6000 / RTX 6000 Ada), ~$0.50–0.80/h.**
Razón: FLUX.2 dev es un modelo de 32B; en 24 GB corre solo con cuantización
agresiva (GGUF) + offloading, y esa fricción cuesta más que el dólar extra
por hora. La 4090 de 24 GB queda como plan B (con GGUF Q5) si no hay 48 GB
disponibles a buen precio.

Filtros en Vast: GPU 48GB · disco ≥ 150 GB · reliability > 99% ·
bandwidth > 500 Mbps · template: **ComfyUI** (imagen oficial/más usada del
marketplace, con ComfyUI-Manager incluido).

## 2 · Setup de la instancia (una sola vez por sesión)

```bash
# 1. Clonar el repo (en /workspace)
git clone https://github.com/migueliraheta9-jpg/character-lab.git

# 2. Exportar token HF (NO escribirlo en ningún archivo)
export HF_TOKEN=<tu_token_real>

# 3. Descargas (a ComfyUI/models/):
#    - FLUX.2-dev en FP8 + su text encoder (repo oficial BFL en HF;
#      verificar en la model card los archivos exactos para ComfyUI)
#    - Qwen-Image 2.0 (quantización recomendada de la model card)
#    - Modelo de detailer facial (impact-pack / FaceDetailer con
#      detector de rostro) vía ComfyUI-Manager
```

Verificación de humo: generar 1 imagen cualquiera con cada motor a
resolución baja. Si ambos responden, empieza el reloj de la sesión.

## 3 · Valeria primero (FLUX.2 dev + FaceDetailer)

**Fase héroe:** 8–12 candidatas de `a1_frontal` con el master prompt de su
CHARACTER.md, 1024×1024, semillas libres. Curar UNA héroe con criterio:
identidad clara + lunar y cicatriz presentes + piel con poros (ampliar a
100%). Si toda la tanda sale porcelana → activar/ajustar FaceDetailer y
bajar términos de belleza del prompt ANTES de seguir. No avanzar con héroe
plástica: contamina todo lo demás.

**Fase set:** las 7 tomas restantes con la héroe como imagen de referencia
(multi-reference de FLUX.2), 2–4 candidatas por toma, cambiando solo lo
que la toma pide (ángulo/expresión/encuadre). Curar 1 por toma.

**Gate 1 (en la propia instancia o local):**
```bash
pip install -r character-lab/validation/requirements.txt
python character-lab/validation/identity_check.py \
  --anchors character-lab/characters/valeria/anchors \
  --candidates character-lab/characters/valeria/anchors --mode real
```
La coherencia interna del set debe dar media ≥ 0.60. Revisión visual de
piel en `a5_closeup` y `a8_luz_dura`. PASS → copiar a `anchors/` y commit.

## 4 · Astrid (Qwen-Image 2.0)

Mismo protocolo: héroe frontal (8–12 candidatas, estilo anime limpio
neutro, sin tokens de estilo de ningún estudio) → curar por checklist de
atributos (cicatriz en ceja, ear cuffs, ojos azul hielo, raya al centro,
peto) → 7 tomas restantes con la héroe como referencia → grid visual 4×4.
El script en modo `anime` es solo señal orientativa; el gate es la
checklist. PASS → `anchors/` y commit.

## 5 · Cierre de sesión (obligatorio, en orden)

1. Commit + push: anchors de ambos personajes + JSONs de los workflows
   usados a `workflows/` (`real_anchor_gen.json`, `anime_anchor_gen.json`).
2. Actualizar la tabla Registro de cada CHARACTER.md (fecha, motor,
   resultado del gate, similitud media).
3. **Destruir/parar la instancia en Vast.** Verificar en el panel que no
   quedó nada facturando.
4. Anotar el gasto real de la sesión (para calibrar presupuestos futuros).

## 6 · Criterios de corte y troubleshooting

| Síntoma | Acción |
|---|---|
| Piel porcelana persistente (Valeria) | FaceDetailer más agresivo; quitar adjetivos de belleza del prompt; si persiste 30 min → cerrar sesión y replantear motor conmigo |
| Deriva de identidad entre tomas | Subir peso de la referencia; regenerar solo la toma desviada; verificar que la héroe va en cada generación |
| Marcadores desaparecen (lunar/cicatriz/ear cuffs) | Reforzarlos al inicio del prompt; descartar candidatas sin marcador (es binario) |
| Qwen no sostiene el diseño de Astrid | Simplificar peto a "silver chest armor" y reintentar; anotar para decidir si el outfit v1 era demasiado ambicioso |
| Presupuesto llega a $10 | Sesión termina, pase lo que pase. Se retoma con diagnóstico, no con inercia |

**Regla de oro de la sesión:** cada problema se corrige en el prompt o el
workflow, nunca tirando seeds al azar. Si en 3 intentos dirigidos no sale,
se anota y se consulta — el laboratorio mide al pipeline, no a la suerte.

## Lecciones Sesión 1 (ejecutada 2026-07-16)

- Filtro obligatorio al rentar en Vast: Internet Down ≥500 Mbps
  (además de: 1x RTX 5090 verified, ≤$0.60/hr, reliability ≥99%,
  disco 150 GB antes de rentar).
- Paso 0 en toda instancia nueva: test de red con aria2 -x16
  contra Hugging Face (archivo VAE ~300MB). Veredicto: ≥30 MiB/s
  verde; 15–30 aceptable; <15 Destroy. El curl de una sola
  conexión solo sirve para descartar limones absolutos (muchos
  hosts capan por stream, no en total).
- No usar speed.cloudflare.com como test: devuelve 403 desde IPs
  de datacenter.
- Descargas siempre con aria2c -x16 -s16 -c
  --auto-file-renaming=false --allow-overwrite=true (evita
  duplicados .1.gguf sobre parciales de wget).
- Nunca pegar comandos en una terminal con un proceso en primer
  plano: se encolan y se ejecutan en cadena. Descarga larga =
  terminal dedicada.
- Qwen-Image 2.0 NO tiene pesos abiertos (feb 2026, solo API
  BaiLian). Sustituto canónico: Qwen-Image-2512 Q8_0 GGUF
  (unsloth) — descargado en S1, quedó sin usar. Pendiente
  evaluarlo en Sesión 2.
- Se destruyeron 2 instancias por red mala antes de la buena;
  costo total de sesión ~$2 de $10.
