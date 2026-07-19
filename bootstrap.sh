#!/usr/bin/env bash
# ============================================================
# bootstrap.sh — character-lab
# Instancia Vast cero → lista para generar, en un solo comando.
#
# USO (en la instancia, tras clonar el repo en /workspace):
#   export HF_TOKEN=tu_token
#   bash /workspace/character-lab/bootstrap.sh
#
# Aborta solo con veredicto claro (red mala => DESTROY).
# ============================================================
set -euo pipefail

echo "=============================================="
echo " character-lab bootstrap — $(date)"
echo "=============================================="

# ---------- 0. Prerrequisitos ----------
if [ -z "${HF_TOKEN:-}" ]; then
  echo "ERROR: exporta primero el token:  export HF_TOKEN=..."; exit 1
fi

nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || { echo "ERROR: sin GPU visible"; exit 1; }
df -h / | tail -1

apt-get update -qq && apt-get install -y -qq aria2 zip >/dev/null

# ---------- 1. Test de red (veredicto go/no-go) ----------
echo "--- Test de red: aria2 x16 contra HF (VAE ~321 MB) ---"
rm -f /tmp/vae_test.safetensors /tmp/vae_test.safetensors.aria2
T0=$SECONDS
aria2c -q -x16 -s16 --auto-file-renaming=false --allow-overwrite=true \
  -d /tmp -o vae_test.safetensors \
  "https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors"
DUR=$(( SECONDS - T0 )); [ "$DUR" -lt 1 ] && DUR=1
SPEED=$(( 321 / DUR ))
rm -f /tmp/vae_test.safetensors
echo "Velocidad efectiva: ~${SPEED} MiB/s (${DUR}s)"
if [ "$SPEED" -lt 15 ]; then
  echo "=============================================="
  echo " VEREDICTO: RED MALA (<15 MiB/s)."
  echo " DESTRUYE esta instancia y renta otra."
  echo " No se instaló nada. Pérdida: centavos."
  echo "=============================================="
  exit 2
fi
echo "VEREDICTO: red OK."

# ---------- 2. Token ----------
WHO=$(curl -s -H "Authorization: Bearer $HF_TOKEN" https://huggingface.co/api/whoami-v2 | head -c 200)
echo "whoami: $WHO"
echo "$WHO" | grep -q '"name"' && echo "=== TOKEN OK ===" || echo "AVISO: token no validado (los repos usados no son gated; continúo)."

# ---------- 3. Localizar ComfyUI ----------
COMFY=$(find /workspace /opt /root -maxdepth 3 -type d -name ComfyUI 2>/dev/null | head -1)
if [ -z "$COMFY" ]; then echo "ERROR: no hay ComfyUI en esta plantilla. Usa una plantilla de Vast con ComfyUI."; exit 1; fi
echo "ComfyUI en: $COMFY"
( cd "$COMFY" && git log -1 --format="ComfyUI version: %h %cd" --date=short )

# ---------- 4. Custom nodes ----------
cd "$COMFY/custom_nodes"
[ -d ComfyUI-GGUF ]          || git clone -q https://github.com/city96/ComfyUI-GGUF
[ -d ComfyUI-Impact-Pack ]   || git clone -q https://github.com/ltdrdata/ComfyUI-Impact-Pack
[ -d ComfyUI-Impact-Subpack ]|| git clone -q https://github.com/ltdrdata/ComfyUI-Impact-Subpack
pip install -q -r ComfyUI-GGUF/requirements.txt
pip install -q -r ComfyUI-Impact-Pack/requirements.txt
pip install -q -r ComfyUI-Impact-Subpack/requirements.txt
mkdir -p "$COMFY/models/diffusion_models" "$COMFY/models/text_encoders" "$COMFY/models/vae" \
         "$COMFY/models/ultralytics/bbox" "$COMFY/models/sams" "$COMFY/models/upscale_models"
echo "=== SETUP OK ==="

# ---------- 5. Descarga maestra (idempotente, reanuda parciales) ----------
cd "$COMFY/models"
cat > /tmp/descargas.txt << 'EOF'
https://huggingface.co/city96/FLUX.2-dev-gguf/resolve/main/flux2-dev-Q6_K.gguf
  dir=diffusion_models
  out=flux2-dev-Q6_K.gguf
https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/text_encoders/mistral_3_small_flux2_fp8.safetensors
  dir=text_encoders
  out=mistral_3_small_flux2_fp8.safetensors
https://huggingface.co/Comfy-Org/flux2-dev/resolve/main/split_files/vae/flux2-vae.safetensors
  dir=vae
  out=flux2-vae.safetensors
https://huggingface.co/Bingsu/adetailer/resolve/main/face_yolov8m.pt
  dir=ultralytics/bbox
  out=face_yolov8m.pt
https://huggingface.co/lokCX/4x-Ultrasharp/resolve/main/4x-UltraSharp.pth
  dir=upscale_models
  out=4x-UltraSharp.pth
https://huggingface.co/segments-arnaud/sam_vit_b/resolve/main/sam_vit_b_01ec64.pth
  dir=sams
  out=sam_vit_b_01ec64.pth
EOF
aria2c -x16 -s16 -j2 -c --auto-file-renaming=false --allow-overwrite=true \
  --summary-interval=30 --console-log-level=warn -i /tmp/descargas.txt
rm -f /tmp/descargas.txt

# ---------- 6. Workflows + referencia ----------
REPO=/workspace/character-lab
mkdir -p "$COMFY/user/default/workflows"
wget -q -O "$COMFY/user/default/workflows/flux2_gguf_valeria.json" \
  "https://www.kombitz.com/wp-content/uploads/2025/11/kombitz_flux2_dev_gguf.json" || \
  echo "AVISO: no bajó el workflow kombitz; cárgalo a mano."
[ -f "$REPO/detailer_standalone_v1.json" ] && \
  cp "$REPO/detailer_standalone_v1.json" "$COMFY/user/default/workflows/" && \
  echo "Detailer standalone instalado."
[ -f "$REPO/wf3_unificado_valeria_v1.json" ] && \
  cp "$REPO/wf3_unificado_valeria_v1.json" "$COMFY/user/default/workflows/" && \
  echo "WF3 unificado instalado."
if [ -d "$REPO/characters/valeria/anchors" ]; then
  cp "$REPO/characters/valeria/anchors/"*.png "$COMFY/input/" 2>/dev/null && \
  echo "Anchors de Valeria copiados a input/ (disponibles como referencia)."
fi

# ---------- 7. Reinicio del servicio ----------
pkill -f "main.py" || true
sleep 25
ss -tlnp | grep 8188 || echo "AVISO: 8188 no visible aún; espera 30s y revisa."

# ---------- 8. Resumen ----------
echo "----------------------------------------------"
ls -lh "$COMFY/models/diffusion_models" "$COMFY/models/text_encoders" "$COMFY/models/vae" \
       "$COMFY/models/ultralytics/bbox" "$COMFY/models/sams" "$COMFY/models/upscale_models" | grep -v put_
df -h / | tail -1
echo "=============================================="
echo " BOOTSTRAP COMPLETO — abre la UI (puerto 8188)"
echo " Workflows listos: flux2_gguf_valeria + detailer_standalone_v1"
echo " Seed canónica: 794808565046336 (fixed)"
echo "=============================================="
