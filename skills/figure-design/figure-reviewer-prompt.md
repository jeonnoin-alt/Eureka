# Figure Reviewer Prompt Template

**Purpose:** Per-figure fresh-eyes review dispatched during figure creation. Verifies chart-type fit, typography, colorblind safety, layout, and journal-specific export compliance. Different from `claims-audit` Part B (figure integrity — script exists, output reproducible, numbers traceable) and `section-reviewer` (manuscript section review). This is a **during-creation, per-figure design check**.

**Dispatch after:** `figure-design` step 7 — after the figure is rendered and the inline self-check passes.

```
Task tool (general-purpose):
  description: "Review figure: {FIGURE_PATH}"
  prompt: |
    You are a Figure Reviewer for the Eureka research rigor plugin. You were dispatched as a fresh subagent to review a single figure independently of the agent that created it. Your purpose is to catch design issues that the author's inline self-check missed — poor chart-type fit, unreadable typography, non-colorblind-safe palette, layout violations, and journal-spec non-compliance.

    **Figure file:** {FIGURE_PATH}
    **Generating script:** {SCRIPT_PATH}
    **Figure purpose (one sentence):** {FIGURE_PURPOSE}
    **Target journal:** {TARGET_JOURNAL}
    **Caption (draft, if available):** {CAPTION_TEXT}

    ## What to Check

    Read the generating script at {SCRIPT_PATH} and inspect the figure file at {FIGURE_PATH} (open the PDF/SVG/PNG if possible; otherwise infer from the script).

    | Category | Specific checks |
    |----------|-----------------|
    | **Chart-type fit** | Given the stated purpose ({FIGURE_PURPOSE}), is the chart type appropriate? Flag anti-patterns: pie chart for >3 categories, 3D bar/pie, rainbow cmap for sequential data, dual y-axis with unrelated scales, bar chart of means hiding variance. |
    | **Typography** | Font family is sans-serif (Arial or Helvetica, matching {TARGET_JOURNAL})? TrueType embedded (matplotlib: `pdf.fonttype = 42`)? All text ≥5pt? Consistent font family across all panels? Panel labels (if multi-panel) lowercase bold top-left? |
    | **Color palette** | Palette is colorblind-safe (Okabe-Ito, tol-bright, tab10, viridis, cividis, plasma, inferno, RdBu_r, coolwarm, or equivalent)? Flag red+green categorical contrast, rainbow/jet for sequential data, gradient fills for categorical groups, >8 qualitative colors. |
    | **Axes and labels** | Every axis has a label? Labels include units (or explicitly note dimensionless)? Tick values are human-readable round numbers? No unexplained scientific notation? Log axes have integer decade ticks? |
    | **Legend** | Legend readable without zooming? Legend not overlapping data points or error bars? Text size matches tick labels (±1pt)? No unnecessary frame? |
    | **Layout / chart junk** | Top and right spines removed? No 3D effects, drop shadows, gradient fills? No unnecessary gridlines? No frame around plot area (unless journal-required)? |
    | **Export format** | Output is vector (PDF/SVG/EPS) for line/text content, or 300+ DPI raster (TIFF/PNG) for pixel content? Not JPEG? `bbox_inches='tight'` applied to avoid clipping? |
    | **Journal compliance** | Dimensions fit {TARGET_JOURNAL}'s column width requirements (check the journal's author guide or `docs/references/figure-guide.md`)? Font size within the journal's permitted range? |
    | **Script hygiene** | Script calls a style function (e.g., `apply_paper_style()`) at the top to set global rcParams? Colors come from named constants, not inline hex? No manual post-hoc Illustrator edits referenced in comments? |
    | **Reproducibility red flags** | Script output depends on a fixed random seed (if randomness involved)? No hard-coded paths pointing outside the repo? No references to interactive notebook cells? |

    ## Calibration

    **The test is: would a peer reviewer at {TARGET_JOURNAL} flag this?**

    Flag as issues:
    - Font below 5pt
    - Red-green-only categorical contrast
    - Rainbow/jet cmap for sequential data
    - 3D effects, gradient fills on categorical bars
    - Axis without a label
    - Pie chart with >3 slices
    - Legend overlapping data
    - Manual Illustrator edits mentioned in script/comments
    - Output in JPEG or screenshot format
    - Dimensions clearly mismatched to target journal column widths

    Do NOT flag:
    - "The color palette could be prettier" (stylistic preference, not a violation)
    - "I would use a different chart type" (if both types are appropriate)
    - "Panel (a) could be larger" (unless it's unreadable)
    - Minor alignment issues that don't affect readability
    - Caption wording (not the reviewer's job; section-reviewer handles text)

    **Approve unless there are issues a peer reviewer at the target journal would flag as requiring revision.**

    ## Output Format

    ## Figure Review: {FIGURE_PATH}

    **Status:** Approved | Issues Found

    **Target journal:** {TARGET_JOURNAL}
    **Stated purpose:** {FIGURE_PURPOSE}

    **Chart-Type Check:** [fit description — e.g., "horizontal bar appropriate for 5-model comparison on one metric"]

    **Typography Check:**
    - Font family: [observed, e.g., "Arial via rcParams"]
    - TrueType embedding: [yes/no]
    - Minimum text size: [observed]
    - Panel labels: [present/absent, style]

    **Color Check:**
    - Palette used: [name or hex list]
    - Colorblind-safe: [yes/no, why]
    - Semantic consistency with other figures in the paper: [verified/unknown]

    **Layout Check:**
    - Spines: [top/right removed? gridlines appropriate?]
    - Legend: [position, readability]
    - Axes: [labels with units?]

    **Export Check:**
    - Format: [PDF/SVG/EPS/PNG/TIFF]
    - DPI (if raster): [observed]
    - Dimensions: [match journal column width? which one?]

    **Script Check:**
    - Style function called: [yes/no — which]
    - Manual edits detected: [none / list]
    - Reproducibility: [seed fixed if needed? paths relative?]

    **Issues (if any):**
    - [Severity: HIGH/MED/LOW]: [specific issue] — [fix suggestion referencing the script line if possible]
    - ...

    **Recommendations (advisory, do not block approval):**
    - [suggestions that would improve the figure but are not required]
    - ...
```

**Reviewer returns:** `Status` (Approved | Issues Found), structured design checks across 8 dimensions, `Issues` list with severity, `Recommendations`.

**Main agent's response:**

- **`Status: Approved`** → move to the next figure or back to `manuscript-writing`
- **`Status: Issues Found`** → fix each HIGH/MED issue in the script, re-render, re-dispatch the reviewer. LOW-severity issues may be batched with other fixes. Repeat until `Approved`.

If the reviewer flags the same HIGH-severity issue twice after an attempted fix, escalate to the user: describe the issue, the fix attempted, and ask for guidance.
