# Stereoblindness Primary Source Notes

This file captures the paper-by-paper extraction behind the repo's current
depth-accessibility guidance.

## Source Set

- [Source cache index](/home/eirikr/Github/openperception/docs/external_sources/stereoblindness_depth_sources.md)
- [Provenance manifest](/home/eirikr/Github/openperception/papers/downloads/stereoblindness/PROVENANCE.json)
- [Harmonized depth guide](/home/eirikr/Github/openperception/docs/harmonized-depth-accommodation-guide.md)

## 1. Chopin, Bavelier, Levi (2019)

Citation:
`The prevalence and diagnosis of 'stereoblindness' in adults less than 60 years of age: a best evidence synthesis.`

Local artifact:
`papers/downloads/stereoblindness/Chopin_Bavelier_Levi_2019_Stereoblindness_Best_Evidence_Synthesis.pubmed.txt`

Granular findings:

- The review frames stereoblindness prevalence as measurement-sensitive rather
  than inherently rare.
- Four prevalence approaches converged on the same median estimate: 7% in
  adults younger than 60.
- The paper explicitly warns that older adults may have higher prevalence.
- The authors recommend an ecological definition of stereoblindness and more
  efficient clinical methods built from adapted existing tools.

Project distillation:

- OpenPerception should treat stereoblindness as a first-class design
  population, not as an edge case.
- Repo claims should avoid broad "5-10%" language when the cited source more
  specifically supports an approximately 7% median estimate for adults under 60.
- Testing language should acknowledge that prevalence depends on how stereopsis
  is measured.

## 2. Yang, Saunders, And Chen (2022)

Citation:
`The experience of stereoblindness does not improve use of texture for slant perception.`

Local artifacts:

- `papers/downloads/stereoblindness/Wang_Saunders_2022_Texture_Slant_Stereoblindness.html`
- `papers/downloads/stereoblindness/Wang_Saunders_2022_Texture_Slant_Stereoblindness.txt`

Granular findings:

- The study compares 24 stereoblind and 24 stereo-normal participants on slant
  discrimination and slant estimation tasks.
- The groups showed comparable ability to discriminate slant from texture
  information under monocular conditions.
- The groups also showed similar mapping from texture information to perceived
  slant, including the same frontal-bias pattern at low slants.
- Stereoblind participants still benefited from binocular viewing in slant
  estimation, even though they could not use binocular disparity in the usual
  way.
- The paper argues against assuming that long-term stereoblindness automatically
  creates superior texture-cue sensitivity.
- The discussion notes that stereoblind people can combine multiple monocular
  cues in natural settings, including motion parallax and contour information.

Project distillation:

- Static monocular cues are not merely "backup" decoration; they can carry real
  task meaning for users without stereopsis.
- We should not frame stereoblind users as needing exaggerated or caricatured
  texture cues. Well-authored texture, perspective, occlusion, and edge cues
  may already be effective.
- Stereo-off paths should still preserve credible slant, ordering, and surface
  interpretation when multiple monocular cues are present.

## 3. Kim, Angelaki, And DeAngelis (2016)

Citation:
`The neural basis of depth perception from motion parallax.`

Local artifacts:

- `papers/downloads/stereoblindness/Nadler_et_al_2016_Motion_Parallax_Depth_Review.html`
- `papers/downloads/stereoblindness/Nadler_et_al_2016_Motion_Parallax_Depth_Review.txt`

Authorship note:

- The local cache still uses a legacy `Nadler_et_al_2016_*` filename, but the
  cached full text identifies the source paper authors as HyunGoo R Kim, Dora
  E Angelaki, and Gregory C DeAngelis.

Granular findings:

- The review describes motion parallax as a powerful cue to three-dimensional
  scene structure during observer translation.
- It distinguishes pictorial/static cues from motion-based cues: static cues are
  valuable, but motion parallax adds quantitative depth information.
- The paper treats motion parallax as sufficient for depth perception when
  properly isolated and disambiguated.
- Perceived depth sign from motion parallax depends on extra-retinal information
  related to eye movements; movement is not optional to this cue.
- The review repeatedly discusses integration between motion parallax and
  binocular disparity rather than a winner-take-all model.

Project distillation:

- Motion parallax is strong enough to reinforce depth, but because it depends on
  movement it cannot be the only path to essential meaning.
- Reduced-motion modes must keep the same spatial interpretation available
  through static cues.
- Depth authoring should assume cue layering, not cue substitution.

## 4. Pladere Et Al. (2022)

Citation:
`Inclusivity in stereoscopic XR: Human vision first.`

Local artifacts:

- `papers/downloads/stereoblindness/Pladere_et_al_2022_Inclusivity_in_Stereoscopic_XR.pdf`
- `papers/downloads/stereoblindness/Pladere_et_al_2022_Inclusivity_in_Stereoscopic_XR.html`
- `papers/downloads/stereoblindness/Pladere_et_al_2022_Inclusivity_in_Stereoscopic_XR.txt`

Granular findings:

- The paper argues that full XR accessibility currently assumes well-functioning
  eyes and binocular vision more often than the XR literature admits.
- It states that more than 30% of the population may have moderate to poor
  stereo vision or related eye and vision problems that can limit XR access.
- The authors criticize common XR study practice for relying on self-report
  vision status and under-reporting participant visual abilities.
- They recommend adaptive hardware and software, including proper refractive
  correction, adjustable inter-pupillary distance, and digital content that can
  be tuned to individual visual needs.
- For users with no or anomalous stereo vision, the paper explicitly suggests
  increasing the saliency of monocular depth cues or switching to a synthesized
  two-dimensional mode.
- The paper also points to sonification as an example of an adaptive
  non-visual supplement when a visual channel does not carry enough information.

Project distillation:

- The repo's `depth_cues={all, monocular_only}` dial is directly supported by
  the paper's adaptation recommendations.
- A harmonized depth system should preserve one authored scene while allowing
  users to increase monocular cue saliency or drop to a 2D interpretation path.
- Non-visual reinforcement is justified for critical spatial meaning, not only
  as an accessibility afterthought.

## Cross-Source Synthesis

Across the source set, the stable design rules are:

1. Stereo is beneficial but not a safe assumption.
2. Static monocular cues must carry essential spatial meaning.
3. Motion parallax is a reinforcement channel, not a mandatory recovery path.
4. Adjustable presentation modes are better than one fixed depth presentation.
5. Source-backed depth accommodations should be described in task terms:
   reachability, ordering, collision risk, target identity, and scene
   navigation.

## Repo Changes Supported By These Notes

- [Depth evidence matrix updates](/home/eirikr/Github/openperception/specs/EVIDENCE_MATRIX.md)
- [UVAS depth-axis updates](/home/eirikr/Github/openperception/specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md)
- [Depth validator wording](/home/eirikr/Github/openperception/specs/VALIDATORS_FRAMEWORK.md)
