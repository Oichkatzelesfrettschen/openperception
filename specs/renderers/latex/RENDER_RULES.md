# LaTeX Rendering Rules for UVAS Compliance

**Version:** 1.0.0
**Purpose:** Ensure LaTeX documents meet UVAS accessibility requirements

---

## 1. Document Setup

### 1.1 Required Preamble

```latex
\documentclass[11pt,a4paper]{article}

% Typography
\usepackage{libertinus}
\usepackage{libertinust1math}
\usepackage[scaled=0.95]{inconsolata}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}

% Spacing
\usepackage{setspace}
\onehalfspacing

% Margins (75 char line length at 11pt)
\usepackage[
  top=25mm,
  bottom=25mm,
  left=25mm,
  right=25mm
]{geometry}

% Colors with CVD-safe palette
\usepackage[dvipsnames,svgnames,table]{xcolor}

% Accessibility
\usepackage[a-3u]{pdfx}
\usepackage{accessibility}

% Hyperlinks
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=NavyBlue,
  citecolor=NavyBlue,
  urlcolor=NavyBlue,
  pdfborder={0 0 0}
}
```

---

## 2. Typography Invariants

### INV-LTX01: Minimum Body Size

```yaml
rule: "Body text >= 10pt"
default: 11pt
rationale: "Below 10pt, print readability degrades significantly"
validation: "Check \\normalsize definition"
```

### INV-LTX02: Line Spacing

```yaml
rule: "Line spacing >= 1.25 (\\onehalfspacing)"
default: 1.25 (setspace \\onehalfspacing)
rationale: "WCAG 1.4.12 requires 1.5x for web; 1.25x is print equivalent"
validation: "Check for \\singlespacing override"
```

### INV-LTX03: Line Length

```yaml
rule: "Line length <= 80 characters"
default: ~75 characters with standard margins
rationale: "Lines over 80 characters cause eye-tracking fatigue"
validation: "Calculate text width / average character width"
```

### INV-LTX04: Heading Hierarchy

```yaml
rule: "No skipped heading levels"
valid: "\\section → \\subsection → \\subsubsection"
invalid: "\\section → \\subsubsection (skipped subsection)"
validation: "Parse document structure"
```

---

## 3. Figure Rules

### 3.1 Alt Text Requirement

Every figure MUST have accessible alt text:

```latex
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.8\textwidth]{plot.pdf}
  \Description{Line chart showing accuracy increasing from 60% to 95%
               over 100 training epochs, with error bars showing
               standard deviation of approximately 2% at each point.}
  \caption{Training accuracy over epochs.}
  \label{fig:accuracy}
\end{figure}
```

### 3.2 Figure Readability

| Property | Minimum | Rationale |
|----------|---------|-----------|
| Stroke width | 1.0pt | Visibility at print scale |
| Font size in figures | 8pt | Legibility when figure scaled |
| Marker size | 4pt diameter | Distinguishability |
| Legend font | 9pt | Readability |

### 3.3 CVD-Safe Figures

```latex
% Use patterns in addition to colors
\usepackage{tikz}
\usetikzlibrary{patterns}

% Bad: Color-only encoding
\draw[red] (0,0) -- (1,1);
\draw[green] (0,1) -- (1,0);

% Good: Color + pattern/line style
\draw[red, thick, dashed] (0,0) -- (1,1);
\draw[green!70!black, thick, solid] (0,1) -- (1,0);
```

### 3.4 Figure Color Palette

Use this CVD-safe palette for categorical data:

```latex
\definecolor{uvas-blue}{HTML}{0077BB}
\definecolor{uvas-cyan}{HTML}{33BBEE}
\definecolor{uvas-teal}{HTML}{009988}
\definecolor{uvas-orange}{HTML}{EE7733}
\definecolor{uvas-red}{HTML}{CC3311}
\definecolor{uvas-magenta}{HTML}{EE3377}
\definecolor{uvas-gray}{HTML}{BBBBBB}
```

Palette verified for protanopia, deuteranopia, and tritanopia.

---

## 4. Table Rules

### 4.1 Table Accessibility

```latex
\usepackage{booktabs}  % Professional table rules
\usepackage{array}     % Enhanced column types

% Good table structure
\begin{table}[htbp]
  \centering
  \caption{Comparison of methods.}
  \label{tab:comparison}
  \begin{tabular}{lcc}
    \toprule
    Method & Accuracy & F1 Score \\
    \midrule
    Baseline & 0.72 & 0.68 \\
    Proposed & \textbf{0.89} & \textbf{0.85} \\
    \bottomrule
  \end{tabular}
\end{table}
```

### 4.2 Table Invariants

| Property | Requirement | Rationale |
|----------|-------------|-----------|
| Header row | Must be present | Screen reader navigation |
| Caption | Must be present | Context for data |
| Avoid color-only emphasis | Use **bold** or `\textbf{}` | CVD accessibility |
| Cell padding | Adequate whitespace | Readability |

---

## 5. Equation Rules

### 5.1 Equation Numbering

```latex
% Number all equations for reference
\begin{equation}
  E = mc^2
  \label{eq:einstein}
\end{equation}

% Reference: Equation~\ref{eq:einstein}
```

### 5.2 Long Equation Breaking

```latex
\usepackage{amsmath}

% Break long equations with alignment
\begin{align}
  f(x) &= a_0 + a_1 x + a_2 x^2 \nonumber \\
       &\quad + a_3 x^3 + a_4 x^4
  \label{eq:polynomial}
\end{align}
```

### 5.3 Equation Accessibility

For PDF/UA compliance, equations should have alt text:

```latex
% With accessibility package
\begin{equation}
  \pdftooltip{$E = mc^2$}{Energy equals mass times the speed of light squared}
\end{equation}
```

---

## 6. Code Listings

### 6.1 Listing Configuration

```latex
\usepackage{listings}
\lstset{
  basicstyle=\footnotesize\ttfamily,
  frame=single,
  breaklines=true,
  breakatwhitespace=true,
  tabsize=4,
  showstringspaces=false,
  numbers=left,
  numberstyle=\tiny\color{gray},
  backgroundcolor=\color{gray!10},
  keywordstyle=\bfseries\color{NavyBlue},
  stringstyle=\color{ForestGreen},
  commentstyle=\itshape\color{gray}
}
```

### 6.2 Code Accessibility

- Use semantic syntax highlighting (bold for keywords, not just color)
- Include line numbers for reference
- Provide caption explaining code purpose
- Keep line length <= 80 characters

---

## 7. PDF Accessibility Checklist

### 7.1 Structure

- [ ] Document has title (`\title{}`)
- [ ] Document has author (`\author{}`)
- [ ] PDF metadata set (`\hypersetup{pdftitle, pdfauthor}`)
- [ ] Tagged PDF enabled (`\usepackage{accessibility}`)
- [ ] Language specified (`\usepackage[english]{babel}`)

### 7.2 Navigation

- [ ] TOC included for documents > 5 pages
- [ ] Heading hierarchy is logical (no skipped levels)
- [ ] All sections are numbered (or explicitly unnumbered with `*`)
- [ ] Cross-references use `\ref{}` and `\label{}`

### 7.3 Images

- [ ] All figures have `\Description{}` alt text
- [ ] Figures have captions
- [ ] Color is not the only means of conveying information
- [ ] Minimum stroke width 1.0pt

### 7.4 Tables

- [ ] Tables have captions
- [ ] Header rows are present
- [ ] Complex tables have scope attributes (via accessibility package)

### 7.5 Links

- [ ] All URLs are hyperlinked
- [ ] Link text is descriptive (not "click here")
- [ ] Internal references use `\ref{}`

---

## 8. Validation Tools

### 8.1 Automated Checks

| Tool | Purpose | Command |
|------|---------|---------|
| pdftotext | Check text extraction | `pdftotext -layout doc.pdf` |
| PAC 3 | PDF/UA validation | GUI tool |
| axe-core | Accessibility audit | Web viewer test |
| chktex | LaTeX linting | `chktex doc.tex` |

### 8.2 Manual Checks

1. **Read aloud test**: Use screen reader (NVDA, VoiceOver) on PDF
2. **High contrast test**: View in Windows High Contrast mode
3. **Zoom test**: Verify readability at 200% zoom
4. **Reflow test**: Check text reflow on narrow screens

---

## 9. Template

Complete UVAS-compliant template:

```latex
% uvas-paper.tex
\documentclass[11pt,a4paper]{article}

%% Typography
\usepackage{libertinus}
\usepackage{libertinust1math}
\usepackage[scaled=0.95]{inconsolata}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}

%% Spacing
\usepackage{setspace}
\onehalfspacing

%% Layout
\usepackage[top=25mm,bottom=25mm,left=25mm,right=25mm]{geometry}
\usepackage{enumitem}
\setlist{itemsep=0.5ex,parsep=0pt,topsep=1ex}

%% Tables and Figures
\usepackage{booktabs}
\usepackage{graphicx}
\usepackage{caption}
\captionsetup{font=small,labelfont=bf}

%% Colors (CVD-safe)
\usepackage[dvipsnames,svgnames,table]{xcolor}
\definecolor{uvas-link}{HTML}{2C5282}

%% Code
\usepackage{listings}
\lstset{basicstyle=\footnotesize\ttfamily,frame=single,breaklines=true}

%% Math
\usepackage{amsmath,amssymb}

%% Accessibility
\usepackage[a-3u]{pdfx}
\usepackage{accessibility}

%% Hyperlinks
\usepackage{hyperref}
\hypersetup{
  colorlinks=true,
  linkcolor=uvas-link,
  citecolor=uvas-link,
  urlcolor=uvas-link,
  pdftitle={Document Title},
  pdfauthor={Author Name},
  pdflang={en-US}
}

%% Bibliography
\usepackage[backend=biber,style=numeric-comp]{biblatex}
\addbibresource{references.bib}

\title{Document Title}
\author{Author Name}
\date{\today}

\begin{document}
\maketitle

\begin{abstract}
Abstract text here.
\end{abstract}

\tableofcontents

\section{Introduction}
\label{sec:intro}

Body text here.

\printbibliography

\end{document}
```

---

*LaTeX Rendering Rules Version 1.0.0 - Generated 2025-12-27*
