# Nystagmus: Accessibility Research Report

**Research Date:** December 2024
**Focus:** Involuntary eye movement, interface design, assistive technology

---

## Understanding Nystagmus

### Definition
> "Nystagmus is an involuntary oscillatory eye movement and is an important diagnostic marker for various neurological and vestibular disorders. It is a vision condition in which the eyes make repetitive, uncontrolled movements, which can prevent someone from forming a stable image."

### Types
- **Congenital/Infantile:** Present from birth
- **Acquired:** Develops later due to disease or injury
- **Vestibular:** Related to inner ear/balance system
- **Drug-induced:** Side effect of certain medications

### Impact on Vision
- Reduced visual acuity
- Difficulty maintaining stable gaze
- Problems with depth perception
- Reading difficulties
- Screen tracking challenges

## Digital Interface Challenges

### Eye Tracking Difficulties
> "Some users with severe eye movement restrictions or conditions such as nystagmus experienced difficulty in achieving reliable cursor control with eye-tracking systems."

### Ocular Parameter Research
> "Research on ocular parameters found that users with SSMI (Severe Speech and Motor Impairment) often suffer from nystagmus and strabismus, limiting the number of elements on a computer screen."

### Current AT Limitations
> "Only general Assistive Technology solutions like glasses, screen magnifiers, speech output, display adaptation and concept holders are available. More specific ATs to reduce the impact of nystagmus are missing."

## Innovative Solutions

### Digital Retinal Image Stabilization
> "Research is exploring ways to reduce the impact of nystagmus by stabilizing the image on the retina by moving the digital image synchronously with the unintended eye movement using gaze contingent display technology."

### Smart Headsets
> "An initial solution could be implemented for smart vision headsets such as Apple Vision Pro that include eye tracking, that can block the user's view entirely, and that can generate images spanning the user's vision in real time."

- [Medium Article](https://rethunk.medium.com/smart-headset-for-nystagmus-correction-e1974bf126d4)

### Adaptive Virtual Keyboards
> "Researchers have developed optimized eye gaze controlled virtual keyboards with adaptive dwell time features for users with SSMI."

Features:
- Reduced eye gaze movement distance
- Adaptive dwell time for selection
- Automatic layout optimization
- [SAGE Research](https://journals.sagepub.com/doi/abs/10.3233/TAD-200292)

### Smartphone Applications
Research is developing smartphone-based eye tracking for nystagmus analysis:
- ConVNG: Convolutional neural network-based nystagmography
- EyePhone: Smartphone eye tracking application
- [IEEE Xplore](https://ieeexplore.ieee.org/document/11253718/)
- [PMC - Smartphone video nystagmography](https://pmc.ncbi.nlm.nih.gov/articles/PMC10129923/)

## Interface Design Recommendations

### General Principles

1. **Large Target Areas**
   > "Allow as much space and size as possible when determining placements of actionable target elements such as buttons, banners, and text links."

2. **Reduced Complexity**
   > "Avoiding web designs that involve the need for complex movements or intricate thought processes will help users navigate with less frustration and eye fatigue."

3. **Stable Content**
   - Minimize moving or animated elements
   - Avoid auto-scrolling content
   - Provide pause controls for any motion

4. **High Contrast**
   - Strong contrast helps compensate for reduced acuity
   - Offer high contrast mode options

### Specific Accommodations

| Element | Recommendation |
|---------|----------------|
| Buttons | Minimum 44x44px, larger preferred |
| Text links | Generous padding, underlined |
| Navigation | Consistent, predictable locations |
| Forms | Large input fields, clear labels |
| Videos | User-controlled playback |
| Animations | Pausable, reducible, or disableable |

### Eye Tracking Alternatives

For users where eye tracking fails:
- Switch scanning interfaces
- Voice control
- Head tracking
- Single-switch input
- Keyboard navigation

## Current Assistive Technology

### Available Solutions
- Screen magnifiers (ZoomText, MAGic)
- Screen readers (JAWS, NVDA, VoiceOver)
- Speech-to-text software
- Voice control systems
- Head-mounted displays

### Gaps in Technology
> "More specific ATs to reduce the impact of nystagmus are missing."

Research needs:
- Real-time image stabilization systems
- Nystagmus-aware eye tracking calibration
- Adaptive interface systems
- Personalized movement prediction

## Research and Resources

### Key Papers

1. **Smartphone Eye Tracking for Nystagmus Analysis**
   - [IEEE Xplore](https://ieeexplore.ieee.org/document/11253718/)

2. **Smartphone Video Nystagmography Using CNN**
   - [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10129923/)

3. **Eye Gaze Controlled Adaptive Virtual Keyboard**
   - [SAGE](https://journals.sagepub.com/doi/abs/10.3233/TAD-200292)

4. **Real-time Eye Movement-based Computer Interface**
   - [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S2352648324000771)

5. **EyePhone Application**
   - [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10926800/)

### Organizations

- Nystagmus Network (UK)
- American Nystagmus Network
- RNIB (Royal National Institute of Blind People)

### WCAG Relevant Guidelines

- 2.2.2 Pause, Stop, Hide (animations)
- 2.3.3 Animation from Interactions (reduce motion)
- 2.5.5 Target Size (larger targets)
- 1.4.12 Text Spacing (readability)

## Future Directions

### Emerging Technologies

1. **AI-powered stabilization**
   - Predictive eye movement algorithms
   - Real-time compensation

2. **AR/VR headsets**
   - Apple Vision Pro potential
   - Meta Quest accessibility features

3. **Brain-computer interfaces**
   - Bypass eye movement entirely
   - Direct neural input

4. **Personalized interfaces**
   - Machine learning adaptation
   - User-specific calibration

---

*See also: [LOW_VISION_ACCESSIBILITY_RESEARCH.md](../low_vision/LOW_VISION_ACCESSIBILITY_RESEARCH.md)*
