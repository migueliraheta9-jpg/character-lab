# PROMPTS S3 — Construcción sistemática del dataset de identidad (Valeria)

**Workflow:** WF3 unificado · **Seed:** 794808565046336 FIJA en todas las corridas · **Resolución:** 1024×1024 · Referencias (Step 3): en bypass.

**Protocolo por carpeta:**
1. Modo taller (grupo detailer en Ctrl+B) → correr todos los prompts de la carpeta, uno por Ejecutar, editando prompt + prefijo BASE cada vez.
2. Curar visualmente las ganadoras.
3. Reactivar grupo detailer → re-ejecutar SOLO las ganadoras (misma seed = misma base + versión detail). Editar prefijo DETAIL en cada una.

**Regla de oro (lección A4):** todo prompt donde se vea el cuerpo lleva el candado corporal COMPLETO, jamás resumido.

---

## CARPETA 1 — expresiones
Prefijo BASE: `valeria/s3/expresiones/<etiqueta>` · Todas head-and-shoulders, estudio.

**1.1 risa_plena**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Editorial photograph, head-and-shoulders portrait, laughing fully with teeth showing, eyes squinted with genuine joy. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**1.2 sonrisa_suave**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Editorial photograph, head-and-shoulders portrait, gentle closed-lip smile, warm relaxed gaze at camera. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**1.3 seria_editorial**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Editorial photograph, head-and-shoulders portrait, serious composed expression, lips closed, direct intense gaze, fashion editorial mood. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**1.4 sorpresa**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Candid photograph, head-and-shoulders portrait, genuinely surprised expression, eyebrows raised, lips slightly parted, hand near her cheek. Neutral seamless light-gray studio background, soft even lighting, 85mm lens look.
```

**1.5 picara**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Editorial photograph, head-and-shoulders portrait, playful smirk with one eyebrow subtly raised, mischievous spontaneous energy. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**1.6 pensativa**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Editorial photograph, head-and-shoulders portrait, thoughtful expression looking slightly down and away, soft introspective mood, fingers lightly touching her chin. Neutral seamless light-gray studio background, soft directional lighting, 85mm lens look.
```

---

## CARPETA 2 — angulos
Prefijo BASE: `valeria/s3/angulos/<etiqueta>` · Rostro neutro-amable constante; solo cambia la cámara.

**2.1 tres_cuartos_izq**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Editorial photograph, head-and-shoulders portrait, face turned three-quarters to her left, eyes toward camera, subtle smile. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**2.2 tres_cuartos_der**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Editorial photograph, head-and-shoulders portrait, face turned three-quarters to her right, eyes toward camera, subtle smile. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**2.3 perfil_izq**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Editorial photograph, clean side profile facing left, relaxed neutral expression, hair falling naturally over her shoulder. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**2.4 perfil_der**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Editorial photograph, clean side profile facing right, relaxed neutral expression, hair tucked behind her ear showing the profile line. Neutral seamless light-gray studio background, soft even beauty lighting, 85mm lens look.
```

**2.5 picado_selfie**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Candid selfie-style photograph from a slightly high angle looking down at her, she looks up at the camera with a bright smile, arm extended holding the phone. Soft natural window light, casual authentic mood, phone camera aesthetic.
```

**2.6 contrapicado_leve**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Editorial photograph from a slightly low angle, chin subtly raised, confident calm expression looking past the camera. Neutral seamless light-gray studio background, soft directional lighting, 85mm lens look.
```

---

## CARPETA 3 — poses_cuerpo
Prefijo BASE: `valeria/s3/poses_cuerpo/<etiqueta>` · Candado corporal COMPLETO en todos. Outfit neutro constante para que el dato sea la pose.

**3.1 frontal_relajada**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow, upright confident posture. Full body editorial photograph, standing facing camera, weight on one hip, arms relaxed, wearing a fitted black tank top and black leggings, barefoot, subtle smile. Neutral seamless light-gray studio background, soft even lighting, 50mm lens look.
```

**3.2 espalda_mirada**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Full body editorial photograph from behind, she looks back over her right shoulder at the camera with a soft smile, wearing a fitted black tank top and black leggings, barefoot. Neutral seamless light-gray studio background, soft even lighting, 50mm lens look.
```

**3.3 sentada_banco**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Three-quarter body editorial photograph, sitting on a low wooden stool, leaning slightly forward with forearms on her knees, relaxed engaged expression, wearing a fitted black tank top and black leggings, barefoot. Neutral seamless light-gray studio background, soft even lighting, 50mm lens look.
```

**3.4 caminando**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Full body editorial photograph, walking toward camera mid-stride, natural arm swing, hair with slight motion, easy confident smile, wearing a fitted black tank top and black leggings, white sneakers. Neutral seamless light-gray studio background, soft even lighting, 50mm lens look.
```

**3.5 brazos_cruzados**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow, upright confident posture. Three-quarter body editorial photograph, arms crossed confidently, slight head tilt, assured warm expression, wearing a fitted black tank top and black leggings. Neutral seamless light-gray studio background, soft even lighting, 50mm lens look.
```

**3.6 estiramiento**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Full body editorial photograph, overhead stretch with both arms raised, gentle side bend, serene expression eyes softly closed, wearing a fitted black tank top and black leggings, barefoot. Neutral seamless light-gray studio background, soft even lighting, 50mm lens look.
```

---

## CARPETA 4 — gym
Prefijo BASE: `valeria/s3/gym/<etiqueta>` · Candado corporal completo. Estética teléfono, no editorial.

**4.1 rack_descanso**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid photograph, three-quarter body shot resting between sets near a dumbbell rack in a modern gym, hair in a high ponytail, matching sage-green sports bra and high-waisted leggings, natural confident smile, light sheen of sweat, soft window light mixed with gym lighting, shot on a phone camera, realistic.
```

**4.2 sentadilla**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid photograph, full body side view performing a barbell squat at a squat rack, focused expression, hair in a high ponytail, black sports bra and dark-gray high-waisted leggings, lifting shoes, chalk dust in the air, gym lighting, shot on a phone camera, realistic.
```

**4.3 mancuernas_banco**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid photograph, three-quarter body shot seated on a flat bench doing dumbbell shoulder presses, concentrated expression, hair in a braid, burgundy sports bra and black leggings, modern gym background softly blurred, shot on a phone camera, realistic.
```

**4.4 selfie_espejo**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid gym mirror selfie photograph, full body, holding her phone at chest height covering nothing of her face, playful smile, hair in a messy bun, matching lilac sports bra and leggings, gym equipment reflected behind, hard flash phone camera look, realistic.
```

**4.5 estiramiento_mat**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid photograph, full body seated hamstring stretch on a black yoga mat, reaching toward her toes, serene focused expression, hair in a low ponytail, white sports bra and sage-green leggings, bright airy gym studio with plants, natural morning light, shot on a phone camera, realistic.
```

**4.6 agua_toalla**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid photograph, half-body shot drinking from a water bottle with a towel over her shoulder after training, flushed cheeks and light sweat sheen, relaxed satisfied smile, black sports bra, gym background softly blurred, warm afternoon light, shot on a phone camera, realistic.
```

---

## CARPETA 5 — escenas
Prefijo BASE: `valeria/s3/escenas/<etiqueta>` · Lifestyle exterior. Candado corporal completo cuando el plano lo muestre.

**5.1 cafe** — el C3 validado, sin cambios
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Candid photograph, half-body shot sitting at an outdoor café table, holding an iced coffee, casual beige linen shirt slightly open over a white top, gold hoop earrings, warm afternoon light, blurred café background, relaxed genuine smile looking just off-camera, lifestyle influencer aesthetic, realistic.
```

**5.2 calle_miami** — el C2 corregido con canon completo
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid street-style photograph, full body walking on a sunny Miami street with pastel art-deco buildings behind, white crop top, light-wash denim shorts and white sneakers, sunglasses pushed up on her head, mid-stride natural laugh, bright daylight, travel influencer aesthetic, realistic.
```

**5.3 playa_paseo**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure built by regular strength training: defined narrow waist, softly muscular shoulders and toned arms, flat toned stomach, round firm glutes, strong athletic thighs and calves, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Candid photograph, full body walking along the shoreline at the beach, one-piece athletic swimsuit in deep teal, wet sand and gentle waves, hair moving in the breeze, laughing naturally looking to the side, golden late-afternoon sun, travel influencer aesthetic, realistic.
```

**5.4 brunch**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Candid photograph, half-body shot at a bright brunch restaurant, holding a fork over an avocado toast plate, mid-laugh looking at someone off-camera, flowy white summer blouse, delicate gold necklace, soft daylight through large windows, lifestyle influencer aesthetic, realistic.
```

**5.5 atardecer_malecon**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Candid photograph, half-body shot leaning on a seaside boardwalk railing at sunset, warm orange light on her face, hair gently wind-blown, casual knit top in cream, peaceful smile looking at the horizon then back to camera, soft long shadows, golden hour glow, realistic.
```

---

## CARPETA 6 — looks
Prefijo BASE: `valeria/s3/looks/<etiqueta>` · Medio cuerpo urbano/estudio; el dato es el vestuario y su versatilidad.

**6.1 casual_denim**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Half-body candid photograph, oversized light-blue denim jacket over a white tee, small gold hoops, relaxed street pose leaning on a concrete wall, easy smile, urban background softly blurred, natural daylight, realistic.
```

**6.2 vestido_negro**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure: defined narrow waist, softly muscular shoulders and toned arms, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow, upright confident posture. Three-quarter body editorial photograph, elegant fitted black midi dress, thin heels, subtle evening makeup, hair in loose waves over one shoulder, confident poised expression, warm interior restaurant lighting with bokeh, realistic.
```

**6.3 athleisure**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Half-body candid photograph, cropped white hoodie and high-waisted charcoal joggers, hair in a sleek low bun, holding a green smoothie, walking out of a juice bar, bright morning light, athleisure street style, shot on a phone camera, realistic.
```

**6.4 oficina_blazer**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, long dark brown hair with caramel balayage. Half-body photograph, tailored beige blazer over a white silk top, minimal gold jewelry, hair straightened sleek, composed professional smile, modern office lobby background softly blurred, soft daylight, realistic.
```

**6.5 verano_floral**
```
Young Latina woman, 25, exact same face in every image: dense freckles across the nose bridge and upper cheeks, small dark beauty mark above the left corner of her lip, almond-shaped light hazel eyes, softly arched thick eyebrows, full lips with a defined cupid's bow, shallow dimple on her right cheek when smiling, long dark brown hair with caramel balayage. Height around 168 cm, fit hourglass figure: defined narrow waist, toned arms, natural medium-full bust proportional to her frame, warm tan skin with an even healthy glow. Three-quarter body candid photograph, light floral summer sundress in warm tones, straw tote bag on her shoulder, walking through an outdoor market, genuine laugh, bright summer daylight, realistic.
```

---

## Registro de curaduría (rellenar en sesión)
| Carpeta | Corridas | Ganadoras (etiquetas) | Notas |
|---|---|---|---|
| expresiones | /6 | | |
| angulos | /6 | | |
| poses_cuerpo | /6 | | |
| gym | /6 | | |
| escenas | /5 | | |
| looks | /5 | | |

**Meta del pull:** ~34 corridas base → curar 15-22 ganadoras → re-correr con detailer → ese conjunto ES el dataset candidato del LoRA (balancear: mayoría detail + 4-5 bases crudas para textura natural).
