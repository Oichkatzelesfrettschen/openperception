# Harmonized Depth Accommodation Guide

This guide translates stereoblindness and depth-perception research into a
single design pattern for OpenPerception: preserve richness for stereo-capable
users, but make essential spatial meaning readable without stereopsis.

## Goal

Build one depth system, not two separate experiences.

- Stereo can add richness.
- Essential depth information cannot depend on stereo alone.
- Motion-based depth can help, but it cannot be the only fallback because it
  intersects with vestibular and reduced-motion needs.

## Language

Use terms like `stereo-capable users`, `users with reduced stereopsis`, or
`users without stereopsis`. Avoid calling one group "normal." The design target
is shared comprehension across different depth channels.

## Distilled Research

1. Stereoblindness is common enough to design for explicitly. A 2019 best
   evidence synthesis found four approaches that converged on a median
   prevalence of about 7% in adults under 60.
2. A single eye can still support rich depth judgments through occlusion,
   relative size, texture gradients, perspective, shading, and motion
   parallax.
3. In a 2022 slant-perception study, stereoblind participants and stereo-normal
   participants showed comparable sensitivity to texture-based slant cues, and
   stereoblind participants still benefited from binocular viewing through
   non-stereopsis information.
4. Motion parallax is a powerful and sufficient depth cue, but it depends on
   movement. Because movement can also provoke discomfort, depth meaning cannot
   be recoverable only through parallax or camera motion.
5. XR systems can exclude a large share of people if they assume well-functioning
   binocular vision. A 2022 XR perspective estimated that ignoring common eye
   and vision problems could exclude at least 30% of the population from
   stereoscopic XR use.
6. Critical spatial information is more robust when depth is reinforced through
   another sensory channel such as spatial audio, haptics, or explicit text.

## Harmonized Depth Pattern

### 1. Make static monocular cues carry the task

If the player must know which object is nearer, in front, reachable, blocked,
targeted, or dangerous, encode that state through static cues first:

- occlusion and clear layer ordering
- relative size and scale gradients
- outlines, edge contrast, and contact shadows
- perspective and ground-plane anchoring
- texture density or atmospheric fade for distance

Static cues are the floor because they remain available when stereo is absent
and when motion is reduced.

### 2. Treat stereo as enrichment, not as entitlement

Binocular disparity can make scenes feel richer, more comfortable, or faster to
parse for some users. Keep that benefit. But if disabling stereo breaks the
ability to locate a hazard, read spacing, judge reachability, or navigate a
scene, the design is not yet harmonized.

### 3. Use motion parallax as reinforcement only

Parallax, camera sway, head-tracked motion, and kinetic depth effects can
strengthen depth perception, but they must layer on top of static cues.

- `motion_intensity=full`: parallax may reinforce depth
- `motion_intensity=reduced`: spatial meaning must remain intact
- `motion_intensity=none`: essential depth still readable through static cues

If turning motion off collapses scene meaning, the scene is underspecified.

### 4. Add nonvisual backup for critical spatial state

When failure to perceive depth has gameplay or comprehension cost, add another
channel:

- spatial audio for direction and distance
- haptic ramps or pulses for approach, impact, or proximity
- labels, captions, callouts, or narrated prompts for essential targets

This helps not only users without stereopsis, but also blind and low-vision
users, users in noisy environments, and users who miss one channel in context.

### 5. Expose depth as a bounded dial

The repo's depth settings should support a simple model:

- `depth_cues=all`: stereo plus monocular plus multisensory reinforcement
- `depth_cues=monocular_only`: no stereo dependency, no motion-only dependency

This keeps one authored scene while allowing users to select the channel mix
that matches their vision and comfort.

### 6. Test the degraded path on purpose

Review scenes and mechanics under these conditions:

1. stereo disabled
2. motion reduced or off
3. low contrast or clutter stress checks where depth edges are harder to read
4. audio off, then audio on

If the same task stays completable and the same priority ordering remains clear,
the depth effect is harmonized rather than exclusive.

## Definition of Done

A depth-critical feature is ready when all of the following are true:

- Essential near/far/in-front/behind meaning is readable from static monocular
  cues.
- Stereo improves richness but is not required for completion.
- Motion parallax is additive, not mandatory.
- Reduced-motion mode preserves the same spatial meaning.
- Critical spatial events have an additional nonvisual backup when consequences
  are meaningful.
- Testing includes people who do and do not rely on stereopsis.

## Repository Mapping

- [UVAS depth axis](/home/eirikr/Github/openperception/specs/UNIFIED_VISUAL_ACCESSIBILITY_SPEC.md)
- [Evidence matrix depth claims](/home/eirikr/Github/openperception/specs/EVIDENCE_MATRIX.md)
- [Validator framework depth gate](/home/eirikr/Github/openperception/specs/VALIDATORS_FRAMEWORK.md)
- [Primary source notes](/home/eirikr/Github/openperception/research/visual_impairments/stereoblindness/primary_source_notes.md)
- [Source cache index](/home/eirikr/Github/openperception/docs/external_sources/stereoblindness_depth_sources.md)
- [Deep research report](/home/eirikr/Github/openperception/research/visual_impairments/stereoblindness/stereoblindness_research_report.md)

## Sources

- Chopin A, Bavelier D, Levi DM. "The prevalence and diagnosis of
  'stereoblindness' in adults less than 60 years of age: a best evidence
  synthesis." Ophthalmic Physiol Opt. 2019.
  https://pubmed.ncbi.nlm.nih.gov/30776852/
- Yang P, Saunders JA, Chen Z. "The experience of stereoblindness does not improve use
  of texture for slant perception." J Vis. 2022.
  https://pmc.ncbi.nlm.nih.gov/articles/PMC9012895/
- Kim HR, Angelaki DE, DeAngelis GC. Review: "The neural basis of
  depth perception from motion parallax." Philos Trans R Soc Lond B Biol Sci.
  2016. https://pmc.ncbi.nlm.nih.gov/articles/PMC4901450/
- Pladere T, Svarverud E, Krumina G, Gilson SJ, Baraas RC. "Inclusivity in
  stereoscopic XR: Human vision first." Front Virtual Real. 2022.
  https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2022.1006021/full
- Microsoft Learn. "Xbox Accessibility Guideline 103: Additional channels for
  visual and audio cues." Updated March 4, 2026.
  https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/103
- Microsoft Learn. "Xbox Accessibility Guideline 117: Visual distractions and
  motion settings." Updated March 4, 2026.
  https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/117
