# DPI Transition Contract

**Version:** 1.0.0
**Purpose:** Define behavior when effective scale (S_eff) changes due to monitor transitions or user scaling
**Companion to:** SCALING_MATHEMATICS.md, QUANTIZATION_POLICY.md

---

## 1. The Problem

### 1.1 What Triggers a DPI Transition

| Trigger | Example | Notification |
|---------|---------|--------------|
| Window drag between monitors | 96 DPI -> 144 DPI | WM_DPICHANGED (Win), backingScaleFactorChanged (macOS) |
| Display configuration change | User enables scaling | Settings daemon, Wayland output events |
| User zoom change | Ctrl+/- in application | Application-level event |
| Hot-plug external display | Laptop dock/undock | Display change notification |
| SDR to HDR transition | HDR content in HDR-capable window | Compositor notification |

### 1.2 What Must Happen

When S_eff changes, the application must:

1. **Recompute** all token -> pixel conversions
2. **Reflow** layout without clipping or overlap
3. **Re-rasterize** scale-dependent assets (icons, images)
4. **Preserve** interaction state (focus, selection, scroll position)
5. **Maintain** reading order and focus order

### 1.3 What Must NOT Happen

| Failure Mode | Description | Severity |
|--------------|-------------|----------|
| Clipping | Content cut off by container | BLOCKING |
| Overlap | Interactive elements overlap | BLOCKING |
| Focus loss | Active element loses focus | WARNING |
| Scroll jump | Scroll position not preserved proportionally | WARNING |
| Blur | Wrong resolution assets displayed | ADVISORY |
| Flash | Visible flash during re-render | ADVISORY |

---

## 2. Platform Notification Mechanisms

### 2.1 Windows

```cpp
// Per-Monitor DPI Awareness v2 (Windows 10 1703+)
// Application must declare in manifest:
// <dpiAwareness>PerMonitorV2</dpiAwareness>

case WM_DPICHANGED:
{
    // wParam: new DPI (LOWORD = X DPI, HIWORD = Y DPI)
    UINT newDpi = HIWORD(wParam);

    // lParam: suggested new window rect
    RECT* prcNewWindow = (RECT*)lParam;

    // MUST resize window to suggested rect
    SetWindowPos(hwnd, NULL,
        prcNewWindow->left, prcNewWindow->top,
        prcNewWindow->right - prcNewWindow->left,
        prcNewWindow->bottom - prcNewWindow->top,
        SWP_NOZORDER | SWP_NOACTIVATE);

    // Then reflow internal layout at new DPI
    OnDpiChanged(newDpi);
    break;
}

// Child windows also receive notification (PMv2 feature)
case WM_DPICHANGED_AFTERPARENT:
    // Update child-specific DPI-dependent resources
    break;
```

**Source:** [Microsoft Learn - High DPI Desktop Application Development](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows)

### 2.2 macOS

```objc
// NSWindow automatically tracks backingScaleFactor
// Override to receive notifications:

- (void)windowDidChangeBackingProperties:(NSNotification *)notification {
    NSNumber *oldScale = [[notification userInfo]
        objectForKey:NSBackingPropertyOldScaleFactorKey];
    CGFloat newScale = [[self window] backingScaleFactor];

    if (oldScale && [oldScale floatValue] != newScale) {
        [self onScaleFactorChanged:newScale];
    }
}

// For layer-backed views:
- (BOOL)layer:(CALayer *)layer
    shouldInheritContentsScale:(CGFloat)newScale
    fromWindow:(NSWindow *)window {
    return YES;  // Inherit scale automatically
}
```

**Source:** [Apple Developer - backingScaleFactor](https://developer.apple.com/documentation/appkit/nswindow/1419459-backingscalefactor)

### 2.3 GTK 4

```c
// GTK 4 handles scaling internally, but apps can observe changes

static void on_scale_factor_changed(GtkWidget *widget, GParamSpec *pspec,
                                     gpointer user_data) {
    int scale = gtk_widget_get_scale_factor(widget);
    // For fractional: use gdk_surface_get_scale()
    g_print("Scale factor changed to %d\n", scale);
    // Trigger layout update
}

g_signal_connect(window, "notify::scale-factor",
                 G_CALLBACK(on_scale_factor_changed), NULL);
```

**Note:** GTK 4.14+ supports fractional scaling via wp_fractional_scale_manager_v1 on Wayland.

**Source:** [GTK 4 Widget scale-factor](https://docs.gtk.org/gtk4/property.Widget.scale-factor.html)

### 2.4 Qt 6

```cpp
// Qt 6 automatically handles DPI changes
// Override for custom handling:

void MyWidget::changeEvent(QEvent *event) {
    if (event->type() == QEvent::DevicePixelRatioChange) {
        qreal dpr = devicePixelRatio();
        // Reload @2x/@3x assets if needed
        reloadImages();
        // Update layout
        updateLayout();
    }
    QWidget::changeEvent(event);
}

// Alternative: connect to QScreen signals
connect(screen(), &QScreen::physicalDotsPerInchChanged,
        this, &MyWidget::onDpiChanged);
```

**Important:** The effective DPR can be a product of native DPR and QT_SCALE_FACTOR. Avoid double-scaling.

**Source:** [Qt 6 High DPI](https://doc.qt.io/qt-6/highdpi.html)

### 2.5 FLTK 1.4+

```cpp
// FLTK 1.4 provides per-screen scale factors
// Get current scale for a window:

float scale = Fl::screen_scale(Fl::screen_num(x(), y(), w(), h()));

// Set scale programmatically:
Fl::screen_scale(screen_num, new_scale);

// Environment override:
// FLTK_SCALING_FACTOR=1.5 ./myapp

// User can change at runtime with Ctrl+/Ctrl-/Ctrl0
```

**Source:** [FLTK Screen Functions](https://www.fltk.org/doc-1.4/group__fl__screen.html)

### 2.6 Wayland (Generic)

```c
// Listen for wl_output.scale or fractional_scale_v1

static void output_scale(void *data, struct wl_output *output,
                         int32_t scale) {
    struct my_surface *surface = data;
    surface->scale = scale;
    surface->needs_redraw = true;
}

// For fractional scaling (Wayland 1.22+):
static void fractional_scale_preferred(void *data,
    struct wp_fractional_scale_v1 *fractional_scale,
    uint32_t scale) {
    // scale is in units of 1/120, so 120 = 1.0, 150 = 1.25
    struct my_surface *surface = data;
    surface->scale = scale / 120.0;
}
```

---

## 3. State Preservation Requirements

### 3.1 What Must Be Preserved

| State | Preservation Method | Example |
|-------|---------------------|---------|
| Focus | Re-apply after layout | Focused button stays focused |
| Selection | Maintain model state | Selected list items unchanged |
| Scroll position | Proportional scaling | If 50% scrolled, stay 50% |
| Caret position | Preserve text offset | Cursor at character 47 stays |
| Hover state | Re-evaluate after layout | May change if mouse position changes |
| Modal state | Unchanged | Dialog stays modal |
| Drag state | May need abort | Complex; recommend abort on DPI change |

### 3.2 Scroll Position Algorithm

```python
def preserve_scroll_position(container, old_scale: float, new_scale: float):
    """
    Preserve logical scroll position across scale changes.
    """
    # Get current scroll in old scale
    old_scroll_px = container.scroll_y
    old_content_height_px = container.content_height
    old_viewport_height_px = container.viewport_height

    # Calculate scroll fraction
    scrollable_range = old_content_height_px - old_viewport_height_px
    if scrollable_range > 0:
        scroll_fraction = old_scroll_px / scrollable_range
    else:
        scroll_fraction = 0

    # Apply new scale to content
    container.update_content_scale(new_scale)

    # Restore scroll fraction
    new_content_height_px = container.content_height
    new_viewport_height_px = container.viewport_height
    new_scrollable_range = new_content_height_px - new_viewport_height_px

    if new_scrollable_range > 0:
        container.scroll_y = scroll_fraction * new_scrollable_range
    else:
        container.scroll_y = 0
```

### 3.3 Focus Preservation Algorithm

```python
def preserve_focus_across_transition(root_widget, old_focus_path: list[str]):
    """
    Restore focus to the same logical element after layout change.

    old_focus_path: path from root to focused element, e.g.,
                    ["main-content", "form", "email-input"]
    """
    # Walk the path to find the element
    current = root_widget
    for segment in old_focus_path:
        child = current.find_child_by_id(segment)
        if child is None:
            # Element no longer exists; focus container
            current.focus()
            return
        current = child

    # Found the element; restore focus
    current.focus()
```

---

## 4. Reflow Requirements

### 4.1 Reflow Contract (from SCALING_MATHEMATICS.md)

When S_eff changes, content must **reflow**, not clip or overlap:

| Behavior | Allowed | Description |
|----------|---------|-------------|
| Line wrap | Yes | Text wraps to fit container |
| Column stack | Yes | Multi-column becomes single |
| Menu collapse | Yes | Nav becomes hamburger |
| Scroll | Yes | Content scrolls vertically |
| Truncation | No | Text cut off with ellipsis |
| Overlap | No | Elements overlapping |
| Horizontal scroll | No | Content requires H-scroll |

### 4.2 Transition-Specific Reflow Rules

```yaml
transition_reflow:
  window_resize:
    rule: "Use suggested window rect from WM_DPICHANGED"
    rationale: "OS suggests proportional resize"

  content_reflow:
    rule: "Reflow after window resize, not before"
    rationale: "Accurate viewport dimensions needed"

  minimum_content:
    rule: "Primary content always visible without scroll"
    rationale: "User should not lose context"

  animation:
    rule: "Skip transition animations during DPI change"
    rationale: "Avoid jank and perceived slowness"
```

### 4.3 Breakpoint Recalculation

Responsive breakpoints must be re-evaluated at the new S_eff:

```python
def recalculate_breakpoints(viewport_width_px: float, s_eff: float):
    """
    Convert physical viewport to logical and check breakpoints.
    """
    viewport_width_lp = viewport_width_px / s_eff

    breakpoints = [
        (320, "mobile"),
        (768, "tablet"),
        (1024, "desktop"),
        (1440, "wide"),
    ]

    for threshold_lp, mode in breakpoints:
        if viewport_width_lp < threshold_lp:
            return mode

    return "ultra-wide"
```

---

## 5. Asset Re-rasterization

### 5.1 Scale-Dependent Assets

| Asset Type | Re-rasterization Strategy |
|------------|---------------------------|
| Vector icons (SVG) | Re-render at new size |
| Bitmap icons (@1x, @2x, @3x) | Select appropriate variant |
| Canvas/WebGL | Resize backing buffer |
| Fonts | System handles automatically |
| Images (photos) | Usually no change needed |

### 5.2 Icon Selection Algorithm

```python
def select_icon_variant(base_name: str, s_eff: float) -> str:
    """
    Select best icon variant for current scale.
    """
    available = ["@1x", "@1.5x", "@2x", "@3x", "@4x"]
    target_scale = s_eff

    # Prefer exact match or next higher
    for variant in available:
        variant_scale = float(variant[1:-1])
        if variant_scale >= target_scale:
            return f"{base_name}{variant}"

    # Fallback to highest available
    return f"{base_name}{available[-1]}"
```

### 5.3 Canvas/WebGL Resize

```javascript
function onDpiChange(canvas, newDpr) {
    // Get CSS size
    const cssWidth = canvas.clientWidth;
    const cssHeight = canvas.clientHeight;

    // Set backing buffer size
    canvas.width = cssWidth * newDpr;
    canvas.height = cssHeight * newDpr;

    // Update WebGL viewport
    const gl = canvas.getContext('webgl2');
    gl.viewport(0, 0, canvas.width, canvas.height);

    // Re-render
    render();
}
```

---

## 6. Transition Timing

### 6.1 Synchronous vs. Asynchronous

| Platform | Transition Model | Notes |
|----------|------------------|-------|
| Windows | Synchronous in WM_DPICHANGED | Must resize before returning |
| macOS | Asynchronous | Notification after change |
| GTK | Synchronous in signal handler | Redraw queued automatically |
| Qt | Asynchronous | changeEvent after new DPR set |

### 6.2 Recommended Timing

```python
class DpiTransitionHandler:
    def __init__(self):
        self.in_transition = False

    def on_dpi_change(self, old_scale: float, new_scale: float):
        """Handle DPI change with minimal user disruption."""
        self.in_transition = True

        # 1. Disable animations (avoid jank)
        self.disable_animations()

        # 2. Capture state
        focus_path = self.capture_focus_path()
        scroll_positions = self.capture_scroll_positions()

        # 3. Update scale factor
        self.set_scale(new_scale)

        # 4. Reset quantizer hysteresis (from QUANTIZATION_POLICY)
        self.quantizer.reset()

        # 5. Trigger synchronous reflow
        self.reflow_all()

        # 6. Restore state
        self.restore_focus(focus_path)
        self.restore_scroll_positions(scroll_positions, old_scale, new_scale)

        # 7. Re-enable animations after a frame
        self.schedule_next_frame(self.enable_animations)

        self.in_transition = False
```

### 6.3 Transition Duration Budget

| Phase | Budget | Notes |
|-------|--------|-------|
| State capture | < 1 ms | Just save references |
| Scale update | < 1 ms | Set variable |
| Reflow | < 16 ms | Target single frame |
| Asset reload | Async | Background thread |
| State restore | < 1 ms | Just set values |
| **Total** | < 20 ms | User should not perceive delay |

---

## 7. Multi-Monitor Scenarios

### 7.1 Window Spanning Two Monitors

When a window spans monitors with different scales:

| Platform | Behavior |
|----------|----------|
| Windows PMv2 | Uses scale of monitor with most window area |
| macOS | Each view uses its window's backingScaleFactor |
| Wayland | Compositor handles; apps see single scale |
| X11 | Global scale; no per-monitor support |

### 7.2 Drag Between Monitors

```python
def on_window_move(new_x: int, new_y: int, new_monitor: Monitor):
    """Handle window crossing monitor boundary."""
    if new_monitor == self.current_monitor:
        return  # Same monitor; no action

    old_scale = self.current_monitor.scale
    new_scale = new_monitor.scale

    if old_scale != new_scale:
        # Trigger full DPI transition
        self.on_dpi_change(old_scale, new_scale)

    self.current_monitor = new_monitor
```

### 7.3 VRR Monitor to Non-VRR

When transitioning to/from a VRR (Variable Refresh Rate) monitor:

```yaml
vrr_transition:
  entering_vrr:
    - Enable VRR_FLICKER_GATE validator
    - Check for VRR-aggravating patterns

  leaving_vrr:
    - Disable VRR_FLICKER_GATE (no longer relevant)
    - Patterns safe on fixed refresh

  always:
    - Flash safety (FLASH_GATE) unchanged
    - Animation timing unchanged (ms-based, not frame-based)
```

---

## 8. Testing Requirements

### 8.1 Transition Test Matrix

```yaml
test_scenarios:
  basic:
    - 96 DPI @ 1.0x -> 144 DPI @ 1.0x
    - 96 DPI @ 1.0x -> 96 DPI @ 2.0x
    - 144 DPI @ 1.0x -> 96 DPI @ 1.0x

  fractional:
    - 96 DPI @ 1.0x -> 96 DPI @ 1.25x
    - 144 DPI @ 1.5x -> 192 DPI @ 1.0x

  edge_cases:
    - Very low (76 DPI) -> very high (192 DPI)
    - User zoom during drag
    - Hot-plug during focus

  state_preservation:
    - Form with filled fields
    - Long scrollable document
    - Modal dialog open
    - Drag operation in progress
```

### 8.2 Automated Test Assertions

```python
def test_dpi_transition_no_content_loss():
    """Verify no text truncation or overlap after DPI change."""
    app = launch_app()

    # Get content summary before
    before_text = app.get_all_visible_text()
    before_elements = app.get_element_bounds()

    # Trigger DPI change
    simulate_dpi_change(app, 96, 192)

    # Get content after
    after_text = app.get_all_visible_text()
    after_elements = app.get_element_bounds()

    # Assert: all text still visible
    for text in before_text:
        assert text in after_text, f"Lost text: {text}"

    # Assert: no overlaps
    overlaps = find_overlapping_elements(after_elements)
    assert len(overlaps) == 0, f"Overlapping elements: {overlaps}"

def test_focus_preserved():
    """Focus should stay on same logical element."""
    app = launch_app()

    # Focus a specific input
    email_input = app.find("email-input")
    email_input.focus()
    assert email_input.has_focus()

    # Change DPI
    simulate_dpi_change(app, 96, 144)

    # Check focus still on email input
    email_input = app.find("email-input")  # Re-query after reflow
    assert email_input.has_focus()
```

---

## 9. Validator Integration

### 9.1 DPI_TRANSITION Gate

```yaml
dpi_transition_gate:
  id: GATE-DPI01
  severity: BLOCKING
  triggers:
    - on_dpi_change
    - on_window_move_to_monitor

  checks:
    - name: no_content_clipping
      rule: "All text visible without truncation after transition"
      severity: BLOCKING

    - name: no_element_overlap
      rule: "No interactive elements overlap after reflow"
      severity: BLOCKING

    - name: focus_preserved
      rule: "Focus remains on same logical element"
      severity: WARNING

    - name: scroll_position_preserved
      rule: "Scroll fraction within 5% of pre-transition"
      severity: ADVISORY

    - name: transition_timing
      rule: "Total transition < 100ms"
      severity: ADVISORY
```

---

## 10. Quick Reference

### 10.1 Platform Notification Summary

| Platform | Message/Signal | Scale Location |
|----------|----------------|----------------|
| Windows | WM_DPICHANGED | wParam (new DPI) |
| macOS | windowDidChangeBackingProperties | [window backingScaleFactor] |
| GTK 3/4 | notify::scale-factor | gtk_widget_get_scale_factor() |
| Qt 5/6 | QEvent::DevicePixelRatioChange | devicePixelRatio() |
| FLTK 1.4 | callback on scale change | Fl::screen_scale() |
| Wayland | wl_output.scale, fractional_scale | scale from event |

### 10.2 Transition Checklist

```
[ ] Capture focus path
[ ] Capture scroll positions
[ ] Disable animations
[ ] Reset quantizer hysteresis
[ ] Update S_eff
[ ] Reflow layout
[ ] Select new asset variants
[ ] Restore focus
[ ] Restore scroll positions (proportional)
[ ] Re-enable animations (next frame)
```

### 10.3 Common Mistakes

| Mistake | Consequence | Fix |
|---------|-------------|-----|
| Ignoring suggested rect (Windows) | Wrong window size | Use lParam rect |
| Not resetting hysteresis | Jitter after transition | Call quantizer.reset() |
| Animating during transition | Jank, perceived slowness | Disable animations |
| Double-scaling with DPR | Content too large/small | Use authoritative scale source |
| Not preserving scroll | User loses place | Proportional restoration |

---

*DPI Transition Contract Version 1.0.0 - Created 2025-12-27*
