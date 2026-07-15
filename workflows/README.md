# workflows/

JSONs de ComfyUI del laboratorio. Se agregan al montar la instancia
(los workflows dependen de las versiones exactas de nodos instalados,
por eso no se pre-fabrican aquí).

Planeados:

| Archivo | Motor | Propósito |
|---|---|---|
| `real_anchor_gen.json` | FLUX.2 FP8 | Anchors y datasets de Valeria (incluye pase de detalle facial) |
| `anime_anchor_gen.json` | Qwen-Image 2.0 | Anchors y datasets de Astrid |
| `real_ood_test.json` | FLUX.2 + multi-reference | Gate 2 fuera de distribución (Valeria) |
| `anime_ood_test.json` | Qwen-Image 2.0 + referencia | Gate 2 fuera de distribución (Astrid) |

Regla: cada workflow guardado aquí queda versionado en git junto con la
fecha y el resultado del batch en el Registro del personaje.
