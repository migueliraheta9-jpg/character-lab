# Guía de Implementación — Pipeline de Anchors de Identidad (v1)

**Origen:** Sesión 1 de character-lab (2026-07-16, Gate 1 aprobado con Valeria).
**Alcance:** de instancia cero a set de anchors validado, commiteado y con cierre limpio.
**Stack:** Vast.ai (RTX 5090 32GB) · ComfyUI v0.27+ · FLUX.2-dev Q6_K GGUF · ComfyUI-GGUF.
**Uso:** reemplazar `<PERSONAJE>` por el personaje de la sesión (ej. `astrid`). Los comandos se pegan tal cual, en orden, salvo donde se indique `<...>`.

> Principio rector: el personaje vive en el repo (anchors + canon + seed). Los modelos
> son commodity re-descargable. Se destruye la instancia al cierre, siempre.

---

## FASE 0 — Rentado de instancia (consola Vast)

Filtros obligatorios, en este orden:

1. GPU: **1x RTX 5090** · **Verified**
2. Reliability: **≥ 99%**
3. Precio: **≤ $0.60/hr**
4. **Internet Down: ≥ 500 Mbps** (slider Internet Speed; si el precio se dispara, 300–400 Mbps es aceptable)
5. **Disco: 150 GB fijado ANTES de rentar** (el slider de disco no se puede cambiar después)

⚠️ Los Mbps que muestra Vast los reporta el host — no son confiables. El filtro reduce limones; el veredicto real es el test de la Fase 1.

---

## FASE 1 — Paso 0: test de red (ANTES de invertir cualquier setup)

En cuanto la instancia esté Running, en la terminal:

```bash
# Sanity check de GPU y disco
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
df -h / | tail -1

# Test 1 — conexión única contra la fuente real (HF). Solo descarta limones absolutos.
curl -sL --max-time 25 -o /dev/null -w "HF:  HTTP %{http_code} | %{speed_download} bytes/s\n" \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors"
```

Lectura del Test 1:

| Resultado | Acción |
|---|---|
| HTTP 200, velocidad KB/s (5–6 dígitos) | **Destroy inmediato.** Host limón. |
| HTTP 200, ≥ 1 MB/s (7+ dígitos) | Pasar al Test 2 — muchos hosts capan por stream, no en total. |
| HTTP 000 | Red aún no levanta: esperar 60 s, repetir una vez, si persiste Destroy. |

```bash
# Test 2 — veredicto real: aria2 con 16 conexiones contra el mismo archivo (~300 MB)
apt-get update -qq && apt-get install -y -qq aria2
cd /tmp
aria2c -x16 -s16 --auto-file-renaming=false --allow-overwrite=true \
  -o vae_test.safetensors \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors"
rm -f vae_test.safetensors
```

Veredicto sobre el `avg speed` del resumen final de aria2:

| avg speed | Veredicto |
|---|---|
| ≥ 30 MiB/s | Verde total (77 GB ≈ 40 min o menos). Continuar. |
| 15–30 MiB/s | Aceptable (~1 h de descarga). Continuar. |
| < 15 MiB/s | **Destroy.** El cap es del uplink del host; aria2 no lo salva. |

⚠️ NO usar `speed.cloudflare.com` como test: devuelve HTTP 403 desde IPs de datacenter (falso negativo).

---

## FASE 2 — Pre-vuelo (repo + token)

1. GitHub → repo `character-lab` → Settings → **Make public**
2. Clonar:

```bash
cd /workspace
git clone https://github.com/<USUARIO>/character-lab.git
```

3. GitHub → **Make private** de nuevo (inmediatamente después del clone)
4. Exportar y validar el token HF (vive en Bitwarden, Read scope):

```bash
export HF_TOKEN=<TOKEN_REAL>
curl -s -H "Authorization: Bearer $HF_TOKEN" https://huggingface.co/api/whoami-v2
```

Go/no-go: el curl devuelve un JSON con tu usuario.

> Nota: los repos GGUF usados (city96, Comfy-Org, unsloth) NO son gated — el token es
> cinturón y tirantes. El único gated es el original de BFL, que no se toca.
> Higiene: el token queda en `.bash_history`; aceptable en instancia efímera,
> pero jamás pegarlo en archivos del repo.

---

## FASE 3 — Bloque 1: Setup (ComfyUI + nodo GGUF)

```bash
COMFY=$(find /workspace /opt /root -maxdepth 3 -type d -name ComfyUI 2>/dev/null | head -1)
echo "ComfyUI en: $COMFY"
cd "$COMFY" && git log -1 --format="ComfyUI version: %h %cd" --date=short
cd "$COMFY/custom_nodes" && git clone https://github.com/city96/ComfyUI-GGUF && pip install -q -r ComfyUI-GGUF/requirements.txt
mkdir -p "$COMFY/models/diffusion_models" "$COMFY/models/text_encoders" "$COMFY/models/vae"
echo "=== SETUP OK ==="
```

Go/no-go (las tres):
1. `ComfyUI en:` imprime ruta no vacía
2. Fecha de versión **≥ diciembre 2025** (soporte FLUX.2). Si la plantilla trae HEAD detached en un tag reciente: NO correr `git pull`, es correcto así.
3. `=== SETUP OK ===`

---

## FASE 4 — Bloque 2: Descarga maestra (~77 GB, un solo comando)

**Regla de disciplina: desde que arranca, esa terminal NO se toca** (lo que se pega con un proceso en primer plano se encola y explota en cadena). Todo lo demás, en una segunda terminal.

```bash
cd "$COMFY/models"
cat > descargas.txt << 'EOF'
https://huggingface.co/city96/FLUX.2-dev-gguf/resolve/main/flux2-dev-Q6_K.gguf
  dir=diffusion_models
  out=flux2-dev-Q6_K.gguf
https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/text_encoders/mistral_3_small_flux2_fp8.safetensors
  dir=text_encoders
  out=mistral_3_small_flux2_fp8.safetensors
https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors
  dir=vae
  out=flux2-vae.safetensors
https://huggingface.co/unsloth/Qwen-Image-2512-GGUF/resolve/main/qwen-image-2512-Q8_0.gguf
  dir=diffusion_models
  out=qwen-image-2512-Q8_0.gguf
https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
  dir=text_encoders
  out=qwen_2.5_vl_7b_fp8_scaled.safetensors
https://huggingface.co/Comfy-Org/Qwen-Image_ComfyUI/resolve/main/split_files/vae/qwen_image_vae.safetensors
  dir=vae
  out=qwen_image_vae.safetensors
EOF
aria2c -x16 -s16 -j2 -c --auto-file-renaming=false --allow-overwrite=true \
  --summary-interval=30 --console-log-level=warn -i descargas.txt
```

Notas:
- Flags anti-desastre: `-c` reanuda; `--auto-file-renaming=false` evita duplicados `.1.gguf` sobre parciales de wget; `-j2` baja 2 archivos en paralelo con 16 streams cada uno.
- Fallback FLUX.2 si Q6_K da OOM en generación (32 GB va al límite): `flux2-dev-Q5_K_M.gguf` (24.1 GB), misma URL cambiando el nombre.
- Qwen-Image-2512 sustituye a "Qwen-Image 2.0" del plan original: 2.0 NO tiene pesos abiertos (feb 2026, solo API BaiLian).

**Verificación al terminar:**

```bash
ls -lh "$COMFY/models/diffusion_models" "$COMFY/models/text_encoders" "$COMFY/models/vae"
df -h / | tail -1
rm -f "$COMFY/models/descargas.txt"
```

Tamaños esperados: flux2 Q6_K ~26G · qwen Q8_0 ~21G · mistral fp8 ~17G · qwen encoder ~8.8G · VAEs 321M y 243M. Los archivos `put_X_here` de 0 bytes son marcadores de plantilla, ignorar.

---

## FASE 5 — Reinicio del servicio ComfyUI

Las plantillas de Vast corren ComfyUI como **servicio supervisado** detrás de un proxy Caddy (por eso el puerto 8188 aparece "in use" si intentas arrancarlo a mano — no lo hagas). El servicio arrancó antes del setup, así que hay que reiniciarlo para que cargue el nodo GGUF y los modelos. Supervisor lo revive solo:

```bash
pkill -f "main.py"; sleep 25
ss -tlnp | grep 8188
```

Go/no-go: `ss` muestra el 8188 escuchando de nuevo (python detrás de caddy).

**Acceso a la UI:** consola Vast → botón **Open** → puerto **8188**.

Verificación en la UI: doble clic en lienzo → buscar `GGUF` → deben existir **Unet Loader (GGUF)** y **CLIPLoader (GGUF)**.

---

## FASE 6 — Workflow

⚠️ NO usar las plantillas de la galería de ComfyUI: las de "Flux 2" son API (cobran créditos, no usan tu GPU) o Image Edit con modelos safetensors que no tenemos. Workflow validado (kombitz, t2i + referencias opcionales):

```bash
wget -O "$COMFY/user/default/workflows/flux2_gguf_<PERSONAJE>.json" \
  "https://www.kombitz.com/wp-content/uploads/2025/11/kombitz_flux2_dev_gguf.json"
```

En la UI: F5 → barra lateral **Workflows** → abrir `flux2_gguf_<PERSONAJE>`.

Cirugía (el JSON apunta a archivos con otros nombres — errores "faltan modelos" esperados):

1. **Borrar** el nodo "Cargar Modelo de Difusión" (cargador safetensors alternativo). Verificar que la salida MODELO del **Unet Loader (GGUF)** quede conectada a la entrada modelo de GuíaBásica.
2. **Unet Loader (GGUF)** → `flux2-dev-Q6_K.gguf`
3. **Cargar CLIP** → `mistral_3_small_flux2_fp8.safetensors` · tipo: `flux2`
4. **Cargar VAE** → `flux2-vae.safetensors` (suele coincidir ya)

Parámetros canónicos:

| Parámetro | Valor |
|---|---|
| width × height | 1024 × 1024 (iteración; alta resolución en fase de producción) |
| Flux2Scheduler → pasos | 30 |
| FluxGuidance | 4.0 |
| sampler | euler |
| batch_size (tamaño_lote) | 1 |
| negative prompt | no existe en FLUX.2 |

Primera generación: varios minutos (carga de 26G+17G a VRAM). Las siguientes, rápidas.

---

## FASE 7 — Protocolo de generación de identidad

### 7.1 Exploración del héroe
1. Seed: `control_after_generate` = **randomize**
2. Prompt héroe con **marcadores de identidad específicos y asimétricos** (pecas localizadas, lunar con posición, hoyuelo unilateral, forma de ojos/cejas, etc.). Los adjetivos de categoría ("latina", "influencer") generan promedios genéricos — la identidad está en los rasgos concretos.
3. Correr **6 veces** → 6 candidatas.

### 7.2 Selección y congelación
1. Elegir UNA. Criterio: ¿la reconocerías en una multitud? Marcadores visibles y claros.
2. Historial → anotar la **seed** de la ganadora → escribirla en Ruido aleatorio → `control_after_generate` = **fixed**. Esa seed es el ADN del personaje: va al CANON.
3. Archivar el héroe (los nombres de output llevan backslash literal — comillas simples obligatorias):

```bash
cd /workspace/ComfyUI/output && ls -lht | head -10
cp 'Flux2\ComfyUI-<FECHA>_<NNNNN>_.png' <personaje>_hero_v1.png
mkdir -p /workspace/character-lab/characters/<PERSONAJE>/anchors
cp <personaje>_hero_v1.png /workspace/character-lab/characters/<PERSONAJE>/anchors/
cp <personaje>_hero_v1.png /workspace/ComfyUI/input/    # los nodos de referencia leen de input/, no de output/
```

### 7.3 Set de anchors (multi-referencia)
1. UI: F5 → primer nodo de referencia (Step 3) → clic derecho → **Modo: Siempre** (quitar bypass) → dropdown → `<personaje>_hero_v1.png`. El segundo nodo de referencia queda en bypass.
2. Seed fija + referencia fija: **la única variable entre corridas es el prompt.**
3. Plantilla de prompt del set — todos empiezan con el candado de identidad:

> `Same woman as in the reference image, exact same face, <MARCADORES CLAVE>.` + descripción de la vista.

Vistas mínimas del set: **A2** tres cuartos · **A3** perfil · **A4** cuerpo entero · **A5** cambio de iluminación (prueba de robustez, ej. golden hour exterior).

4. Una corrida por prompt, una imagen por corrida (batch 1).

⚠️ Lección A4: la referencia head-and-shoulders NO ancla el cuerpo — el cuerpo lo decide el prompt, y adjetivos ambiguos ("athletic curvy") varían entre corridas. El cuerpo requiere descripción explícita canónica. Si una vista sale mal: se ajusta ese prompt puntual, NO se vuelve a randomize.

5. Archivar el set (verificar números reales con `ls -lht`; los descartes no se copian a anchors ni se borran):

```bash
cd /workspace/ComfyUI/output
cp 'Flux2\ComfyUI-<FECHA>_<NN>_.png' <personaje>_anchor_02_3q.png
cp 'Flux2\ComfyUI-<FECHA>_<NN>_.png' <personaje>_anchor_03_profile.png
cp 'Flux2\ComfyUI-<FECHA>_<NN>_.png' <personaje>_anchor_04_fullbody.png
cp 'Flux2\ComfyUI-<FECHA>_<NN>_.png' <personaje>_anchor_05_golden.png
cp <personaje>_anchor_0*.png /workspace/character-lab/characters/<PERSONAJE>/anchors/
ls -lh /workspace/character-lab/characters/<PERSONAJE>/anchors/
```

### 7.4 Gate 1
Comparar las 4 vistas contra el héroe: misma cara reconocible, marcadores presentes en cada vista. Umbral: **≥ 80% de consistencia** → aprobado. Nota conocida: en cuerpo entero a 1024px los marcadores faciales pierden detalle (pendiente fase 2: face detailer + upscale).

---

## FASE 8 — Cierre de sesión

### 8.1 Zip y descarga al PC
```bash
cd /workspace/character-lab/characters/<PERSONAJE>/anchors
zip /workspace/<personaje>_anchors_s<N>.zip *.png
ls -lh /workspace/<personaje>_anchors_s<N>.zip
```
Descargar vía **Jupyter** (pestaña de la instancia) → `/workspace/` → clic derecho al zip → Download. **Verificar el zip en el PC ANTES de destruir.**

### 8.2 Destroy
Consola Vast → **Destroy** (no Stop: Stop factura storage y no garantiza re-arranque). Verificar que desaparece de Instances. Cerrar terminal NO detiene facturación.

### 8.3 Commit vía Claude Code local
En el clone local del repo, bloque para Code con: extraer anchors → crear/actualizar `characters/<PERSONAJE>/CANON.md` (identidad + marcadores + seed + stack + prompts A1–A5 + notas) → actualizar lecciones del RUNBOOK → `git add/commit/push`. Regla: si Code propone tocar cualquier otra cosa del repo, NO aceptar.

---

## ANEXO — Troubleshooting (lecciones Sesión 1)

| Síntoma | Causa | Acción |
|---|---|---|
| Descarga a KB/s con wget | Host con uplink malo O cap por stream | Test aria2 -x16; si sigue <15 MiB/s → Destroy |
| `speed.cloudflare.com` da 403 / 0 bytes | CF bloquea IPs de datacenter | Ignorar; testear siempre contra HF |
| aria2 crea `archivo.1.gguf` | Parcial previo de wget sin archivo de control | `rm` de parciales + flags `--auto-file-renaming=false --allow-overwrite=true` |
| Comandos "fantasma" se ejecutan solos tras Ctrl+C | Se pegó texto con proceso en primer plano: quedó encolado | Nunca pegar sobre proceso activo; terminal dedicada por descarga |
| "Port 8188 already in use" al arrancar ComfyUI | La plantilla ya lo corre como servicio tras Caddy | No arrancar a mano; `pkill -f main.py` para reiniciar (supervisor lo revive) |
| Plantillas Flux 2 de la galería fallan / piden créditos | Son API o Image Edit con otros modelos | Usar el JSON de la Fase 6 |
| `cp` falla a `anchors/` | GitHub no conserva carpetas vacías del repo | `mkdir -p` antes de copiar |
| OOM / offload agresivo en generación | Q6_K (27.4 GB) al límite en 32 GB | Cambiar a Q5_K_M (24.1 GB) |
| Nodo de referencia no lista la imagen | Lee de `input/`, no de `output/` | `cp` a `/workspace/ComfyUI/input/` + F5 |

---

## Presupuesto de referencia (Sesión 1 real)

- 2 instancias destruidas por red mala: centavos
- Instancia buena: ~3.5 h ≈ $2 (descarga 77 GB en ~28 min a 100+ MiB/s)
- **Total: ~$2 de un corte duro de $10.** Con protocolo endurecido, una sesión de reconstrucción + generación debería rondar $1–1.5.
