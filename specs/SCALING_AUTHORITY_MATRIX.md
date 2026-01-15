# Scaling Authority Matrix

**Version:** 1.0.0
**Purpose:** Define which component owns scaling for each platform/toolkit to prevent double-scaling
**Companion to:** SCALING_MATHEMATICS.md, DPI_TRANSITION_CONTRACT.md

---

## 1. The Double-Scaling Problem

### 1.1 What Happens

When multiple layers each apply scaling, the result compounds:

```
Intended: 16 lp * 1.5 = 24 px

With double-scaling:
  App applies: 16 lp * 1.5 = 24 internal units
  Toolkit applies: 24 * 1.5 = 36 px

Result: 36 px instead of 24 px (50% too large!)
```

### 1.2 Common Causes

| Cause | Example | Symptom |
|-------|---------|---------|
| App queries DPI and scales, toolkit also scales | Qt app with manual DPI math | UI 2x too large |
| Environment variable + toolkit scaling | GDK_SCALE=2 + GTK auto | UI 4x too large |
| Multiple coordinate system conversions | DIPs -> pixels -> DIPs | Accumulated error |
| Window manager + compositor both scale | X11 with Xft.dpi + compositor | Blur, wrong size |

### 1.3 The Solution

Define a **single authority** for scaling per platform. All other layers operate in the authority's coordinate system.

---

## 2. Authority Matrix

### 2.1 Summary Table

| Platform | Primary Authority | Scale API | Coordinate System |
|----------|-------------------|-----------|-------------------|
| **Windows** | OS (Per-Monitor v2) | GetDpiForWindow() | DIPs (1/96 inch) |
| **macOS** | OS (Backing Scale) | backingScaleFactor | Points (1/72 inch) |
| **GTK 4** | Toolkit | gtk_widget_get_scale_factor() | Logical pixels |
| **GTK 3** | Toolkit + Env | GDK_SCALE + auto | Logical pixels |
| **GTK 2** | Environment | GDK_DPI_SCALE | No native HiDPI |
| **Qt 6** | Toolkit | devicePixelRatio() | Device-independent |
| **Qt 5** | Toolkit + Env | devicePixelRatio() | Device-independent |
| **FLTK 1.4** | Toolkit | Fl::screen_scale() | Logical pixels |
| **Wayland** | Compositor | wl_output.scale | Buffer scale |
| **X11** | Mixed (problematic) | Xft.dpi / Xresources | Varies |
| **Microwindows** | Application | No native HiDPI | Physical pixels |
| **Metacity/Marco** | Window Manager + GTK | window-scaling-factor | Logical pixels |
| **SDL2** | Toolkit (hint-based) | SDL_GetWindowSizeInPixels() | Configurable |
| **SDL3** | Toolkit (automatic) | SDL_GetWindowPixelDensity() | Points/pixels split |
| **LVGL** | Application (config) | LV_DPI_DEF in lv_conf.h | Physical pixels |
| **NuttX/NxWidgets** | Application | No native HiDPI | Physical pixels |
| **EFL/Elementary** | Toolkit | ELM_SCALE / finger size | Scale factor (not DPI) |
| **Tk** | Toolkit | tk scaling | Points (1/72 inch) |
| **Motif/LessTif** | Environment (X11) | Xft.dpi | Physical pixels |
| **Dear ImGui** | Application | io.DisplayFramebufferScale | Physical pixels |
| **Nuklear** | Application | Manual scaling | Physical pixels |

### 2.2 Decision Flow

```
Question: Who owns scaling?

1. Is there a native OS API that provides the scale factor?
   YES -> Use it as authority
   NO  -> Continue

2. Does the toolkit provide a scale factor API?
   YES -> Use it as authority
   NO  -> Continue

3. Is there an environment variable convention?
   YES -> Use it, document clearly
   NO  -> Application is authority (manual scaling)
```

---

## 3. Detailed Platform Guidance

### 3.1 Windows

**Authority:** OS via Per-Monitor DPI Awareness v2

**Setup:**
```xml
<!-- app.manifest -->
<application xmlns="urn:schemas-microsoft-com:asm.v3">
  <windowsSettings>
    <dpiAwareness xmlns="http://schemas.microsoft.com/SMI/2016/WindowsSettings">
      PerMonitorV2
    </dpiAwareness>
  </windowsSettings>
</application>
```

**Scaling Rule:**
```cpp
// The OS tells you the DPI; you respond to WM_DPICHANGED
// DO NOT query DPI and manually scale if already using PMv2

// CORRECT: Get DPI from window
UINT dpi = GetDpiForWindow(hwnd);
float scale = dpi / 96.0f;

// WRONG: Query monitor DPI separately and multiply again
// This causes double-scaling!
```

**Environment Variables:** None standard; avoid custom DPI overrides.

**Source:** [Microsoft Learn - High DPI Desktop Application Development](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows)

---

### 3.2 macOS

**Authority:** OS via backing scale factor

**Scaling Rule:**
```objc
// CORRECT: Let the system handle scaling
// Draw in points; system converts to pixels

// For custom drawing, query backing scale:
CGFloat scale = [[self window] backingScaleFactor];
// Use for @2x/@3x asset selection only

// WRONG: Multiply your point values by backingScaleFactor
// The system already does this at the rendering layer!
```

**Key Insight:**
> "For almost all common cases, developers should avoid using the backingScaleFactor as an input to layout or drawing calculations."
> -- Apple Developer Documentation

**Retina Pattern:**
```objc
// Asset selection, not coordinate scaling:
if ([[self window] backingScaleFactor] >= 2.0) {
    image = [NSImage imageNamed:@"icon@2x"];
} else {
    image = [NSImage imageNamed:@"icon"];
}
```

**Source:** [Apple Developer - backingScaleFactor](https://developer.apple.com/documentation/appkit/nswindow/1419459-backingscalefactor)

---

### 3.3 GTK 4

**Authority:** Toolkit (automatic on Wayland/X11)

**Scaling Rule:**
```c
// GTK 4 handles scaling internally
// DO NOT manually multiply by scale factor for layout

// For asset selection:
int scale = gtk_widget_get_scale_factor(widget);

// For fractional (4.14+):
double frac_scale = gdk_surface_get_scale(gdk_surface);
```

**Fractional Scaling (Wayland, GTK 4.14+):**
```bash
# Enable fractional GL rendering (experimental)
GDK_DEBUG=gl-fractional ./myapp
```

**Environment Variables:**

| Variable | Effect | Use Case |
|----------|--------|----------|
| GDK_SCALE | Integer scale multiplier | Testing |
| GDK_DPI_SCALE | Text-only scaling | Accessibility |

**Warning:** Do not set both GDK_SCALE and let GTK auto-detect; this causes double-scaling.

**Source:** [GTK 4 High DPI](https://docs.gtk.org/gtk4/property.Widget.scale-factor.html)

---

### 3.4 GTK 3

**Authority:** Toolkit + Environment (mixed)

**Scaling Rule:**
```c
// GTK 3 only supports integer scaling
// Fractional values are rounded down

int scale = gtk_widget_get_scale_factor(widget);

// GDK_SCALE overrides auto-detection
```

**Common Pattern (HiDPI):**
```bash
# 2x scaling with half-size text (net: large UI, normal text)
export GDK_SCALE=2
export GDK_DPI_SCALE=0.5
./gtk3_app
```

**Plasma 5.27+ Note:**
> "Plasma 5.27 dropped use of GDK_SCALE/GDK_DPI_SCALE variables and switched to Xsettingsd."

**Source:** [Arch Wiki - HiDPI](https://wiki.archlinux.org/title/HiDPI)

---

### 3.5 GTK 2

**Authority:** Environment (no native HiDPI support)

**Scaling Rule:**
```bash
# GTK 2 has no native HiDPI support
# Use environment-based DPI scaling:
export GDK_DPI_SCALE=1.5
./gtk2_app

# Or Xft.dpi in ~/.Xresources:
# Xft.dpi: 144
```

**Limitations:**
- No integer scaling (GDK_SCALE not supported)
- Icons may not scale properly
- Bitmap fonts may look bad

**Recommendation:** Migrate to GTK 3+ for HiDPI support.

---

### 3.6 Qt 6

**Authority:** Toolkit (automatic)

**Scaling Rule:**
```cpp
// Qt 6 is Per-Monitor DPI Aware V2 by default
// DO NOT manually scale if using devicePixelRatio

qreal dpr = widget->devicePixelRatio();
// Use for asset selection only, not layout

// WRONG:
int width_px = my_width_lp * dpr;  // Qt already did this!

// CORRECT:
int width = 200;  // Device-independent; Qt scales at render
```

**Important:**
> "The effective device pixel ratio, as returned by QWindow::devicePixelRatio(), will be a product of the set scale factor and the native device pixel ratio."

This means `QT_SCALE_FACTOR=2` on a 2x display yields DPR of 4!

**Environment Variables:**

| Variable | Effect | Danger Level |
|----------|--------|--------------|
| QT_SCALE_FACTOR | Multiplies DPR | HIGH (compounds!) |
| QT_AUTO_SCREEN_SCALE_FACTOR | 0 disables auto | Medium |
| QT_ENABLE_HIGHDPI_SCALING | 0 reverts to Qt 5 behavior | Medium |

**Source:** [Qt 6 High DPI](https://doc.qt.io/qt-6/highdpi.html)

---

### 3.7 Qt 5

**Authority:** Toolkit + Environment

**Scaling Rule:**
```cpp
// Qt 5 requires opt-in for high DPI:
QApplication::setAttribute(Qt::AA_EnableHighDpiScaling);

// Then use devicePixelRatio for assets:
qreal dpr = widget->devicePixelRatio();
```

**Environment Variables:**
```bash
# Enable automatic scaling
export QT_AUTO_SCREEN_SCALE_FACTOR=1
export QT_SCALE_FACTOR=1  # Optional override

./qt5_app
```

---

### 3.8 FLTK 1.4+

**Authority:** Toolkit

**Scaling Rule:**
```cpp
// FLTK 1.4 provides per-screen scale factors
float scale = Fl::screen_scale(Fl::screen_num(x(), y(), w(), h()));

// User can change at runtime with Ctrl+/Ctrl-/Ctrl0
// Disable with:
Fl::keyboard_screen_scaling(0);  // Before fl_open_display()
```

**Environment Override:**
```bash
# Multiply OS-provided scale by factor
export FLTK_SCALING_FACTOR=1.5
./fltk_app
```

**Retina/HiDPI:**
```cpp
// FLTK 1.4 automatically uses high-resolution backing on macOS
// and fractional scales on Wayland
```

**Source:** [FLTK Screen Functions](https://www.fltk.org/doc-1.4/group__fl__screen.html)

---

### 3.9 Microwindows/Nano-X

**Authority:** Application (no native HiDPI)

**Status:** Microwindows does not have native high-DPI scaling support. Applications must implement their own scaling.

**Scaling Rule:**
```c
// Query screen dimensions
int screen_width, screen_height;
GrGetScreenInfo(&screen_width, &screen_height);

// Application must compute and apply scale manually
float user_scale = get_user_preference();  // e.g., 1.5
int my_widget_width = 100 * user_scale;
```

**Recommendations for Microwindows:**
1. Define a reference DPI (96) in your application
2. Query actual DPI if available from hardware/driver
3. Compute S_eff = actual_dpi / 96 * user_scale
4. Apply to all layout calculations
5. Use UVAS+ token system for consistency

**Source:** [GitHub - ghaerr/microwindows](https://github.com/ghaerr/microwindows)

---

### 3.10 Metacity / Marco (MATE)

**Authority:** Window Manager + GTK (org.mate.desktop.interface.window-scaling-factor)

**MATE HiDPI (1.20+):**
```bash
# Set via gsettings:
gsettings set org.mate.desktop.interface window-scaling-factor 2

# Dynamic detection enabled by default
# Toggle triggers resize without log out
```

**Known Issue:**
> "Marco appears as if it is using a scale of 1 (original size)" when window-scaling-factor is set higher.

**Workaround:**
```bash
# Force Marco to respect scale:
gsettings set org.mate.Marco.general force-window-scale 2
```

**Metacity (GNOME 2/Flashback):**
```bash
# Similar pattern:
gsettings set org.gnome.desktop.interface scaling-factor 2
```

**Source:** [GitHub - mate-desktop/marco](https://github.com/mate-desktop/marco)

---

### 3.11 SDL2

**Authority:** Toolkit (hint-based, configurable)

**Setup:**
```c
// Enable high DPI mode at window creation
SDL_Window *window = SDL_CreateWindow("My App",
    SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
    640, 480,
    SDL_WINDOW_ALLOW_HIGHDPI);  // This flag is key

// Or use the Windows DPI scaling hint (recommended for Windows)
SDL_SetHint(SDL_HINT_WINDOWS_DPI_SCALING, "1");
```

**Scaling Rule:**
```c
// Get logical window size (what you requested)
int w, h;
SDL_GetWindowSize(window, &w, &h);

// Get actual pixel size (what you draw to)
int pw, ph;
SDL_GetWindowSizeInPixels(window, &pw, &ph);

// Calculate scale factor
float scale = (float)pw / (float)w;

// For rendering, use pixel dimensions:
SDL_RenderSetLogicalSize(renderer, w, h);  // SDL handles scaling
```

**Platform Differences:**
| Platform | Coordinate System | Note |
|----------|-------------------|------|
| macOS/iOS | Points | High DPI via flag |
| Windows | DIPs or pixels | Controlled by hint |
| Linux/X11 | Pixels | Similar to Windows |
| Linux/Wayland | Points-like | Similar to macOS |

**Source:** [SDL Wiki - SDL_HINT_WINDOWS_DPI_SCALING](https://wiki.libsdl.org/SDL2/SDL_HINT_WINDOWS_DPI_SCALING)

---

### 3.12 SDL3

**Authority:** Toolkit (automatic, improved)

**Key Changes from SDL2:**
- Window size is now distinct from window pixel size
- `SDL_WINDOW_HIGH_PIXEL_DENSITY` flag for high-res backing
- `SDL_GetWindowPixelDensity()` returns the ratio

**Scaling Rule:**
```c
// Create high pixel density window
SDL_Window *window = SDL_CreateWindow("My App",
    640, 480,
    SDL_WINDOW_HIGH_PIXEL_DENSITY);

// Get the content scale for UI sizing
float content_scale = SDL_GetWindowDisplayScale(window);

// Get pixel density for rendering
float pixel_density = SDL_GetWindowPixelDensity(window);

// UI sizing: multiply logical sizes by content_scale
int button_height = 44 * content_scale;

// Rendering: use pixel density for asset selection
```

**Source:** [SDL GitHub - High DPI Plan](https://github.com/libsdl-org/SDL/issues/7134)

---

### 3.13 LVGL

**Authority:** Application (configuration-based)

**Setup (lv_conf.h):**
```c
/* Default Dot Per Inch. Used to initialize default sizes. */
#define LV_DPI_DEF 130  // Adjust to your display's actual DPI

/* If you're using a high-density display, set this higher.
 * This affects default widget sizes and style paddings. */
```

**Scaling Rule:**
```c
// LVGL uses pixels directly
// To implement logical scaling, wrap your sizes:

#define SCALE_FACTOR 1.5f
#define LP_TO_PX(lp) ((lv_coord_t)((lp) * SCALE_FACTOR))

// Usage:
lv_obj_set_size(button, LP_TO_PX(100), LP_TO_PX(44));

// Or use styles with scaled values:
static lv_style_t style;
lv_style_set_width(&style, LP_TO_PX(100));
lv_style_set_height(&style, LP_TO_PX(44));
```

**Recommendations for LVGL:**
1. Set LV_DPI_DEF to your target display's actual DPI
2. Use consistent scale factors for all widgets
3. Consider creating a UVAS+-compatible wrapper layer
4. For multi-DPI support, reconfigure and rebuild layout on DPI change

**Source:** [LVGL Documentation](https://lvgl.io/)

---

### 3.14 NuttX/NxWidgets

**Authority:** Application (no native HiDPI)

**Status:** NxWidgets provides a windowing system for embedded NuttX, but does not include built-in DPI awareness. Applications must implement scaling manually.

**Scaling Rule:**
```cpp
// NxWidgets operates in physical pixels
// Implement UVAS+-style scaling:

class UvasScaler {
private:
    float m_scale;

public:
    UvasScaler(int target_dpi) {
        m_scale = target_dpi / 96.0f;
    }

    nxgl_coord_t lp_to_px(float lp) {
        return (nxgl_coord_t)(lp * m_scale + 0.5f);
    }
};

// Usage in widget creation:
UvasScaler scaler(my_display_dpi);
button->resize(scaler.lp_to_px(100), scaler.lp_to_px(44));
```

**Recommendations:**
- Detect display DPI from hardware if available
- Store user scale preference in NuttX settings
- Apply consistent scaling to all NxWidget instances
- Use CONFIG_NX_NPLANES for multi-display awareness

**Source:** [NuttX NxWidgets Documentation](https://nuttx.apache.org/docs/latest/applications/graphics/nxwidgets/index.html)

---

### 3.15 EFL/Elementary

**Authority:** Toolkit (explicit scale factor, not DPI-based)

**Philosophy:**
> "DPI is not a solution - for example, a TV. Even if we scaled on a phone based on DPI we'd be far too big because phones are normally held at 1/3rd the distance from a user than a desktop screen might be. Thus explicit scale factor to deal with the COMBO of view distance PLUS DPI."

**Scaling Rule:**
```c
// EFL uses explicit scale factor, not automatic DPI
elm_config_scale_set(1.5);  // Set programmatically

// Or via environment:
// ELM_SCALE=1.5 ./my_efl_app

// Finger size for touch targets:
elm_config_finger_size_set(50);  // Pixels
```

**Configuration Methods:**

| Method | Scope | Persistence |
|--------|-------|-------------|
| ELM_SCALE env var | Per-launch | None |
| elm_config_scale_set() | Runtime | Optional |
| Elementary Config Tool | User preference | Persistent |
| Profile | Per-device class | Persistent |

**Source:** [Enlightenment Foundation Libraries](https://www.enlightenment.org/about-efl.md)

---

### 3.16 Tk (Tcl/Tk)

**Authority:** Toolkit (tk scaling command)

**Scaling Rule:**
```tcl
# Query current scaling (pixels per point; 1 point = 1/72 inch)
set current_scale [tk scaling]

# Set scaling for high DPI (e.g., 144 DPI = 2.0 scaling)
tk scaling 2.0

# Calculate from actual DPI:
# scaling = dpi / 72
tk scaling [expr {$my_dpi / 72.0}]
```

**Platform Behavior:**

| Platform | tk scaling Behavior |
|----------|---------------------|
| macOS (Aqua) | Always returns 100; desktop scales automatically |
| X11 | Derived from Xft.dpi; can be set manually |
| Windows | Reflects system DPI settings |

**Best Practices:**
```tcl
# Use point sizes for fonts (not pixels):
font create myfont -family "Helvetica" -size 12  # 12 points

# Use pt suffix for padding:
grid $someWidget -padx 7pt -pady 7pt

# Avoid pixel sizes for resizable elements
```

**Known Limitations:**
- No automatic icon scaling (until Tk 8.7 with SVG support)
- Window size is always in pixels; not portable to HiDPI

**Source:** [Tcl Wiki - tk scaling](https://wiki.tcl-lang.org/page/tk+scaling)

---

### 3.17 Motif/LessTif

**Authority:** Environment (X11-based, no native HiDPI)

**Status:** Legacy toolkit with no built-in HiDPI support. Relies on X11 font DPI settings.

**Scaling Workarounds:**
```bash
# Set X font DPI (affects Xft-rendered text):
# In ~/.Xresources:
Xft.dpi: 144

# Apply:
xrdb -merge ~/.Xresources

# Or at X startup:
xrandr --dpi 144
```

**Limitations:**
- Icons do not scale
- Widget geometry is in pixels
- Scrollbars and other chrome remain small
- No per-monitor awareness

**Recommendations:**
1. Use Xft.dpi for text scaling
2. Consider compositor-level scaling (not ideal)
3. For new development, migrate to a modern toolkit
4. If maintaining legacy Motif app, implement manual scaling layer

**Source:** [Arch Wiki - HiDPI](https://wiki.archlinux.org/title/HiDPI)

---

### 3.18 Dear ImGui

**Authority:** Application (manual scaling required)

**Scaling Rule:**
```cpp
// ImGui requires explicit scaling setup
ImGuiIO& io = ImGui::GetIO();

// 1. Scale fonts
ImFontConfig config;
config.SizePixels = 16.0f * my_scale;
io.Fonts->AddFontDefault(&config);

// 2. Set framebuffer scale (for retina/HiDPI)
io.DisplayFramebufferScale = ImVec2(my_scale, my_scale);

// 3. Scale style
ImGuiStyle& style = ImGui::GetStyle();
style.ScaleAllSizes(my_scale);
```

**With SDL2 Backend:**
```cpp
// Get scale from SDL
int w, h, pw, ph;
SDL_GetWindowSize(window, &w, &h);
SDL_GetWindowSizeInPixels(window, &pw, &ph);
float scale = (float)pw / (float)w;

// Apply to ImGui
io.DisplaySize = ImVec2((float)w, (float)h);
io.DisplayFramebufferScale = ImVec2(scale, scale);
```

**Source:** [ImGui GitHub Issue #2956](https://github.com/ocornut/imgui/issues/2956)

---

### 3.19 Nuklear

**Authority:** Application (manual scaling required)

**Scaling Rule:**
```c
// Nuklear operates in pixels; implement scaling wrapper

struct nk_context ctx;
float scale = 1.5f;  // User/DPI-derived scale

// Scale font
struct nk_font_atlas *atlas;
nk_font_atlas_init_default(&atlas);
nk_font_atlas_begin(&atlas);
struct nk_font *font = nk_font_atlas_add_default(atlas, 14.0f * scale, NULL);
// ... bake atlas

// Scale layout
nk_layout_row_dynamic(&ctx, 30 * scale, 1);

// Or use a size helper:
#define NK_SCALED(x) ((x) * scale)
nk_layout_row_dynamic(&ctx, NK_SCALED(30), 1);
```

**Integration with Microwindows:**
Nuklear is included with Microwindows. Apply the same manual scaling approach, using UVAS+ tokens for consistency.

**Source:** [GitHub - ghaerr/microwindows](https://github.com/ghaerr/microwindows)

---

## 4. Cross-Toolkit Applications

### 4.1 Electron / CEF

**Authority:** Chromium compositor

```javascript
// Electron handles scaling internally
// Access DPR for asset selection:
const dpr = window.devicePixelRatio;

// For CSS, use device-independent units:
element.style.width = '200px';  // Not 200 * dpr!
```

### 4.2 Java Swing/AWT

**Authority:** JVM + Environment

```bash
# Force scaling in Java:
export GDK_SCALE=2  # For GTK look-and-feel
java -Dsun.java2d.uiScale=2.0 -jar myapp.jar
```

### 4.3 wxWidgets

**Authority:** Follows underlying toolkit (GTK on Linux, native on Windows/macOS)

```cpp
// Query DPI from wxWindow:
wxSize dpi = GetDPI();
double scale = dpi.GetWidth() / 96.0;
```

---

## 5. Environment Variable Reference

### 5.1 GTK Variables

| Variable | GTK 2 | GTK 3 | GTK 4 | Effect |
|----------|-------|-------|-------|--------|
| GDK_SCALE | No | Yes (int) | Yes (int) | Scale factor multiplier |
| GDK_DPI_SCALE | Yes | Yes | Yes | Text scaling only |
| GDK_DEBUG=gl-fractional | No | No | Yes | Enable fractional GL |

### 5.2 Qt Variables

| Variable | Qt 5 | Qt 6 | Effect |
|----------|------|------|--------|
| QT_AUTO_SCREEN_SCALE_FACTOR | Opt-in | Default | Enable auto DPI |
| QT_SCALE_FACTOR | Yes | Yes | Force scale (compounds!) |
| QT_ENABLE_HIGHDPI_SCALING | N/A | Yes | Master switch |

### 5.3 Other Variables

| Variable | Platform | Effect |
|----------|----------|--------|
| FLTK_SCALING_FACTOR | FLTK 1.4 | Multiplies detected scale |
| ELM_SCALE | Enlightenment | Elementary widget scale |
| STEAM_FORCE_DESKTOPUI_SCALING | Steam | UI scale override |

---

## 6. Avoiding Double-Scaling: Decision Tree

```
START: Need to draw at 200 logical pixels wide

Q1: Does my toolkit provide devicePixelRatio / scale_factor API?
    |
    +-- YES: Use toolkit's layout system with 200 units
    |        (Toolkit handles conversion to physical pixels)
    |
    +-- NO: Continue to Q2

Q2: Am I setting environment variables for scaling?
    |
    +-- YES: Ensure I'm NOT also querying DPI and scaling manually
    |
    +-- NO: Continue to Q3

Q3: Is the platform Windows with DPI awareness manifest?
    |
    +-- YES: Use DIPs (200 means 200 DIPs, OS scales at compositing)
    |
    +-- NO: Continue to Q4

Q4: Am I on a legacy/embedded platform (Microwindows, etc.)?
    |
    +-- YES: I am the authority; implement scaling myself
    |
    +-- NO: Check platform documentation
```

---

## 7. Testing for Double-Scaling

### 7.1 Visual Test

1. Launch app at 100% scale
2. Measure a known element (e.g., button width 200lp should be 200px)
3. Change to 200% scale
4. Measure same element (should be 400px)
5. If 800px: **double-scaling detected**

### 7.2 Automated Test

```python
def test_no_double_scaling():
    """Verify scaling is applied exactly once."""
    app = launch_app()

    for scale in [1.0, 1.5, 2.0]:
        set_system_scale(scale)
        refresh_app(app)

        button = app.find("test-button")
        expected_width = 200 * scale  # 200lp button
        actual_width = button.physical_width()

        # Allow 2px tolerance for rounding
        assert abs(actual_width - expected_width) <= 2, \
            f"At scale {scale}: expected {expected_width}px, got {actual_width}px"
```

### 7.3 Log-Based Detection

```cpp
void debugScaleInfo() {
    // Log all scale-related values
    LOG("OS DPI: %d", GetDpiForWindow(hwnd));
    LOG("devicePixelRatio: %f", window->devicePixelRatio());
    LOG("GDK_SCALE env: %s", getenv("GDK_SCALE"));
    LOG("QT_SCALE_FACTOR env: %s", getenv("QT_SCALE_FACTOR"));
    LOG("Computed S_eff: %f", s_eff);

    // Check for suspicious values
    if (s_eff > 3.0 && getenv("QT_SCALE_FACTOR")) {
        LOG("WARNING: Possible double-scaling detected!");
    }
}
```

---

## 8. Quick Reference

### 8.1 "Don't Touch Scaling" Platforms

On these platforms, the toolkit/OS handles everything:
- Windows (with PMv2 manifest)
- macOS (always)
- GTK 4 on Wayland
- Qt 6 (default config)

Just use device-independent units and trust the system.

### 8.2 "You Must Configure" Platforms

On these platforms, some setup is required:
- GTK 3 (set GDK_SCALE if auto-detect fails)
- Qt 5 (enable high DPI explicitly)
- X11 (set Xft.dpi or use Xsettingsd)

### 8.3 "You Are the Authority" Platforms

On these platforms, implement scaling yourself:
- Microwindows/Nano-X
- NuttX/NxWidgets
- LVGL (configure LV_DPI_DEF)
- Dear ImGui
- Nuklear
- Custom OpenGL/Vulkan without toolkit
- Legacy embedded systems

### 8.4 "Uses Explicit Scale Factor (Not DPI)" Platforms

On these platforms, scale is explicit and may account for viewing distance:
- EFL/Elementary (ELM_SCALE)
- Tk (tk scaling command)
- SDL2/SDL3 (content scale + pixel density)

### 8.5 "Legacy, No Real HiDPI" Platforms

On these platforms, HiDPI is limited to workarounds:
- GTK 2 (GDK_DPI_SCALE for text only)
- Motif/LessTif (Xft.dpi for text only)
- FLTK 1.3 (no scaling support)

---

## 9. Revision History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-12-27 | Initial release |

---

*Scaling Authority Matrix Version 1.0.0 - Created 2025-12-27*

## References

### Platform Documentation
- [Microsoft Learn - High DPI Desktop Application Development](https://learn.microsoft.com/en-us/windows/win32/hidpi/high-dpi-desktop-application-development-on-windows)
- [Apple Developer - backingScaleFactor](https://developer.apple.com/documentation/appkit/nswindow/1419459-backingscalefactor)
- [Arch Wiki - HiDPI](https://wiki.archlinux.org/title/HiDPI)

### Major Toolkit Documentation
- [Qt 6 High DPI](https://doc.qt.io/qt-6/highdpi.html)
- [GTK 4 Widget scale-factor](https://docs.gtk.org/gtk4/property.Widget.scale-factor.html)
- [FLTK Screen Functions](https://www.fltk.org/doc-1.4/group__fl__screen.html)
- [SDL Wiki - SDL_HINT_WINDOWS_DPI_SCALING](https://wiki.libsdl.org/SDL2/SDL_HINT_WINDOWS_DPI_SCALING)
- [SDL GitHub - High DPI Plan](https://github.com/libsdl-org/SDL/issues/7134)
- [Enlightenment Foundation Libraries](https://www.enlightenment.org/about-efl.md)
- [Tcl Wiki - tk scaling](https://wiki.tcl-lang.org/page/tk+scaling)

### Embedded/Specialty Toolkit Documentation
- [LVGL Documentation](https://lvgl.io/)
- [NuttX NxWidgets Documentation](https://nuttx.apache.org/docs/latest/applications/graphics/nxwidgets/index.html)
- [GitHub - ghaerr/microwindows](https://github.com/ghaerr/microwindows)
- [ImGui GitHub Issue #2956](https://github.com/ocornut/imgui/issues/2956)

### Window Manager Documentation
- [GitHub - mate-desktop/marco](https://github.com/mate-desktop/marco)
