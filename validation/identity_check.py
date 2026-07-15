#!/usr/bin/env python3
"""
identity_check.py — Validación de identidad contra el set ancla.

Modos:
  real  : embeddings faciales ArcFace (insightface). Gate duro para
          personajes fotorrealistas. Umbral por defecto: 0.60 de coseno.
  anime : similitud CLIP como señal DÉBIL (los modelos de reconocimiento
          facial no son confiables en rostros anime). Solo orientativo;
          el gate real en anime es el grid visual + checklist de atributos.

Uso:
  python identity_check.py --anchors ../characters/valeria/anchors \
                           --candidates ../characters/valeria/outputs/2026-07-20 \
                           --mode real --threshold 0.60

Salida: tabla por imagen candidata con similitud media contra los anchors
y veredicto PASS/FAIL, más el resumen del batch.

Dependencias: ver requirements.txt (insightface + onnxruntime para modo real,
open-clip-torch para modo anime).
"""

import argparse
import sys
from pathlib import Path

import numpy as np

IMG_EXTS = {".png", ".jpg", ".jpeg", ".webp"}


def list_images(folder: Path):
    files = sorted(p for p in folder.iterdir()
                   if p.suffix.lower() in IMG_EXTS and p.is_file())
    if not files:
        sys.exit(f"[ERROR] No hay imágenes en {folder}")
    return files


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))


# ---------------------------------------------------------------- modo real
def embed_faces_arcface(paths):
    import cv2
    from insightface.app import FaceAnalysis

    app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
    app.prepare(ctx_id=0, det_size=(640, 640))

    embeddings = {}
    for p in paths:
        img = cv2.imread(str(p))
        if img is None:
            print(f"[WARN] No se pudo leer {p.name}, se omite")
            continue
        faces = app.get(img)
        if not faces:
            print(f"[WARN] Sin rostro detectado en {p.name}, se omite")
            continue
        # Rostro de mayor área si hay varios
        face = max(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]))
        embeddings[p.name] = face.normed_embedding
    return embeddings


# --------------------------------------------------------------- modo anime
def embed_clip(paths):
    import torch
    import open_clip
    from PIL import Image

    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-B-32", pretrained="laion2b_s34b_b79k")
    model.eval()

    embeddings = {}
    with torch.no_grad():
        for p in paths:
            try:
                img = preprocess(Image.open(p).convert("RGB")).unsqueeze(0)
            except Exception as e:
                print(f"[WARN] No se pudo leer {p.name}: {e}")
                continue
            feat = model.encode_image(img).squeeze(0).numpy()
            embeddings[p.name] = feat / (np.linalg.norm(feat) + 1e-8)
    return embeddings


# --------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Validación de identidad vs anchors")
    ap.add_argument("--anchors", required=True, type=Path)
    ap.add_argument("--candidates", required=True, type=Path)
    ap.add_argument("--mode", choices=["real", "anime"], default="real")
    ap.add_argument("--threshold", type=float, default=None,
                    help="Umbral de similitud (default: 0.60 real / 0.75 anime)")
    args = ap.parse_args()

    threshold = args.threshold if args.threshold is not None \
        else (0.60 if args.mode == "real" else 0.75)

    anchor_paths = list_images(args.anchors)
    cand_paths = list_images(args.candidates)

    embed = embed_faces_arcface if args.mode == "real" else embed_clip

    print(f"[i] Modo: {args.mode} | Umbral: {threshold:.2f}")
    print(f"[i] Anchors: {len(anchor_paths)} | Candidatas: {len(cand_paths)}\n")

    anchor_emb = embed(anchor_paths)
    if len(anchor_emb) < 3:
        sys.exit("[ERROR] Menos de 3 anchors utilizables. Revisa el set ancla.")

    # Coherencia interna del set ancla (autodiagnóstico)
    names = list(anchor_emb)
    pairs = [cosine(anchor_emb[a], anchor_emb[b])
             for i, a in enumerate(names) for b in names[i + 1:]]
    print(f"[i] Coherencia interna anchors: media {np.mean(pairs):.3f} "
          f"| mín {np.min(pairs):.3f}")
    if args.mode == "real" and np.mean(pairs) < threshold:
        print("[!!] El propio set ancla no es coherente. "
              "Arregla los anchors antes de validar candidatas.\n")

    cand_emb = embed(cand_paths)
    results, passed = [], 0
    for name, emb in cand_emb.items():
        sims = [cosine(emb, a) for a in anchor_emb.values()]
        mean_sim = float(np.mean(sims))
        ok = mean_sim >= threshold
        passed += ok
        results.append((name, mean_sim, ok))

    print(f"\n{'Imagen':<40}{'Similitud':>10}   Veredicto")
    print("-" * 65)
    for name, sim, ok in sorted(results, key=lambda r: -r[1]):
        print(f"{name:<40}{sim:>10.3f}   {'PASS' if ok else 'FAIL'}")

    total = len(results)
    rate = 100.0 * passed / total if total else 0.0
    print("-" * 65)
    print(f"Batch: {passed}/{total} PASS ({rate:.0f}%). "
          f"Gate 2 exige >= 80%. {'GO' if rate >= 80 else 'NO-GO'}")
    if args.mode == "anime":
        print("[i] Recordatorio: en anime esto es señal débil. "
              "El gate real es el grid visual + checklist de atributos.")


if __name__ == "__main__":
    main()
