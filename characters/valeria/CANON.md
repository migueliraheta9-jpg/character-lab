# Valeria — Canon de identidad (v1, Sesión 1)

## Identidad
Valeria, 25 años, latina. Marcadores de identidad:
- Pecas densas en puente nasal y pómulos superiores
- Ojos avellana claros, almendrados, leve inclinación ascendente
- Cejas gruesas suavemente arqueadas
- Labios llenos con arco de cupido definido
- Lunar pequeño oscuro sobre la comisura izquierda del labio
- Hoyuelo superficial en mejilla derecha al sonreír
- Piel tostada cálida con textura realista
- Pelo castaño oscuro largo ondulado, balayage caramelo,
  raya al centro ligeramente cargada a la izquierda

## Parámetros canónicos
- Seed héroe: 794808565046336 (control_after_generate: fixed)
- Stack: FLUX.2-dev Q6_K GGUF (city96/FLUX.2-dev-gguf) +
  mistral_3_small_flux2_fp8.safetensors (Comfy-Org) +
  flux2-vae.safetensors
- ComfyUI v0.27.0 + ComfyUI-GGUF (city96)
- Workflow: flux2_gguf_valeria.json (base kombitz flux2 dev gguf)
- 1024x1024, 30 steps, FluxGuidance 4.0, sampler euler,
  batch_size 1, sin negative prompt
- Anchors A2–A5 generados con valeria_hero_v1.png como imagen
  de referencia (multi-reference de FLUX.2) y seed fija

## Prompts canónicos
### A1 — Héroe (frontal)
Editorial photograph, head-and-shoulders portrait of a young Latina
woman, 25 years old. Distinctive face: warm tan skin with realistic
texture and visible pores, light freckles scattered across the nose
bridge and upper cheeks, a small dark beauty mark above the left
corner of her lip, softly arched thick eyebrows, almond-shaped light
hazel eyes with a subtle upturn, full lips with a defined cupid's
bow, a single shallow dimple on the right cheek when smiling. Long
dark brown hair with caramel balayage, natural waves, parted
slightly off-center to the left. Soft glam natural makeup.
Front-facing, direct gaze at camera, relaxed confident expression
with a subtle closed-lip smile. Neutral seamless light-gray studio
background, soft even beauty lighting, 85mm lens look, sharp focus
on the face.

### A2 — Tres cuartos
Same woman as in the reference image, exact same face, freckles,
hazel eyes and caramel balayage hair. Editorial photograph,
head-and-shoulders portrait, face turned three-quarters to her
left, eyes toward camera, subtle closed-lip smile. Neutral seamless
light-gray studio background, soft even beauty lighting, 85mm lens
look.

### A3 — Perfil
Same woman as in the reference image, exact same face, freckles,
hazel eyes and caramel balayage hair. Editorial photograph, side
profile portrait facing left, relaxed neutral expression, hair
falling naturally over her shoulder. Neutral seamless light-gray
studio background, soft even beauty lighting, 85mm lens look.

### A4 — Cuerpo entero
Same woman as in the reference image, exact same face, freckles,
hazel eyes and caramel balayage hair. Full body editorial
photograph, standing relaxed with weight on one hip, wearing a
simple white fitted t-shirt and light-blue jeans, white sneakers,
athletic curvy figure. Neutral seamless light-gray studio
background, soft even lighting, 50mm lens look.

### A5 — Golden hour
Same woman as in the reference image, exact same face, freckles,
hazel eyes and caramel balayage hair. Photograph, half-body
portrait outdoors at golden hour, warm sunlight on her face, soft
long shadows, casual beige knit top, natural background softly
blurred, 85mm lens look.

## Notas de sesión
- A4 requirió 2 corridas: la primera salió con figura incorrecta.
  Lección: el cuerpo no está anclado por la referencia
  (head-and-shoulders); "athletic curvy figure" es ambiguo. TODO
  Sesión 2: redactar descripción corporal explícita y canónica.
- La cara en cuerpo entero a 1024px pierde detalle de marcadores.
  TODO fase 2: pase de face detailer + upscale para planos abiertos.
- Gate 1: APROBADO (~90% consistencia de identidad en 4 vistas).
