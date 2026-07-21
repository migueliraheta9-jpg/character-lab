# Runbook Sesión 2 — Valeria: de identidad a producción

## Decisión estratégica (2026-07-16)
Profundizar Valeria antes de crear a Astrid. Valeria es el activo
comercial; Astrid nace después, sobre el pipeline ya industrializado.

## Objetivo: Gate 2
3 imágenes de contenido real (gym, calle Miami, café) publicables en
Instagram con identidad intacta.

## Bloques
1. Cuerpo canónico: redactar descripción corporal explícita (cierra
   TODO A4 del CANON), generar anchor de cuerpo en alta resolución,
   sumar al CANON.
2. Set de expresiones: 4-5 anchors (risa abierta, seria, mirada
   lateral, gesto casual). Doble propósito: robustez + dataset del
   futuro LoRA (Sesión 3).
3. Pipeline de detalle: face detailer + upscale 2K para planos
   abiertos.
4. Prueba de producción: las 3 imágenes del Gate 2.

## Paso 0 (antes de rentar): crear Proyecto de Claude "character-lab"
con GUIA_PIPELINE_ANCHORS_v1.md y characters/valeria/CANON.md como
conocimiento del proyecto.

## Infraestructura
Seguir GUIA_PIPELINE_ANCHORS_v1.md (Fases 0-6). Presupuesto: corte
duro $10. Qwen-2512: solo si sobra presupuesto, no es crítico.

## Roadmap posterior
Sesión 3: LoRA de identidad (dataset ~12-15 imágenes de S1+S2) →
abre producción en volumen y video (LTX). Astrid: después de Gate 2.

## Estado (parcial, 2026-07-17)
Completado: bloques 1 y 2 (cuerpo canónico + set expresiones).
Pendiente para próxima sesión GPU: probar detailer_standalone_v1.json
(bloque 3), escenas C1-C3 y veredicto Gate 2 (bloque 4).

Infra: instancia de 412 MiB/s validada con filtro de red; setup
completo en ~10 min con Bloque B; SAM se descarga del mirror HF
segments-arnaud/sam_vit_b (Meta bloquea datacenters). Workflow
monolítico con detailer integrado: descartado (imágenes negras);
arquitectura definitiva: generación (s2) + detailer standalone como
post-proceso.

## Lecciones
- El zip de cierre se hace ANTES de cualquier otro paso final y se
  verifica el conteo en PC antes del Destroy: las descargas
  individuales desde Jupyter se atascan en ráfagas. Siempre bajar
  zip único (`zip -r valeria_sN.zip valeria/`).
- 9 refinadas (detail 00005-00013) se perdieron con el Destroy:
  re-generarlas es el primer bloque de S3 (las bases están a salvo y
  el proceso es reproducible).
- Gate 2 formalmente PENDIENTE hasta re-refinar las escenas.
- WF3 unificado creado; estreno con prueba controlada en S3
  (fallback: Ctrl+B al grupo detailer o los 2 workflows probados).

## S3 pendientes
- Verificar tooling de entrenamiento LoRA sobre FLUX.2-dev vs Klein
  9B con datos frescos.
- Verificar términos de licencia BFL para uso comercial de outputs.
- Atributos de Civitai: ecosistema maduro solo en Klein; re-evaluar
  en S4.

## Hallazgos externos (2026-07-19) — track de realismo y motor secundario

Fuente evaluada: workflow "Flux.2 Klein + Refiner v2.0" (Civitai,
ShinobiSat). El archivo NO se adopta (motor Klein 9B incompatible con
nuestro dev-32B, e ingeniería frágil). Se extraen dos ideas validadas
por su comunidad (34 reseñas positivas):

1. EXPERIMENTO S4 — Pulido global SDXL: pase de KSampler con checkpoint
   SDXL-DMD a denoise muy bajo (0.15-0.25) DESPUÉS del FaceDetailer,
   como etapa opcional apagable (patrón Ctrl+B). Objetivo: textura de
   piel y grano fotográfico que ataquen el acabado "irreal/editorial".
   Costo: ~6GB extra al bootstrap (checkpoint SDXL DMD). Riesgo a
   vigilar: deriva de identidad facial — por eso va DESPUÉS del
   detailer y a denoise mínimo. Condición: solo tras medir línea base
   del LoRA (S3), para saber qué aporta cada pieza.

2. DATO PARA EVALUACIÓN KLEIN (S3/S4): Klein 9B genera en 20-30 seg
   por imagen (reporte de comunidad), ~3-5x más rápido que dev-32B.
   Refuerza la arquitectura candidata de dos motores: dev-32B para
   calidad (anchors, campañas) + Klein para volumen (contenido diario),
   donde además vive el ecosistema maduro de LoRAs de atributo.

3. Recordatorio reforzado: la página exhibe licencia BFL no-comercial —
   la tarea S3 de verificar términos de uso comercial de outputs es
   bloqueante antes de monetizar.
