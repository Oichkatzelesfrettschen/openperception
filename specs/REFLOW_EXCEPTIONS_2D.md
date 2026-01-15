# Reflow Exceptions for 2D Content

**Version:** 1.0.0
**Purpose:** Formalize exceptions to reflow requirements for content that inherently requires two-dimensional layout
**Standards:** WCAG 2.2 Success Criterion 1.4.10 (Reflow)
**Companion to:** SCALING_MATHEMATICS.md, LAYOUT_SYSTEM.md

---

## 1. The Exception

### 1.1 WCAG 1.4.10 Reflow

WCAG 2.2 SC 1.4.10 requires that content can be presented without loss of information or functionality, and without requiring scrolling in two dimensions, for:

- Vertical scrolling content at a width equivalent to 320 CSS pixels
- Horizontal scrolling content at a height equivalent to 256 CSS pixels

### 1.2 The Exception Clause

> "Except for parts of the content which require two-dimensional layout for usage or meaning."

**Examples explicitly listed by WCAG:**
- Images
- Maps
- Diagrams
- Video
- Games
- Presentations
- Data tables
- Interfaces where toolbars must remain visible while manipulating content

### 1.3 What This Means for UVAS+

Two-dimensional content is **exempt** from single-axis reflow requirements. However:

1. The exception applies **only to that specific content region**
2. Surrounding UI (chrome, controls, navigation) must still reflow
3. The 2D content itself must remain accessible via alternative means

---

## 2. Content Categories

### 2.1 Inherently 2D Content

| Category | Examples | Reason for Exception |
|----------|----------|----------------------|
| **Spatial visualization** | Maps, floor plans, circuit diagrams | Spatial relationships are meaning |
| **Data relationships** | Tables, matrices, spreadsheets | Row/column intersection is meaning |
| **Visual media** | Images, videos, art | Composition is fixed |
| **Interactive 2D** | Games, drawing apps, CAD | 2D interaction is core function |
| **Time + space** | Gantt charts, timelines | Dual-axis layout encodes meaning |

### 2.2 NOT Inherently 2D Content

| Content Type | Why NOT Exempt | Required Behavior |
|--------------|----------------|-------------------|
| Multi-column text | Layout convenience, not meaning | Collapse to single column |
| Side-by-side images | Could be stacked vertically | Stack on narrow viewports |
| Horizontal navigation | Convenience, not necessity | Convert to hamburger/dropdown |
| Form fields in rows | Layout preference | Stack vertically |

### 2.3 Decision Algorithm

```python
def is_2d_exempt(content: Content) -> bool:
    """
    Determine if content qualifies for 2D reflow exception.
    """
    # Check explicit 2D semantic meaning
    if content.type in ["game", "map", "diagram", "video", "image"]:
        return True

    # Check data table with meaningful intersections
    if content.type == "table":
        return content.has_column_headers and content.has_row_headers

    # Check toolbar-dependent content
    if content.requires_persistent_toolbar_visibility:
        return True

    # Check spatial interaction
    if content.interaction_mode == "2d_spatial":
        return True

    # Default: not exempt
    return False
```

---

## 3. Required Affordances

### 3.1 When Content Is Exempt

Even when content qualifies for the 2D exception, UVAS+ requires:

| Affordance | Requirement | Rationale |
|------------|-------------|-----------|
| **Pan/scroll** | Must be possible within the 2D region | Access all content |
| **Zoom** | Must support zoom in/out | See detail and overview |
| **Reset view** | Must provide "fit to view" or "reset" | Recover from zoom |
| **Alternative access** | Consider text description for key info | Screen reader users |
| **No control overlap** | UI controls never overlap each other | Usability |
| **Controls reachable** | All controls accessible without horizontal scroll | Accessibility |

### 3.2 Implementation Pattern

```yaml
2d_exempt_region:
  structure:
    - container: scrollable_2d_viewport
      role: "region"
      aria-label: "Interactive game area"
      scroll: [horizontal, vertical]
      zoom:
        min: 0.5
        max: 4.0
        default: 1.0
      controls:
        - zoom_in: "accessible button"
        - zoom_out: "accessible button"
        - reset_view: "accessible button"
        - toggle_fullscreen: "optional"

  constraints:
    - controls_position: "outside 2D region OR overlay with contrast"
    - controls_reflow: true  # Controls MUST reflow
    - content_reflow: false  # 2D content exempt
```

### 3.3 Visual Example

```
+------------------------------------------+
| [Chrome / Navigation Bar]         [Menu] |  <- MUST reflow
+------------------------------------------+
| [Toolbar: Brush | Eraser | Color | ...]  |  <- MUST reflow
+------------------------------------------+
|                                          |
|    +-----------------------------+       |
|    |                             |       |
|    |    2D CANVAS / GAME         |       |  <- EXEMPT
|    |    (scrollable, zoomable)   |       |
|    |                             |       |
|    +-----------------------------+       |
|                                          |
|  [Zoom: [-] [100%] [+]]  [Reset]         |  <- MUST reflow
+------------------------------------------+
```

---

## 4. Games and Interactive 2D Applications

### 4.1 Game UI Structure

```yaml
game_accessibility_structure:
  # 2D exempt regions
  exempt_content:
    - game_world: "The playable 2D space"
    - minimap: "Optional spatial overview"
    - hud_fixed_elements: "Health bars, ammo counts at fixed positions"

  # Non-exempt UI (MUST reflow)
  accessible_ui:
    - main_menu: "Reflows to screen width"
    - pause_menu: "Reflows to screen width"
    - settings: "Reflows to screen width"
    - dialogue_boxes: "Text reflows, positioned accessibly"
    - inventory: "May use grid but controls reflow"
    - tutorials: "Text and controls reflow"
```

### 4.2 Game-Specific Affordances

```python
class GameAccessibilityConfig:
    """
    Required accessibility features for 2D game UI.
    """

    # Camera/view controls
    camera_controls = {
        "zoom_in": KeyBinding(default="=", rebindable=True),
        "zoom_out": KeyBinding(default="-", rebindable=True),
        "reset_view": KeyBinding(default="0", rebindable=True),
        "pan": MouseDrag(button="middle", or_keys=["shift+drag"]),
    }

    # HUD positioning
    hud_config = {
        "scale_with_ui": True,  # HUD scales with UI scale
        "position_mode": "anchored",  # Corner anchors, not absolute
        "repositionable": True,  # Player can move HUD elements
        "hideable": True,  # Player can hide HUD for screenshots
    }

    # Alternative information access
    alternative_access = {
        "screen_reader_mode": "Announce game events",
        "spatial_audio": "Audio cues for spatial information",
        "high_contrast_mode": "Simplified visuals",
    }
```

### 4.3 Touch Target Preservation in Games

Even in 2D game regions, touch targets must meet minimums:

```python
def validate_game_touch_targets(game_ui: GameUI, s_eff: float):
    """
    Validate touch targets in game UI, accounting for 2D exception.
    """
    violations = []

    for element in game_ui.interactive_elements:
        size_px = measure_element(element, s_eff)
        min_size = 44 * s_eff  # 44lp minimum

        if element.in_hud or element.in_overlay:
            # HUD elements MUST meet touch target minimum
            if min(size_px.width, size_px.height) < min_size:
                violations.append(HUDTouchTargetViolation(element))

        elif element.is_game_world_control:
            # In-world controls: advisory, not blocking
            if min(size_px.width, size_px.height) < min_size:
                log_advisory(f"In-world control {element} is small")

    return violations
```

---

## 5. Data Tables

### 5.1 When Tables Are Exempt

Tables are exempt when they encode meaning in both dimensions:

```python
def table_is_2d_exempt(table: Table) -> bool:
    """
    Determine if a table requires 2D layout for meaning.
    """
    # Has both row and column headers
    if table.has_row_headers and table.has_column_headers:
        return True

    # Matrix-style data where position matters
    if table.cell_relationship == "intersection_meaning":
        return True

    # Calendar grids, timetables
    if table.semantic_role in ["calendar", "schedule", "grid"]:
        return True

    # Simple key-value list
    if table.structure == "name_value_pairs":
        return False  # NOT exempt; can stack vertically

    return False
```

### 5.2 Table Accessibility Even When Exempt

```yaml
exempt_table_requirements:
  structure:
    - Use semantic <table> markup (not divs)
    - Include <caption> describing the table
    - Use <th> with scope="col" and scope="row"
    - Use <thead>, <tbody> for structure

  scrolling:
    - Table in own scrollable container
    - Page around table reflows normally
    - Sticky headers for large tables

  alternative:
    - Provide summary for complex tables
    - Consider "card view" toggle for mobile
    - Screen reader should announce row/column headers
```

### 5.3 Responsive Table Pattern

```html
<!-- Table in scrollable container -->
<div class="table-container" style="overflow-x: auto;">
  <table>
    <caption>Q4 Sales by Region (scrollable)</caption>
    <thead>
      <tr>
        <th scope="col">Region</th>
        <th scope="col">Oct</th>
        <th scope="col">Nov</th>
        <th scope="col">Dec</th>
        <th scope="col">Total</th>
      </tr>
    </thead>
    <tbody>
      <!-- Data rows -->
    </tbody>
  </table>
</div>

<!-- Surrounding content reflows normally -->
<p>Analysis: The North region showed strongest growth...</p>
```

---

## 6. Maps and Diagrams

### 6.1 Map Accessibility Requirements

```yaml
map_requirements:
  core_exemption:
    - Map content scrolls/pans in 2D
    - Zoom supported (min 0.5x to 4x)
    - Geographic relationships preserved

  accessibility_layer:
    - Search: "Find location by text input"
    - Directions: "Text-based navigation instructions"
    - Landmarks: "List view of nearby points of interest"
    - Current location: "Text announcement of position"
    - Scale indicator: "Visual and accessible"

  controls:
    - Zoom buttons: "Reflow with UI, meet touch targets"
    - Search box: "Reflows with UI"
    - Layer toggles: "Reflow with UI"
    - Legend: "Collapsible, accessible"
```

### 6.2 Diagram Accessibility

```python
class AccessibleDiagram:
    """
    Pattern for accessible 2D diagrams.
    """

    def __init__(self, svg_content: str, alt_text: str):
        self.svg = svg_content
        self.alt_text = alt_text
        self.long_description = None  # Optional detailed description
        self.data_table = None  # Optional tabular alternative

    def render(self) -> str:
        return f'''
        <figure role="img" aria-label="{self.alt_text}">
            <div class="diagram-container" style="overflow: auto;">
                {self.svg}
            </div>
            <figcaption>
                {self.alt_text}
                {self._render_long_description()}
            </figcaption>
        </figure>
        '''

    def _render_long_description(self) -> str:
        if self.long_description:
            return f'''
            <details>
                <summary>Detailed description</summary>
                <p>{self.long_description}</p>
            </details>
            '''
        return ""
```

---

## 7. Invariants and Constraints

### 7.1 Reflow Exception Invariants

```yaml
INV-RE01:
  rule: "2D exemption applies only to the specific 2D content region"
  severity: BLOCKING
  example: "Game world is exempt, but game menus must reflow"

INV-RE02:
  rule: "Controls for 2D content must be accessible without horizontal scroll"
  severity: BLOCKING
  example: "Zoom buttons can be reached without scrolling right"

INV-RE03:
  rule: "2D exempt regions must support zoom and pan"
  severity: WARNING
  example: "User can zoom in/out and scroll within the 2D area"

INV-RE04:
  rule: "No UI control overlap at any scale"
  severity: BLOCKING
  example: "Buttons don't stack on top of each other at 400% zoom"

INV-RE05:
  rule: "Alternative access method for critical 2D information"
  severity: ADVISORY
  example: "Map provides text-based location search"
```

### 7.2 Exception Scope Constraint

```python
def validate_exception_scope(page: Page) -> list[Violation]:
    """
    Ensure 2D exception doesn't leak to non-exempt content.
    """
    violations = []

    for region in page.regions:
        if region.is_2d_exempt:
            # Check that exemption is scoped
            if region.parent and region.parent.is_2d_exempt:
                # OK: nested within another exempt region
                continue

            # Check sibling content
            for sibling in region.siblings:
                if sibling.has_horizontal_scroll and not sibling.is_2d_exempt:
                    violations.append(ExceptionScopeLeakViolation(
                        exempt_region=region,
                        affected_sibling=sibling
                    ))

    return violations
```

---

## 8. Validator Integration

### 8.1 REFLOW_EXCEPTION Gate

```yaml
reflow_exception_gate:
  id: GATE-RE01
  severity: WARNING
  checks:
    - name: valid_exemption
      rule: "Only inherently 2D content marked as exempt"
      validation: is_2d_exempt()

    - name: scoped_exemption
      rule: "Exemption doesn't affect surrounding content"
      validation: validate_exception_scope()

    - name: controls_accessible
      rule: "Controls reflow even if content is exempt"
      severity_override: BLOCKING

    - name: zoom_available
      rule: "2D content supports zoom in/out"

    - name: pan_available
      rule: "2D content supports pan/scroll"

    - name: alternative_access
      rule: "Text alternative for key information"
      severity: ADVISORY
```

### 8.2 Test Cases

```python
def test_game_ui_reflow_exception():
    """
    Verify game correctly applies 2D exception.
    """
    game = load_game_ui()

    # Game world is exempt
    assert is_2d_exempt(game.game_world)

    # Main menu reflows
    simulate_viewport(320, 800)
    assert not has_horizontal_scroll(game.main_menu)

    # Pause menu reflows
    assert not has_horizontal_scroll(game.pause_menu)

    # Settings reflow
    assert not has_horizontal_scroll(game.settings_screen)

    # Controls are reachable
    for control in game.game_world.controls:
        assert is_reachable_without_horizontal_scroll(control)

def test_table_exception_scoping():
    """
    Verify table exemption doesn't leak.
    """
    page = load_page_with_table()

    # Table is in scrollable container
    table_container = page.find("table-container")
    assert table_container.overflow_x == "auto"

    # Content around table reflows
    simulate_viewport(320, 800)
    for sibling in table_container.siblings:
        assert not has_horizontal_scroll(sibling)
```

---

## 9. Quick Reference

### 9.1 Is My Content 2D Exempt?

```
[ ] Maps, floor plans, geographic data       -> YES
[ ] Games with 2D spatial interaction        -> YES
[ ] Data tables with row AND column headers  -> YES
[ ] Charts where position encodes meaning    -> YES
[ ] Images, videos, visual art               -> YES
[ ] CAD, drawing, diagramming apps           -> YES

[ ] Multi-column article text                -> NO
[ ] Horizontal navigation menu               -> NO
[ ] Side-by-side comparison                  -> MAYBE (if comparison requires)
[ ] Form with fields in rows                 -> NO
```

### 9.2 If Content Is Exempt, Require:

```
[x] Scrollable container (own scroll, not page)
[x] Zoom controls (in, out, reset)
[x] Pan/drag support
[x] Controls outside or overlaid with contrast
[x] Controls themselves reflow
[x] Touch targets meet 44lp minimum for controls
[x] Alternative text/description for key info
```

### 9.3 Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Marking entire page as 2D exempt | Exemption too broad | Scope to specific region |
| Controls inside scroll area | May scroll off-screen | Place controls outside |
| No zoom support | User can't see detail | Add zoom controls |
| Game menus don't reflow | Only game world is exempt | Separate game UI from world |
| Horizontal page scroll for table | Should be table scroll only | Put table in container |

---

*Reflow Exceptions for 2D Content Version 1.0.0 - Created 2025-12-27*

## References

- [W3C - Understanding SC 1.4.10: Reflow](https://www.w3.org/WAI/WCAG21/Understanding/reflow.html)
- [Deque University - 1.4.10 Reflow (AA)](https://dequeuniversity.com/resources/wcag2.1/1.4.10-reflow)
- [WCAG 2.2 Specification](https://www.w3.org/TR/WCAG22/)
