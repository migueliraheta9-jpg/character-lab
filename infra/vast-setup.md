# Infraestructura Vast.ai — character-lab

**Regla de gasto:** Vast NO se enciende hasta que Gate 0 (canon firmado)
esté cerrado. Este documento se ejecuta recién en esa fase.

## Perfiles de instancia

| Perfil | GPU | Uso | Cuándo |
|---|---|---|---|
| GEN | RTX 4090 24GB (~$0.30–0.40/h) | Generación de anchors, datasets y Gate 2 | Fase de laboratorio |
| TRAIN/VIDEO | 48GB (L40S / A6000 / RTX 6000 Ada) | LoRA training, video i2v/v2v | Solo si se llega a esa fase |

Template base: imagen Docker de ComfyUI actualizada del marketplace de Vast
(elegir la de mayor uso reciente; verificar que incluya ComfyUI-Manager).

## Volumen persistente (~200 GB)

```
/workspace/
├── ComfyUI/models/
│   ├── checkpoints/      # FLUX.2 (FP8) · Qwen-Image 2.0
│   ├── loras/
│   ├── controlnet/
│   └── video/            # Wan 2.2 (fase video, no en laboratorio)
├── character-lab/        # clon de este repo (git pull al iniciar)
└── outputs/              # se sincroniza a characters/*/outputs del repo
```

## Modelos a descargar (verificar versión/quantización al montar)

- **FLUX.2** en FP8 — motor realista principal (Valeria).
  ⚠️ Pendiente Bloque 0: verificar términos de licencia comercial de los
  pesos abiertos antes de facturar contenido generado con él.
- **Qwen-Image 2.0** — motor anime + edición (Astrid). Apache 2.0 ✅.
- (Fase video, después de Gate 2): Wan 2.2 i2v.

## Flujo de sesión estándar

1. Encender instancia GEN → `git pull` del repo en /workspace.
2. Cargar workflow correspondiente desde `workflows/`.
3. Generar batch → curar → copiar seleccionadas a `outputs/YYYY-MM-DD/`.
4. Correr `validation/identity_check.py` local o en la instancia.
5. Registrar resultado en el `CHARACTER.md` correspondiente (sección Registro).
6. **Apagar la instancia.** Nada queda encendido idle.

## Checklist Bloque 0 (antes del primer encendido)

- [ ] Canon de Astrid firmado
- [ ] Canon de Valeria firmado
- [ ] Licencia comercial FLUX.2 verificada (si es restrictiva → Qwen-Image 2.0
      asume también la línea realista)
- [ ] Repo subido a GitHub (privado)
