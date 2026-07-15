# Bloque listo para pegar en Claude Code

> Contexto para Miguel: pega esto en Claude Code desde la carpeta donde
> descomprimiste `character-lab/`. ACEPTA lo que Code proponga solo si se
> limita a: crear el repo privado, commit inicial y push. NO ACEPTES si
> propone modificar el contenido de los CHARACTER.md o generar workflows
> de ComfyUI en esta fase — eso viene después de Gate 0.

---

Tengo la carpeta `character-lab/` en el directorio actual. Es un laboratorio
de identidad de personajes IA (dos personajes de prueba: astrid/anime y
valeria/realista) con protocolo de validación por gates.

Tareas, en este orden y nada más:

1. Inicializa git en `character-lab/`, crea un `.gitignore` apropiado que
   excluya: imágenes pesadas de `characters/*/datasets/` y
   `characters/*/outputs/` (mantén los `.gitkeep`), `__pycache__/`,
   `.venv/`, y modelos/checkpoints (`*.safetensors`, `*.ckpt`, `*.onnx`).
   Los `anchors/` SÍ se versionan (son el activo de identidad, pocas
   imágenes).
2. Crea el repo privado `character-lab` en mi cuenta de GitHub
   (migueliraheta9-jpg) usando `gh repo create`.
3. Commit inicial con mensaje: `lab: estructura base + canon v1 (pendiente
   Gate 0)` y push a main.
4. Verifica que el repo quedó privado y muéstrame la URL.

No modifiques el contenido de ningún archivo existente. No instales
dependencias de Python. No crees workflows de ComfyUI.
