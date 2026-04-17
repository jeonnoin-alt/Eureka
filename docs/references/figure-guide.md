# Figure Guide

This is a reference document, not a skill. It provides lookup tables and copy-paste-ready recipes for research figure design — chart-type selection, typography, colorblind-safe palettes, journal-specific export specs, matplotlib style, and accessibility testing tools. Referenced by `eureka:figure-design` when creating or reviewing figures.

---

## 1. Chart Type Selection Flowchart

Start from the figure's purpose (one sentence). Pick the first matching row:

| Purpose | Data shape | First choice | Acceptable alternative |
|---|---|---|---|
| Compare groups on one metric | ≤5 discrete categories, one value each | Horizontal bar | Grouped vertical bar, dot plot |
| Compare groups on one metric | 6-20 discrete categories | Dot plot, lollipop | Heatmap |
| Compare groups on one metric | >20 categories | Heatmap with clustering | Faceted small multiples |
| Show distribution (one variable) | Continuous, one group | Histogram, density plot | Violin plot |
| Show distribution (multiple groups) | Continuous, few groups | Violin + raw points, raincloud | Box plot with jitter |
| Show trend over time | Continuous x, continuous y | Line plot with CI band | Scatter with LOESS |
| Show trend over time (discrete timepoints) | Discrete x, continuous y | Point + line with error bars | Slope chart |
| Show relationship | Two continuous variables | Scatter + regression | Hexbin (N large) |
| Show relationship | Three continuous variables | Scatter with size encoding | Faceted scatter grid |
| Show rank | Ordered list of items | Horizontal bar, dot plot | Slope chart (ranks across 2 conditions) |
| Part-to-whole | Few categories summing to 100% | Stacked horizontal bar | Waffle chart, tree map |
| Show flow | From categories to categories | Sankey diagram, alluvial | Chord diagram |
| Show spatial pattern | Geographic, anatomical | Choropleth, heatmap on coordinates | Glass brain (neuroscience) |
| Show network | Nodes and edges | Force-directed graph, arc diagram | Adjacency matrix heatmap |
| Show matrix | All pairwise comparisons | Correlation matrix heatmap | Clustered heatmap |

**Never use:**

- 3D bar chart or 3D pie chart — 3D projection distorts comparison
- Pie chart with >3 slices — angle comparison is harder than length comparison
- Rainbow / `jet` colormap for any sequential data — not perceptually uniform
- Gradient fills for categorical data — implies ordering that doesn't exist
- Dual y-axes with unrelated scales — invites misleading visual correlation

---

## 2. Typography Reference

### Font family by journal

| Journal family | Preferred font |
|---|---|
| Nature family | Arial or Helvetica |
| Science family | Helvetica |
| Cell family | Arial or Helvetica |
| JAMA, NEJM | Arial |
| IEEE Transactions | Times (body text), Helvetica (figures) |
| PNAS | Arial |

**Rule of thumb:** use the same sans-serif font across ALL figures in a single paper. Mixing Arial and Helvetica across figures is a reviewer's cheap hit.

### Font size

- **Minimum**: 5pt (absolute floor; 6pt is safer)
- **Axis tick labels**: 6-7pt
- **Axis labels**: 7-8pt
- **Legend entries**: 6-7pt
- **Panel labels (a, b, c)**: 8-10pt, bold
- **Title**: 8-10pt (but most top journals discourage within-figure titles — the caption carries the title)

### TrueType embedding (matplotlib)

Default matplotlib embeds Type 3 fonts, which most journals reject. Set once at the top of the script:

```python
import matplotlib as mpl
mpl.rcParams['pdf.fonttype'] = 42   # TrueType
mpl.rcParams['ps.fonttype'] = 42    # TrueType for PS output
```

To verify a submitted PDF uses TrueType, open the PDF in Acrobat → File → Properties → Fonts tab. TrueType fonts are listed; Type 3 fonts are flagged.

---

## 3. Color Palette Reference

### Qualitative palettes (discrete categories, no order)

**Okabe-Ito (8 colors, colorblind-safe, recommended)**:

```
Black:       #000000
Orange:      #E69F00
Sky Blue:    #56B4E9
Bluish Green:#009E73
Yellow:      #F0E442
Blue:        #0072B2
Vermilion:   #D55E00
Reddish Purple: #CC79A7
```

**tol-bright (7 colors, colorblind-safe)**:

```
Blue:   #4477AA
Cyan:   #66CCEE
Green:  #228833
Yellow: #CCBB44
Red:    #EE6677
Purple: #AA3377
Grey:   #BBBBBB
```

**Matplotlib `tab10`** (10 colors, adequate for ≤5 categories; check specific pairs with Coblis for safety):

```
#1f77b4  #ff7f0e  #2ca02c  #d62728  #9467bd
#8c564b  #e377c2  #7f7f7f  #bcbd22  #17becf
```

**Rules:**
- Use at most 8 qualitative colors in one figure; beyond that, human discrimination saturates
- Never combine red and green as the only categorical contrast
- Assign colors semantically: if "model A" is blue in Figure 2, it stays blue throughout the paper

### Sequential palettes (ordered magnitude, one direction)

All of these are perceptually uniform AND colorblind-safe:

| Palette | Character | Best for |
|---|---|---|
| `viridis` | Purple → green → yellow | General-purpose sequential |
| `cividis` | Dark blue → yellow | Colorblind-optimized (designed for it) |
| `plasma` | Purple → pink → yellow | High-contrast alternative |
| `inferno` | Black → red → yellow | Dark-background presentations |
| `magma` | Black → purple → white | Dark-background, softer |

**Never:** `jet`, `rainbow`, `hsv`, `spectral` for sequential data. They are not perceptually uniform and confuse colorblind readers.

### Diverging palettes (zero-centered, positive/negative)

| Palette | Endpoints | Notes |
|---|---|---|
| `RdBu_r` | Red (positive) ↔ Blue (negative) | Classic; colorblind-safe |
| `coolwarm` | Blue ↔ Red | Similar to RdBu_r, slightly softer |
| `PuOr` | Purple ↔ Orange | Alternative when red/blue is overused |
| `BrBG` | Brown ↔ Blue-Green | For soil/vegetation or similar semantics |

**Rule:** anchor the midpoint at zero explicitly — do not let the default colorbar put zero off-center.

### Colorblind-safety quick check

- Red ↔ Green: AVOID as the only contrast
- Red ↔ Blue: SAFE
- Orange ↔ Blue: SAFE (Okabe-Ito uses this)
- Purple ↔ Yellow: SAFE
- Green ↔ Magenta: SAFE (microscopy: use magenta/green instead of red/green)

---

## 4. Journal-Specific Export Specifications

| Journal | 1-col width | 1.5-col width | 2-col width | Max height | Font | Font size | DPI (raster) | Preferred vector | Accepted raster |
|---|---|---|---|---|---|---|---|---|---|
| Nature | 89 mm | — | 183 mm | 247 mm | Arial/Helvetica | 5-7 pt | 300+ | PDF, AI, EPS | TIFF, PNG |
| Nat Communications | 85 mm | — | 180 mm | 225 mm | Arial/Helvetica | 5-7 pt | 300+ | PDF, EPS | TIFF, PNG |
| Science | 55 mm | 115 mm | 180 mm | 240 mm | Helvetica | 6-12 pt | 300+ | PDF, EPS | TIFF |
| Science Advances | 55 mm | 115 mm | 180 mm | 240 mm | Helvetica | 6-12 pt | 300+ | PDF, EPS | TIFF |
| Cell | 85 mm | 114 mm | 174 mm | 225 mm | Arial/Helvetica | 6-8 pt | 300+ | PDF | TIFF, EPS |
| Neuron | 85 mm | 114 mm | 174 mm | 225 mm | Arial/Helvetica | 6-8 pt | 300+ | PDF | TIFF |
| JAMA | 3.375" (86mm) | — | 6.75" (171mm) | 9.25" (235mm) | Arial | 7-9 pt | 300+ | EPS, PDF | TIFF |
| NEJM | 3.25" (83mm) | — | 6.75" (171mm) | 9" (229mm) | Arial | 7-9 pt | 300+ | EPS, PDF | TIFF |
| IEEE Transactions | 3.5" (89mm) | — | 7.16" (182mm) | — | Times/Helvetica | 8pt min | 300+ | PDF, EPS | — |
| PNAS | 8.7 cm (87mm) | 11.4 cm | 17.8 cm | 22 cm | Arial | 7-9 pt | 300+ | PDF, EPS | TIFF |
| NeuroImage | 90 mm | — | 190 mm | 240 mm | Arial | 7-8 pt | 300+ | PDF, EPS | TIFF |
| Brain | 85 mm | — | 175 mm | 230 mm | Arial | 7-8 pt | 300+ | PDF, EPS | TIFF |

**When in doubt:** check the target journal's author guide; specs change and supplementary requirements may apply. Most Nature-family journals publish a "research figure guide" with worked examples.

---

## 5. Matplotlib Style Recipe

Copy-paste into `src/visualization/style.py` (or equivalent). Call `apply_paper_style()` once at the top of every figure-generating script.

```python
"""Global matplotlib style for publication figures.

Call ``apply_paper_style()`` once at the top of any figure-generating script
to enforce consistent font, DPI, and palette across all outputs.

Design choices:
- Sans-serif (Arial/Helvetica) at 7pt — fits top-journal column widths
- TrueType font embedding (pdf.fonttype=42) — required by most journals
- 600 DPI savefig for headroom over the 300 DPI minimum
- Top and right spines removed (Tufte: reduce chart junk)
- Okabe-Ito qualitative palette and viridis sequential (colorblind-safe)
"""
from __future__ import annotations

import matplotlib as mpl

# Okabe-Ito palette — 8 colorblind-safe qualitative colors.
OKABE_ITO: list[str] = [
    "#000000",  # black
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#009E73",  # bluish green
    "#F0E442",  # yellow
    "#0072B2",  # blue
    "#D55E00",  # vermilion
    "#CC79A7",  # reddish purple
]


def apply_paper_style() -> None:
    """Set global matplotlib rcParams for publication figures."""
    mpl.rcParams.update({
        "figure.dpi": 150,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
        "pdf.fonttype": 42,            # TrueType (required for submission)
        "ps.fonttype": 42,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "font.size": 7.0,
        "axes.titlesize": 8.0,
        "axes.labelsize": 7.5,
        "axes.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "xtick.major.size": 3.0,
        "ytick.major.size": 3.0,
        "legend.fontsize": 6.5,
        "legend.frameon": False,
        "lines.linewidth": 1.2,
        "lines.markersize": 4,
        "errorbar.capsize": 2.5,
        "image.cmap": "viridis",
    })
    mpl.rcParams["axes.prop_cycle"] = mpl.cycler(color=OKABE_ITO)
```

**Usage in a plotting script:**

```python
from src.visualization.style import apply_paper_style, OKABE_ITO
import matplotlib.pyplot as plt

apply_paper_style()

fig, ax = plt.subplots(figsize=(3.5, 2.5))  # width in inches, ~89mm single column
ax.bar(labels, values, color=OKABE_ITO[:len(labels)])
ax.set_xlabel("Model")
ax.set_ylabel("Accuracy")
fig.savefig("figures/fig_model_comparison.pdf")  # vector, TrueType, 600 DPI
```

---

## 6. Accessibility Tools

| Tool | Purpose | URL |
|---|---|---|
| Coblis | Online colorblind simulator — upload a figure, see 5 colorblind types | https://www.color-blindness.com/coblis-color-blindness-simulator/ |
| Color Oracle | Desktop colorblind simulator (live screen filter) — Mac/Win/Linux | https://colororacle.org |
| WebAIM Contrast Checker | Text-on-background contrast ratio (WCAG AA/AAA) | https://webaim.org/resources/contrastchecker/ |
| Viz Palette | Visualize palette with colorblind simulation | https://projects.susielu.com/viz-palette |
| Paletton | Palette generator with colorblind simulation | https://paletton.com |

**Testing workflow:**
1. Export the figure as PDF or PNG
2. Open in Coblis (web) or drag over Color Oracle (desktop)
3. Cycle through Deuteranopia, Protanopia, Tritanopia, Achromatopsia
4. Check that the argument still reads — are the categories still distinguishable?
5. If not, swap the palette (usually to Okabe-Ito or viridis) and re-export

---

## 7. Common Matplotlib Pitfalls

| Problem | Symptom | Fix |
|---|---|---|
| Type 3 fonts in PDF | Journal submission system rejects the PDF with a font-embedding error | Set `mpl.rcParams['pdf.fonttype'] = 42` at the top of the script |
| Bitmap output in a vector-looking file | PDF opens fine but axes/text are pixelated at 200% zoom | Always use `savefig('file.pdf')`, not `savefig('file.pdf', format='png')`. Do not use `rasterized=True` on text or axes |
| Tight layout clipping axis labels | Labels or legend get cut off in the final PDF | Use `bbox_inches='tight'` and `pad_inches=0.02` in `savefig` |
| DPI too low in raster output | TIFF looks pixelated at print size | `savefig(..., dpi=600)`. 600 gives headroom over the 300 minimum |
| Default rainbow cmap | Heatmap uses `viridis` (matplotlib ≥2.0 default) — fine; older versions default to `jet` | Explicitly set `cmap='viridis'` (or cividis/plasma/inferno). Never `jet` or `rainbow` |
| Axis spines not removed | Top and right spines visible by default | `ax.spines['top'].set_visible(False); ax.spines['right'].set_visible(False)` or set globally via `apply_paper_style()` |
| Default font is DejaVu Sans | Figures have an inconsistent look vs journal style | Set `font.family='sans-serif'` and `font.sans-serif=['Arial', 'Helvetica', 'DejaVu Sans']` (falls back if Arial not installed) |
| Panel labels using `fig.text` at arbitrary coordinates | Inconsistent panel label placement across figures | Use `ax.text(-0.1, 1.05, 'a', transform=ax.transAxes, fontweight='bold')` pattern in a helper function |
| Legend overlapping data | Legend inside the axes covers the line or bars | `ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), frameon=False)` — move legend outside the axes |
| Scientific notation on tick labels | `2.5e4` instead of `25000` on y-axis | `ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:g}'))` or use `ticklabel_format(style='plain')` |

---

## 8. Export Workflow

### Matplotlib (Python)

```python
fig.savefig('figures/fig_name.pdf', bbox_inches='tight', pad_inches=0.02)
# Optionally also save raster fallback:
fig.savefig('figures/fig_name.png', dpi=600, bbox_inches='tight', pad_inches=0.02)
```

### Seaborn (Python)

Seaborn wraps matplotlib; export via the underlying Figure object:

```python
import seaborn as sns
g = sns.relplot(data=df, x='x', y='y', hue='group')
g.figure.savefig('figures/fig_name.pdf', bbox_inches='tight', pad_inches=0.02)
```

### ggplot2 (R)

```r
library(ggplot2)
p <- ggplot(df, aes(x, y, color=group)) + geom_point() + theme_classic(base_size=7)
ggsave('figures/fig_name.pdf', p, width=89, height=60, units='mm', device=cairo_pdf)
```

Use `device=cairo_pdf` to ensure proper font embedding in R.

### Plotly (HTML/interactive)

Plotly is designed for HTML-interactive figures; journal submission requires static export. Use `write_image()` with the `kaleido` backend:

```python
import plotly.io as pio
fig.write_image('figures/fig_name.pdf', engine='kaleido', width=350, height=250)
```

However, for top-journal submissions, prefer matplotlib/seaborn/ggplot2 over Plotly — the static export from an interactive-first tool often has typography and styling quirks that require post-processing.

---

## 9. Tufte Principles (Brief)

Edward Tufte's *The Visual Display of Quantitative Information* (1983) introduced principles that still define good figures:

1. **Maximize the data-ink ratio**: every pixel should carry information. Remove gridlines, frames, 3D effects, textures, and decorative elements that don't advance the argument.
2. **Avoid chart junk**: no 3D bar/pie, no drop shadows, no gradient fills on categorical bars, no redundant legends when direct labeling works.
3. **Show data variation, not design variation**: use consistent conventions (same palette, same axis orientation, same chart type) across a set of figures.
4. **Use small multiples** for comparison: instead of overlaying 8 time series, show 8 small panels with the same axes. Readers compare panels faster than color-coded lines.
5. **Integrate text and graphics**: labels on lines (direct labeling) often beat a separate legend. Annotations attached to specific data points beat sidebar explanations.
6. **Above all else, show the data**: the figure exists to communicate data, not to look pretty. Aesthetics serve communication, not the other way around.

---

## 10. Further Reading

- Tufte, E. (1983). *The Visual Display of Quantitative Information*. Graphics Press.
- Wilke, C. O. (2019). *Fundamentals of Data Visualization*. O'Reilly. Free online: https://clauswilke.com/dataviz/
- Nature Research Figure Guide: https://research-figure-guide.nature.com
- Cell Press Figure Guidelines: https://www.cell.com/information-for-authors/figure-guidelines
- Seaborn color palettes: https://seaborn.pydata.org/tutorial/color_palettes.html
- ggpubfigs: https://github.com/JLSteenwyk/ggpubfigs — publication-ready ggplot2 themes
- ColorBrewer: https://colorbrewer2.org — curated palettes for sequential/diverging/qualitative
- Paul Tol's notes on colour schemes and templates: https://personal.sron.nl/~pault/
