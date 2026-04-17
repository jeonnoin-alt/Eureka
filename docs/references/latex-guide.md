# LaTeX Guide

This is a reference document, not a skill. It provides LaTeX conventions for research manuscript writing — `main.tex` structure, section file organization, BibTeX key format, citation commands, math notation, figure/table commands, abbreviation rules, and the compile workflow. Referenced by `eureka:manuscript-writing` when the user's chosen format is LaTeX.

---

## 1. When to Use LaTeX vs. Alternatives

**Use LaTeX when:**

- Targeting a top-tier STEM journal (Nature family, Science family, Cell family, Brain, NeuroImage, JAMA, IEEE Transactions, etc.) — nearly all accept LaTeX submissions, and several *require* LaTeX for math-heavy papers
- Your paper contains equations, derivations, or structured algorithms
- Bibliography management matters (BibTeX is the de facto standard in STEM)
- You want fine-grained control over figure placement, table structure, and cross-references
- Reproducibility of the manuscript itself is important (the `.tex` + `.bib` source is portable across decades)

**Use Markdown when:**

- Your workflow is preprint-first or blog-style (arXiv, bioRxiv, a personal site)
- Math content is minimal
- Target venue accepts Markdown directly or you convert with pandoc at submission
- Collaborators prefer text over compile-to-PDF iteration

**Use Word (via pandoc) when:**

- A collaborator or journal template mandates it
- The submission system requires a `.docx` upload and pandoc round-tripping is acceptable

---

## 2. Recommended `main.tex` Structure

A standard preamble for research papers, covering the most common needs:

```latex
\documentclass[11pt]{article}

% === Core packages ===
\usepackage[utf8]{inputenc}            % input encoding
\usepackage[T1]{fontenc}               % output font encoding
\usepackage{amsmath,amssymb,amsfonts}  % math
\usepackage{graphicx}                  % figures
\usepackage{subcaption}                % subfigures
\usepackage{booktabs}                  % professional tables
\usepackage{natbib}                    % author-year citations
\usepackage{hyperref}                  % clickable links (load last among core)
\usepackage{xcolor}                    % colored text
\usepackage[margin=1in]{geometry}      % page margins

% === Optional packages ===
% \usepackage{algorithm}               % algorithm environments
% \usepackage{algorithmic}             % algorithm pseudocode
% \usepackage{siunitx}                 % units and numbers
% \usepackage{cleveref}                % smart cross-references

% === Custom commands (keep minimal) ===
\newcommand{\ie}{\textit{i.e.}}
\newcommand{\eg}{\textit{e.g.}}
\newcommand{\etal}{\textit{et al.}}

% === Document ===
\begin{document}

\title{Your Paper Title in Sentence Case}
\author{Author One\thanks{Affiliation 1} \and Author Two\thanks{Affiliation 2}}
\date{}
\maketitle

\begin{abstract}
  \input{sections/abstract}
\end{abstract}

\input{sections/01-introduction}
\input{sections/02-related-work}
\input{sections/03-method}
\input{sections/04-experiments}
\input{sections/05-discussion}
\input{sections/06-conclusion}

\bibliographystyle{apalike}
\bibliography{references}

\end{document}
```

**Notes:**

- `\input{sections/...}` (no extension) keeps per-section files small and version-controllable.
- `hyperref` should be loaded last among core packages (it redefines many internals).
- `natbib` with `\bibliographystyle{apalike}` gives author-year in-text citations pre-submission; convert to the target journal's style at submission time.
- `geometry` defaults to 1-inch margins; journals often provide their own class file that overrides this — strip `\usepackage[margin=1in]{geometry}` when switching to the journal template.

---

## 3. Section File Organization

Recommended layout:

```
paper/
├── main.tex
├── references.bib
├── figures/
│   ├── fig1_overview.pdf
│   ├── fig2_results.pdf
│   └── ...
└── sections/
    ├── abstract.tex               (written last, no number prefix)
    ├── 01-introduction.tex
    ├── 02-related-work.tex        (or 02-background.tex)
    ├── 03-method.tex
    ├── 04-experiments.tex         (or 04-results.tex)
    ├── 05-discussion.tex
    └── 06-conclusion.tex
```

**Naming rules:**

- Numeric prefix (`01-`, `02-`, ...) enforces ordering in file listings and matches the reading order.
- Kebab-case for readability.
- Abstract is written last — no number prefix, to reflect that it summarizes the finished work rather than leading it.

**Why split:**

- Each section is a small, focused file → easier `git diff` review during writing.
- Matches the per-section workflow of `eureka:manuscript-writing`: write one section, dispatch `section-reviewer`, fix, commit, move on.
- Enables parallel work (co-authors editing different sections without merge conflicts).
- Sections can be reused or restructured (e.g., swapping "Related Work" and "Background" framings) by changing `\input{}` lines in `main.tex`.

---

## 4. BibTeX Conventions

### Key format

- `FirstAuthorLastNameYear` (e.g., `Smith2024`, `Jones2018`).
- Start with uppercase letter (pure convention; improves grep-ability).
- Disambiguation suffix: `Jones2018a`, `Jones2018b` when the same first author has multiple papers in the same year.

### Required fields

- **`author`**: full names, separated by ` and ` (case-sensitive `and`).
- **`title`**: full title in sentence case (journal style will be applied at conversion).
- **`journal`** (or `booktitle` for conferences): spell out the full name; let the bibliography style abbreviate if needed.
- **`year`**: four digits.
- **`doi`**: **mandatory** — enables automatic journal-style formatting and helps reviewers find the paper. Format: `10.xxxx/yyyyy` (no URL prefix).
- **`volume`**, **`pages`**: when available.

### Sample entry

```bibtex
@article{Smith2024,
  author  = {Smith, Jane A. and Doe, John B. and others},
  title   = {Full paper title in sentence case},
  journal = {Journal of Example Research},
  year    = {2024},
  volume  = {42},
  pages   = {123--145},
  doi     = {10.xxxx/yyyyy}
}
```

### Additional rules

- **Preprints** (bioRxiv, medRxiv, arXiv): cite these only when the published version does not yet exist. Replace with the published entry as soon as available.
- **URLs**: do not include a `url` field when `doi` is present — the DOI already resolves.
- **Book chapters**: use `@incollection` with `booktitle`, `editor`, `publisher`, `address`, `pages`.
- **Dissertations**: `@phdthesis` with `school` and `year`.
- **Conference papers**: `@inproceedings` with `booktitle`, `pages`.

---

## 5. Citation Commands (natbib)

| Command | Renders as | Use for |
|---|---|---|
| `\citep{key}` | (Author et al., Year) | Parenthetical citation within a sentence |
| `\citet{key}` | Author et al. (Year) | Citation as the subject of the sentence |
| `\citep[see][]{key}` | (see Author et al., Year) | Parenthetical with prefix |
| `\citep[p.~45]{key}` | (Author et al., Year, p. 45) | Citation with page number |
| `\citep{k1, k2, k3}` | (Author1 et al., Year; Author2 et al., Year; ...) | Multiple parenthetical |
| `\citeauthor{key}` | Author et al. | Author only |
| `\citeyear{key}` | Year | Year only |

### Citation density guidelines

- One specific citation per factual claim (do not lazy-cite the same review paper repeatedly).
- Avoid more than 5 consecutive citations in a single parenthetical — distribute across sentences so each citation supports a specific statement.
- Cite the **original source**, not the highest-citation review that mentions it, when possible.

---

## 6. Math Notation Conventions

| Concept | Typographic convention | LaTeX |
|---|---|---|
| Vector | Bold lowercase | `\mathbf{x}` |
| Matrix | Bold uppercase | `\mathbf{A}` |
| Scalar | Italic lowercase | `x` |
| Set | Blackboard bold | `\mathbb{R}`, `\mathbb{N}` |
| Operator/space | Calligraphic | `\mathcal{L}`, `\mathcal{F}` |
| Random variable | Italic uppercase | `X`, `Y` |
| Probability | `\Pr` or `\mathbb{P}` | `\Pr(X = x)` |

### Rules

- **Define every variable on first appearance.** A reader seeing `\alpha` for the first time should immediately see "where `\alpha` is the diffusion rate constant."
- **Equation numbering is sequential.** Use `\begin{equation}...\end{equation}` for numbered equations, `\begin{align}...\end{align}` for multi-line numbered equations (one number per line by default), or `\begin{align*}` for unnumbered.
- **Label equations you reference**: `\begin{equation}\label{eq:diffusion} ... \end{equation}`, then reference with `\ref{eq:diffusion}` or `\autoref{eq:diffusion}`.
- **Consistent notation across sections**: if you use `\mathbf{x}` for input in the Method section, the Results section must also use `\mathbf{x}`.
- **Spacing**: use `\,` for thin space (e.g., before units), `\quad` for larger gaps, never raw spaces in math mode.

---

## 7. Figure and Table Conventions

### Figures

```latex
\begin{figure}[t]
  \centering
  \includegraphics[width=\linewidth]{figures/fig1_overview.pdf}
  \caption{Overview of the method. (a) Input. (b) Processing. (c) Output.}
  \label{fig:overview}
\end{figure}
```

- **Use PDF for vector content** (diagrams, plots from matplotlib's `pdf` backend) — scales without quality loss.
- **Use PNG for raster content** (photographs, microscopy) — avoid JPEG for scientific figures (compression artifacts).
- **Always** include `\caption{...}` and `\label{fig:X}`. Reference with `\ref{fig:X}` or `\autoref{fig:X}` (with `cleveref` or `hyperref`'s autoref).
- **Minimum resolution**: 300 DPI for raster; PDF for anything line-based.
- **Colorblind-safe palette**: viridis, cividis, plasma, or manually-chosen palettes passing Coblis simulation.
- **Figures must be script-generated** — this is enforced by `eureka:claims-audit` (Part B: Figure Integrity). Keep the generating script in the repo and reference it in the figure caption or a `README.md` in `figures/`.

### Subfigures

```latex
\begin{figure}[t]
  \centering
  \begin{subfigure}[b]{0.48\linewidth}
    \includegraphics[width=\linewidth]{figures/fig1a.pdf}
    \caption{Panel A caption.}
    \label{fig:overview:a}
  \end{subfigure}
  \hfill
  \begin{subfigure}[b]{0.48\linewidth}
    \includegraphics[width=\linewidth]{figures/fig1b.pdf}
    \caption{Panel B caption.}
    \label{fig:overview:b}
  \end{subfigure}
  \caption{Overall caption describing the figure.}
  \label{fig:overview}
\end{figure}
```

### Tables

```latex
\begin{table}[t]
  \centering
  \caption{Model comparison on held-out test set.}
  \label{tab:results}
  \begin{tabular}{@{}lccc@{}}
    \toprule
    Model & Accuracy & Precision & Recall \\
    \midrule
    Baseline A & 0.72 & 0.70 & 0.75 \\
    Baseline B & 0.79 & 0.78 & 0.80 \\
    Our model  & \textbf{0.86} & \textbf{0.85} & \textbf{0.87} \\
    \bottomrule
  \end{tabular}
\end{table}
```

- **Use `booktabs`**: `\toprule`, `\midrule`, `\bottomrule`. Never use `\hline` or vertical rules — standard practice in professional typography.
- **Column alignment**: `l` (left), `c` (center), `r` (right). First column is usually `l` (category labels), numeric columns usually `c` or `r`.
- **`@{}` at start and end** removes the default padding at the table edges — cleaner appearance.
- **Best result bolded** with `\textbf{...}` for quick visual identification.
- **Caption above** the table (standard journal style), but place `\caption{}` above `\begin{tabular}` — LaTeX handles positioning regardless of source order.

---

## 8. Abbreviation Rules

- **Spell out on first use in the Abstract**, then use the abbreviation for the rest of the Abstract.
- **Spell out again on first use in the main text** (the Abstract and main body are read independently; the first occurrence in the body must define the abbreviation even if the Abstract already did).
- **Figure/table captions define abbreviations independently** if the abbreviation appears only in the caption or the caption is the first use.
- **Universally-known abbreviations do not need expansion**: MRI, CT, DNA, RNA, PET, EEG, fMRI, API, HTTP, CPU, GPU, AI, ML.
- **Three-letter acronyms benefit from disambiguation**: "MS" is multiple sclerosis in a medical paper but Microsoft in a software paper — clarify at first use regardless of domain.

Example:

> **Abstract:** We trained a graph neural network (GNN) on a cohort of 500 subjects... The GNN achieved...
>
> **Introduction (first line):** We propose a graph neural network (GNN) approach to...

---

## 9. LaTeX Compile Workflow

### Manual compile cycle

```bash
pdflatex main.tex    # first pass: generates .aux files
bibtex main          # processes the .bib, generates .bbl
pdflatex main.tex    # second pass: embeds bibliography
pdflatex main.tex    # third pass: resolves cross-references
```

### Automated (recommended)

```bash
latexmk -pdf main.tex
```

`latexmk` runs the necessary passes automatically and rebuilds only what changed.

### Clean build artifacts

```bash
latexmk -c           # removes .aux, .log, .bbl, etc. (keeps PDF)
latexmk -C           # removes everything including PDF
```

### Git hygiene — `.gitignore`

Commit:
- `main.tex`, `sections/*.tex`, `abstract.tex`
- `references.bib`
- `figures/*.pdf`, `figures/*.png`
- Scripts that generate figures (`figures/scripts/*.py`, etc.)

Ignore:
- `main.aux`, `main.log`, `main.out`, `main.toc`, `main.bbl`, `main.blg`, `main.synctex.gz`
- `sections/*.aux`
- `*.fls`, `*.fdb_latexmk`

Optional (preference-dependent):
- `main.pdf` — committing the built PDF helps collaborators who don't have a TeX distribution, but adds binary churn to git. Many teams commit the final submission PDF only.

---

## 10. Section-Specific LaTeX Patterns

### Introduction — contribution list

```latex
Our contributions are:
\begin{enumerate}
  \item We propose ...
  \item We demonstrate ...
  \item We release ...
\end{enumerate}
```

### Method — numbered equations

```latex
The diffusion process is defined as
\begin{equation}
  \frac{d\mathbf{c}}{dt} = -\beta \mathbf{L} \mathbf{c},
  \label{eq:diffusion}
\end{equation}
where $\mathbf{c}$ is the concentration vector, $\mathbf{L}$ is the graph Laplacian, and $\beta$ is the diffusion rate.
```

### Method — multi-step derivations

```latex
\begin{align}
  f(x) &= x^2 + 2x + 1 \label{eq:step1} \\
       &= (x + 1)^2.   \label{eq:step2}
\end{align}
```

### Method — algorithms

```latex
\begin{algorithm}
\caption{Gradient descent on $f$}
\label{alg:gd}
\begin{algorithmic}[1]
  \REQUIRE initial $x_0$, learning rate $\eta$, tolerance $\epsilon$
  \STATE $x \gets x_0$
  \WHILE{$\|\nabla f(x)\| > \epsilon$}
    \STATE $x \gets x - \eta \nabla f(x)$
  \ENDWHILE
  \RETURN $x$
\end{algorithmic}
\end{algorithm}
```

### Results — limitations bullet list (in Discussion)

```latex
Our approach has several limitations:
\begin{itemize}
  \item Sample size limits statistical power for subgroup analyses.
  \item The method assumes stationary dynamics; time-varying behavior is out of scope.
  \item ...
\end{itemize}
```

---

## 11. Common Mistakes to Avoid

| Mistake | Fix |
|---|---|
| `\label{}` before `\caption{}` in figure/table environments | Place `\label{}` **after** `\caption{}` — otherwise the label points to the wrong counter |
| Using `$$...$$` for display math | Use `\[...\]` or `\begin{equation}...\end{equation}` — `$$...$$` is deprecated and handles spacing incorrectly |
| Manually adjusting figure placement with `[h]` everywhere | Use `[t]` (top) or `[tbp]` and trust LaTeX — float placement obsession wastes time |
| Forgetting `\usepackage{hyperref}` | Without it, `\ref{}` produces dead text. Load `hyperref` last among core packages |
| Bold math with `\textbf{$x$}` | Use `\boldsymbol{x}` or `\mathbf{x}` — `\textbf` around math breaks the rendering |
| Quotation marks as `"..."` | Use `` ``...'' `` (backticks for open, apostrophes for close) or `\enquote{...}` with `csquotes` |
| Citations appearing as `[?]` | Run `bibtex main` after the first `pdflatex`, then two more `pdflatex` passes |
| `fig:1`, `fig:2` label names | Use descriptive labels (`fig:overview`, `fig:results-accuracy`) — numeric labels break when figures are reordered |

---

## 12. Converting to Journal-Specific Style at Submission

Most journals provide a `.cls` file or `.sty` file. The typical conversion:

1. Replace `\documentclass{article}` with the journal's class (e.g., `\documentclass{nature}`, `\documentclass{elsarticle}`).
2. Remove the `geometry` package if the class handles margins.
3. Replace `\bibliographystyle{apalike}` with the journal's style (e.g., `naturemag`, `elsarticle-num`).
4. Rename `\cite{}` commands if the class uses a different citation package.
5. Verify the PDF with `latexmk -pdf main.tex` and manually check the title page, section numbering, and bibliography format.

Keep the generic (apalike / natbib) version in a `pre-submission/` branch for continued writing; apply journal-specific changes in a separate branch just before upload.

---

## 13. Further Reading

- `The Not So Short Introduction to LaTeX2e` (lshort) — free online, excellent starting reference
- `The LaTeX Companion` (Mittelbach et al.) — comprehensive desk reference
- `biblatex` package — modern alternative to `natbib`, more flexible BibTeX processing (worth considering for new projects)
- `pandoc` — for Markdown ↔ LaTeX ↔ Word conversions
