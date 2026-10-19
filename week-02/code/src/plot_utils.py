"""
opt_plots.py -- plotting and sanity-check utilities for the optimization assignments
(week 1 corrections: GD + Armijo on Rosenbrock; week 3: Newton vs gradient descent).

You run the algorithms. You record the iterates (and, if you have them, step sizes etc.).
You hand the records to these functions. Nothing here runs an optimizer.

Quick start
-----------
    from opt_plots import make_run, plot_convergence, plot_rosenbrock_paths, summary_table

    run = make_run(
        "GD + Armijo",                  # method name: shown in legends, also fixes the colour
        xs,                             # list/array of iterates INCLUDING the start x0, shape (K+1, d)
        f=f, grad=grad_f,               # or pass fs=..., gnorms=... that you already logged
        alphas=alphas,                  # accepted step sizes, length K (optional)
        tol=1e-6, max_iter=200_000,     # the stopping rule you actually used
        meta={"beta": 1e-4, "p": 0.5},  # anything you want listed in the table (optional)
    )
    plot_convergence([run_gd, run_newton])         # gradient norm vs iteration, log y
    plot_rosenbrock_paths(runs)                    # one panel per start point
    summary_table(runs)                            # DataFrame with an explicit convergence column

Design notes (what these functions guard against)
-------------------------------------------------
* Labels come from the data. Every legend entry is built from the run itself (iteration count,
  converged or not), so a legend cannot disagree with the code that produced the curve.
* Methods are compared at the same tolerance. Multi-run plots raise ValueError if tolerances
  differ (override with allow_mixed_tol=True; then each tolerance is drawn and the title says so).
* Gradient-norm plots use a log y-axis, all methods on the same axes, with the tolerance line.
* Runs that hit the iteration cap, stall or diverge are marked (x marker and legend text),
  never drawn as if they had converged.
* Colour identifies the METHOD (by name, in first-seen order, or your `color_order`), so the same
  method keeps its colour across panels and figures. Line style and marker also differ per method,
  so figures survive greyscale printing and colour-blindness.
* Every function returns None after displaying (show=True) or returns the Figure (show=False),
  so a notebook never shows a figure twice. save="name.png" writes a 200-dpi PNG.

Requirements: numpy, matplotlib, pandas.
"""
from __future__ import annotations

import math
import warnings
from dataclasses import dataclass, field, replace
from typing import Callable, Dict, Iterable, List, Optional, Sequence

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.ticker import FuncFormatter, MaxNLocator, LogFormatterSciNotation

__all__ = [
    "OptRun", "make_run", "check_run", "check_runs", "summary_table",
    "plot_convergence", "plot_convergence_panel", "plot_step_sizes",
    "plot_condition_numbers", "plot_descent_check", "plot_shifts",
    "plot_rosenbrock_paths", "plot_kappa_scaling", "rosenbrock_xy",
]

# --------------------------------------------------------------------------------------
# Style: reference categorical palette (first three slots validated for all-pairs colour-blind
# separation), recessive hairline grid, white background, text in ink colours not series colours.
# --------------------------------------------------------------------------------------
_SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
_LINESTYLES = ["-", (0, (6, 2)), (0, (1, 1.5)), (0, (4, 1.5, 1, 1.5))]
_MARKERS = ["o", "s", "^", "D", "v", "P", "X", "*"]
_INK, _INK2, _GRID, _SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#ffffff"

_RC = {
    "figure.facecolor": _SURFACE, "axes.facecolor": _SURFACE, "savefig.facecolor": _SURFACE,
    "axes.edgecolor": "#b9b8b2", "axes.linewidth": 0.8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": _GRID, "grid.linewidth": 0.6, "grid.linestyle": "-",
    "axes.axisbelow": True,
    "text.color": _INK, "axes.labelcolor": _INK2, "xtick.color": _INK2, "ytick.color": _INK2,
    "axes.titlesize": 12, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.labelsize": 10.5, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "legend.frameon": False, "legend.fontsize": 9.5,
    "figure.dpi": 110, "savefig.dpi": 200, "font.size": 10,
    "lines.solid_capstyle": "round",
}


def _styled(fn):
    """Apply the module style only while this function runs (no global side effects)."""
    def wrapper(*args, **kwargs):
        with plt.rc_context(_RC):
            return fn(*args, **kwargs)
    wrapper.__name__, wrapper.__doc__ = fn.__name__, fn.__doc__
    return wrapper


# --------------------------------------------------------------------------------------
# Data container
# --------------------------------------------------------------------------------------
@dataclass
class OptRun:
    """One optimization run. Build it with make_run(); do not fill it by hand."""
    name: str
    xs: np.ndarray                       # (K+1, d) iterates, xs[0] = starting point
    fs: np.ndarray                       # (K+1,)   f(x_k)
    gnorms: np.ndarray                   # (K+1,)   ||grad f(x_k)||
    tol: float
    max_iter: Optional[int] = None
    converged: bool = False
    status: str = ""
    diverged: bool = False
    alphas: Optional[np.ndarray] = None          # (K,) accepted step sizes
    cond_numbers: Optional[np.ndarray] = None    # condition number of the Hessian at x_k
    shifts: Optional[np.ndarray] = None          # (K,) diagonal shift lambda used (0 = none)
    dirderivs: Optional[np.ndarray] = None       # (K,) g_k . d_k, before any safeguard
    meta: Dict[str, object] = field(default_factory=dict)
    runtime_s: Optional[float] = None

    @property
    def iterations(self) -> int:
        return len(self.xs) - 1

    @property
    def start(self) -> tuple:
        return tuple(float(v) for v in self.xs[0])

    def step_rule(self) -> str:
        """Describe the step-size rule from the data itself."""
        if self.alphas is None or len(self.alphas) == 0:
            return "not recorded"
        a = self.alphas
        if np.allclose(a, a[0], rtol=0, atol=0):
            return f"fixed alpha = {a[0]:g}"
        return f"backtracking (alpha in [{a.min():.3g}, {a.max():.3g}])"

    def label(self) -> str:
        """Legend text built from the run's own data."""
        k = f"{self.iterations:,} it."
        if self.converged:
            tail = k
        else:
            tail = f"{k}, did not converge ({self.status_short()})"
        return f"{self.name} ({tail})"

    def status_short(self) -> str:
        s = self.status or ("converged" if self.converged else "stopped")
        return s


def _fmt_point(p) -> str:
    return "(" + ", ".join(f"{v:g}" for v in p) + ")"


def _as_2d(xs) -> np.ndarray:
    arr = np.asarray([np.atleast_1d(np.asarray(x, dtype=float)) for x in xs], dtype=float)
    if arr.ndim != 2:
        raise ValueError(f"xs must be a sequence of vectors (K+1, d); got shape {arr.shape}.")
    return arr


def make_run(name: str, xs, *, tol: float, f: Optional[Callable] = None,
             grad: Optional[Callable] = None, fs=None, gnorms=None, alphas=None,
             max_iter: Optional[int] = None, converged: Optional[bool] = None,
             status: Optional[str] = None, cond_numbers=None, shifts=None, dirderivs=None,
             meta: Optional[dict] = None, runtime_s: Optional[float] = None) -> OptRun:
    """
    Package one run for plotting.

    name       method name, e.g. "GD + Armijo", "Newton (plain)", "Newton (safeguarded)".
    xs         iterates including the start point: xs[0] = x0, ..., xs[K] = final point.
    tol        the gradient-norm tolerance you used to stop. Required on purpose.
    f, grad    functions of one vector; used to compute fs / gnorms when you did not log them.
    fs, gnorms values at every iterate (length K+1). Give these OR f and grad.
    alphas     accepted step size at each iteration (length K).
    max_iter   iteration cap you used (lets the table say "iteration cap").
    converged  default: final gradient norm <= tol.
    status     optional text for non-convergence: "stalled", "line search failed", ...
    cond_numbers  condition number of the Hessian at each iterate (length K or K+1).
    shifts     diagonal shift lambda used at each iteration (length K, 0 when no shift).
    dirderivs  g_k . d_k at each iteration (length K), recorded BEFORE any fallback.
    meta       dict of hyperparameters to list in summary_table (beta, p, ...).
    """
    X = _as_2d(xs)
    K = len(X) - 1
    if K < 0:
        raise ValueError("xs is empty. Include at least the starting point.")

    def vec(v, n, what):
        if v is None:
            return None
        v = np.asarray(v, dtype=float).ravel()
        if len(v) != n:
            hint = ""
            if what in ("fs", "gnorms") and len(v) == n - 1:
                hint = " (did you forget to record iteration 0, the starting point?)"
            raise ValueError(f"{what} has length {len(v)} but {n} was expected{hint}.")
        return v

    if fs is None:
        if f is None:
            raise ValueError("Provide either fs (values at each iterate) or f (a function to compute them).")
        fs = [f(x) for x in X]
    if gnorms is None:
        if grad is None:
            raise ValueError("Provide either gnorms (gradient norms at each iterate) or grad.")
        gnorms = [np.linalg.norm(np.asarray(grad(x), dtype=float)) for x in X]
    fs = vec(fs, K + 1, "fs")
    gnorms = vec(gnorms, K + 1, "gnorms")
    alphas = vec(alphas, K, "alphas")
    dirderivs = vec(dirderivs, K, "dirderivs")
    shifts = vec(shifts, K, "shifts")
    if cond_numbers is not None:
        cond_numbers = np.asarray(cond_numbers, dtype=float).ravel()
        if len(cond_numbers) not in (K, K + 1):
            raise ValueError(f"cond_numbers has length {len(cond_numbers)}; expected {K} or {K + 1}.")

    # Truncate at the first non-finite value (a diverged run), and say so.
    bad = ~(np.isfinite(X).all(axis=1) & np.isfinite(fs) & np.isfinite(gnorms))
    diverged = bool(bad.any())
    if diverged:
        i = int(np.argmax(bad))
        if i == 0:
            raise ValueError("The starting point itself gives a non-finite value of f or its gradient.")
        K = i - 1
        X, fs, gnorms = X[:i], fs[:i], gnorms[:i]
        alphas = None if alphas is None else alphas[:K]
        dirderivs = None if dirderivs is None else dirderivs[:K]
        shifts = None if shifts is None else shifts[:K]
        if cond_numbers is not None:
            cond_numbers = cond_numbers[:i]

    if converged is None:
        converged = bool(gnorms[-1] <= tol) and not diverged
    if status is None:
        if converged:
            status = "converged"
        elif diverged:
            status = "diverged"
        elif max_iter is not None and K >= max_iter:
            status = "iteration cap"
        else:
            status = "stopped early"
    return OptRun(name=name, xs=X, fs=fs, gnorms=gnorms, tol=float(tol), max_iter=max_iter,
                  converged=bool(converged), status=status, diverged=diverged, alphas=alphas,
                  cond_numbers=cond_numbers, shifts=shifts, dirderivs=dirderivs,
                  meta=dict(meta or {}), runtime_s=runtime_s)


# --------------------------------------------------------------------------------------
# Sanity checks (the things a reviewer would otherwise find)
# --------------------------------------------------------------------------------------
def check_run(run: OptRun) -> List[str]:
    """Return a list of human-readable problems with one run (empty list = clean)."""
    out = []
    scale = np.maximum(1.0, np.abs(run.fs[:-1]))
    up = run.fs[1:] - run.fs[:-1] > 1e-10 * scale
    if up.any() and run.alphas is not None and not np.allclose(run.alphas, run.alphas[0]):
        out.append(f"{run.name}: f increased at {int(up.sum())} of {run.iterations} iterations; "
                   "an Armijo line search with a descent direction should never allow that. "
                   "Check the direction (is g.d < 0?) and the line-search condition.")
    if run.converged and run.gnorms[-1] > run.tol:
        out.append(f"{run.name}: marked converged but the final gradient norm {run.gnorms[-1]:.3g} "
                   f"exceeds the tolerance {run.tol:g}.")
    if (not run.converged) and run.gnorms[-1] <= run.tol:
        out.append(f"{run.name}: marked NOT converged but the final gradient norm "
                   f"{run.gnorms[-1]:.3g} is within the tolerance {run.tol:g}.")
    if run.alphas is not None and len(run.alphas):
        if (run.alphas <= 0).any() or (run.alphas > 1 + 1e-12).any():
            out.append(f"{run.name}: accepted step sizes outside (0, 1]; backtracking starts at 1.")
    if run.max_iter is not None and run.iterations > run.max_iter:
        out.append(f"{run.name}: {run.iterations} iterations recorded but max_iter={run.max_iter}.")
    if run.dirderivs is not None and run.status == "converged" and (run.dirderivs >= 0).any():
        out.append(f"{run.name}: some recorded g.d are >= 0; make sure those steps used a fallback "
                   "direction before the line search.")
    return out


def check_runs(runs: Sequence[OptRun], require_same_tol: bool = True) -> List[str]:
    """Problems across a set of runs, including comparing at different tolerances."""
    out = []
    for r in runs:
        out += check_run(r)
    tols = sorted({r.tol for r in runs})
    if require_same_tol and len(tols) > 1:
        out.append("Runs use different tolerances (" + ", ".join(f"{t:g}" for t in tols) +
                   "). Compare methods at the same tolerance, or pass allow_mixed_tol=True.")
    return out


def _prepare(runs, allow_mixed_tol=False, disambiguate=True) -> List[OptRun]:
    runs = list(runs)
    if not runs:
        raise ValueError("No runs given.")
    for r in runs:
        if not isinstance(r, OptRun):
            raise TypeError("Pass the objects returned by make_run(...).")
    tols = {r.tol for r in runs}
    if len(tols) > 1 and not allow_mixed_tol:
        raise ValueError("Runs use different tolerances (" + ", ".join(f"{t:g}" for t in sorted(tols)) +
                         "). Rerun with the same tolerance so iteration counts are comparable, "
                         "or pass allow_mixed_tol=True.")
    seen = set()
    for r in runs:
        key = (r.name, r.start)
        if key in seen:
            raise ValueError(f"Two runs share the name {r.name!r} and start {_fmt_point(r.start)}; "
                             "give them different names.")
        seen.add(key)
    for r in runs:
        for msg in check_run(r):
            warnings.warn(msg, stacklevel=3)
    if disambiguate:
        # same method from several starts: each curve gets its own name (and colour) in line plots
        counts: Dict[str, int] = {}
        for r in runs:
            counts[r.name] = counts.get(r.name, 0) + 1
        runs = [replace(r, name=f"{r.name} from {_fmt_point(r.start)}") if counts[r.name] > 1 else r
                for r in runs]
    return runs


def _tol_note(runs) -> str:
    tols = sorted({r.tol for r in runs})
    if len(tols) == 1:
        return f"Stopping rule: ||grad f|| <= {tols[0]:g}"
    return "Mixed tolerances: " + ", ".join(f"{t:g}" for t in tols)


# --------------------------------------------------------------------------------------
# Table
# --------------------------------------------------------------------------------------
def summary_table(runs: Sequence[OptRun]):
    """One row per run. The 'Converged' column says "yes" or "NO (...)" so a failure cannot hide."""
    import pandas as pd
    rows = []
    for r in runs:
        row = {
            "Method": r.name,
            "Start": _fmt_point(r.start),
            "Iterations": r.iterations,
            "Converged": "yes" if r.converged else f"NO ({r.status})",
            "Final f": float(r.fs[-1]),
            "Final ||grad||": float(r.gnorms[-1]),
            "Tolerance": r.tol,
            "Step rule": r.step_rule(),
        }
        if r.max_iter is not None:
            row["Iteration cap"] = r.max_iter
        if r.shifts is not None:
            row["Iterations shifted"] = int((r.shifts > 0).sum())
        if r.dirderivs is not None:
            row["Non-descent steps (g.d >= 0)"] = int((r.dirderivs >= 0).sum())
        if r.runtime_s is not None:
            row["Time (s)"] = round(r.runtime_s, 3)
        row.update(r.meta)
        rows.append(row)
    df = pd.DataFrame(rows)
    return df.style.format({"Final f": "{:.3e}", "Final ||grad||": "{:.3e}", "Tolerance": "{:g}"}) \
        if hasattr(df, "style") and _in_notebook() else df


def _in_notebook() -> bool:
    try:
        from IPython import get_ipython
        return get_ipython() is not None and "IPKernelApp" in get_ipython().config
    except Exception:
        return False


# --------------------------------------------------------------------------------------
# Shared helpers
# --------------------------------------------------------------------------------------
def _style_for(runs, color_order=None):
    """Map method name -> (colour, linestyle, marker); stable across panels and figures."""
    names = list(color_order) if color_order else []
    for r in runs:
        if r.name not in names:
            names.append(r.name)
    if len(names) > 8:
        raise ValueError("More than 8 methods in one figure; compare fewer methods or split the figure.")
    if len(names) > 3:
        warnings.warn("More than 3 methods in one figure: colours 4+ are harder to tell apart. "
                      "Line style and marker still differ, but consider splitting the figure.", stacklevel=3)
    return {n: (_SERIES[i], _LINESTYLES[i % len(_LINESTYLES)], _MARKERS[i % len(_MARKERS)])
            for i, n in enumerate(names)}


def _finish(fig, show, save):
    if save:
        fig.savefig(save, bbox_inches="tight")
    if show:
        plt.show()
        return None
    return fig


def _iter_axis(ax, runs, xscale):
    kmax = max(r.iterations for r in runs)
    kmin = max(min(r.iterations for r in runs), 1)
    use_symlog = xscale == "symlog" or (xscale == "auto" and kmax >= 100 and kmax / kmin >= 20)
    if use_symlog:
        ax.set_xscale("symlog", linthresh=10, linscale=1.0)
        ax.set_xlim(0, kmax * 1.15)
        ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{int(v):,}"))
        ax.set_xlabel("iteration k  (linear up to 10, logarithmic beyond)")
    else:
        ax.set_xlim(-0.025 * max(kmax, 1), max(kmax, 1) * 1.04)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        ax.set_xlabel("iteration k")
    return use_symlog


def _end_marker(ax, x, y, r, color):
    if r.converged:
        ax.plot([x], [y], marker="o", ms=8, mfc=color, mec=_SURFACE, mew=2, ls="none", zorder=6)
    else:
        ax.plot([x], [y], marker="X", ms=10, mfc=color, mec=_SURFACE, mew=1.5, ls="none", zorder=6)


def _handles(runs, sty, with_end_markers=True):
    h = []
    for r in runs:
        c, ls, _ = sty[r.name]
        h.append(Line2D([0], [0], color=c, ls=ls, lw=2.2, label=r.label()))
    if with_end_markers:
        h.append(Line2D([0], [0], marker="o", ls="none", mfc=_INK2, mec=_SURFACE, ms=7, label="end of run, converged"))
        h.append(Line2D([0], [0], marker="X", ls="none", mfc=_INK2, mec=_SURFACE, ms=8, label="end of run, did not converge"))
    return h


_FLOOR = 1e-18  # zeros cannot be drawn on a log axis; they are shown at this height and footnoted


# --------------------------------------------------------------------------------------
# Convergence plots
# --------------------------------------------------------------------------------------
def _draw_convergence(ax, runs, sty, what, f_star, xscale):
    clipped = False
    for r in runs:
        c, ls, _ = sty[r.name]
        if what == "grad_norm":
            y = r.gnorms.copy()
        else:
            y = r.fs - f_star
        clipped |= bool((y <= 0).any())
        y = np.maximum(y, _FLOOR)
        k = np.arange(len(y))
        step = max(1, len(y) // 20000)               # decimate only for drawing, keep the last point
        idx = np.unique(np.r_[np.arange(0, len(y), step), len(y) - 1])
        ax.plot(k[idx], y[idx], color=c, ls=ls, lw=2.0, zorder=3)
        _end_marker(ax, k[-1], y[-1], r, c)
    ax.set_yscale("log")
    if what == "grad_norm":
        for t in sorted({r.tol for r in runs}):
            ax.axhline(t, color=_INK2, lw=1.0, zorder=2)
            ax.annotate(f"tolerance {t:g}", xy=(0, t), xycoords=("axes fraction", "data"),
                        xytext=(6, 4), textcoords="offset points", ha="left", va="bottom",
                        fontsize=8.5, color=_INK2)
        ax.set_ylabel(r"gradient norm  $\|\nabla f(x_k)\|$  (log scale)")
    else:
        ax.set_ylabel(r"suboptimality  $f(x_k)-f^\star$  (log scale)")
    _iter_axis(ax, runs, xscale)
    lo = min(float(np.min(np.maximum((r.gnorms if what == "grad_norm" else r.fs - f_star), _FLOOR))) for r in runs)
    if what == "grad_norm":
        lo = min(lo, min(r.tol for r in runs)) / 5
    else:
        lo = lo / 5
    ax.set_ylim(bottom=max(lo, _FLOOR / 10))
    return clipped


@_styled
def plot_convergence(runs: Sequence[OptRun], what: str = "grad_norm", f_star: float = 0.0,
                     xscale: str = "auto", title: Optional[str] = None,
                     allow_mixed_tol: bool = False, color_order=None,
                     show: bool = True, save: Optional[str] = None):
    """
    Gradient norm (what="grad_norm") or suboptimality f - f_star (what="suboptimality") against
    iteration, log y-axis, every run on the same axes, tolerance line drawn.

    f_star is the true minimum value (0 for both assignment problems).
    xscale="auto" switches to a symlog iteration axis when runs differ by more than 20x in length
    (so a 10-step Newton run and a 100,000-step GD run are both readable); the axis label says so.
    """
    if what not in ("grad_norm", "suboptimality"):
        raise ValueError('what must be "grad_norm" or "suboptimality".')
    runs = _prepare(runs, allow_mixed_tol)
    sty = _style_for(runs, color_order)
    fig, ax = plt.subplots(figsize=(11.0, 5.0))
    clipped = _draw_convergence(ax, runs, sty, what, f_star, xscale)
    ax.set_title(title or ("Gradient norm vs iteration" if what == "grad_norm"
                           else "Suboptimality vs iteration"))
    ax.legend(handles=_handles(runs, sty), loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=9)
    note = _tol_note(runs)
    if clipped:
        note += f".  Values <= 0 are drawn at {_FLOOR:g}."
    fig.text(0.01, -0.01, note, fontsize=8.5, color=_INK2, ha="left", va="top")
    fig.tight_layout()
    return _finish(fig, show, save)


@_styled
def plot_convergence_panel(runs: Sequence[OptRun], f_star: float = 0.0, xscale: str = "auto",
                           title: Optional[str] = None, allow_mixed_tol: bool = False,
                           color_order=None, show: bool = True, save: Optional[str] = None):
    """Gradient norm and suboptimality side by side (two panels, two axes, no dual y-axis)."""
    runs = _prepare(runs, allow_mixed_tol)
    sty = _style_for(runs, color_order)
    fig, axs = plt.subplots(1, 2, figsize=(13.2, 4.8))
    c1 = _draw_convergence(axs[0], runs, sty, "grad_norm", f_star, xscale)
    c2 = _draw_convergence(axs[1], runs, sty, "suboptimality", f_star, xscale)
    axs[0].set_title("Gradient norm")
    axs[1].set_title("Suboptimality")
    fig.legend(handles=_handles(runs, sty), loc="lower center", ncol=min(3, len(runs) + 2),
               bbox_to_anchor=(0.5, -0.17), fontsize=9.5)
    if title:
        fig.suptitle(title, x=0.01, ha="left", fontweight="bold", fontsize=13)
    note = _tol_note(runs) + (f".  Values <= 0 are drawn at {_FLOOR:g}." if (c1 or c2) else "")
    fig.text(0.01, -0.02, note, fontsize=8.5, color=_INK2, ha="left", va="top")
    fig.tight_layout()
    return _finish(fig, show, save)


@_styled
def plot_step_sizes(runs: Sequence[OptRun], title: str = "Accepted step size per iteration",
                    xscale: str = "auto", allow_mixed_tol: bool = False, color_order=None,
                    show: bool = True, save: Optional[str] = None):
    """Accepted step size alpha_k (log y). alpha = 1 is a full step; smaller means backtracking."""
    runs = _prepare(runs, allow_mixed_tol)
    sty = _style_for(runs, color_order)
    have = [r for r in runs if r.alphas is not None and len(r.alphas)]
    if not have:
        raise ValueError("None of the runs has step sizes. Pass alphas=... to make_run.")
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    for r in have:
        c, ls, mk = sty[r.name]
        k = np.arange(1, len(r.alphas) + 1)
        step = max(1, len(k) // 20000)
        ax.plot(k[::step], r.alphas[::step], color=c, ls=ls, lw=1.6, zorder=3)
        if len(k) <= 60:
            ax.plot(k, r.alphas, ls="none", marker=mk, ms=6, mfc=c, mec=_SURFACE, mew=1.5, zorder=4)
    ax.axhline(1.0, color=_INK2, lw=1.0)
    ax.annotate("alpha = 1 (full step)", xy=(0, 1.0), xycoords=("axes fraction", "data"),
                xytext=(4, 4), textcoords="offset points", fontsize=8.5, color=_INK2)
    ax.set_yscale("log")
    _iter_axis(ax, have, xscale)
    ax.set_ylabel(r"accepted step size $\alpha_k$  (log scale)")
    ax.set_title(title)
    ax.legend(handles=_handles(have, sty, with_end_markers=False), loc="best")
    skipped = [r.name for r in runs if r not in have]
    if skipped:
        fig.text(0.01, -0.01, "No step sizes recorded for: " + ", ".join(skipped),
                 fontsize=8.5, color=_INK2, ha="left", va="top")
    fig.tight_layout()
    return _finish(fig, show, save)


@_styled
def plot_condition_numbers(runs: Sequence[OptRun], title: str = "Condition number of the Hessian along the run",
                           xscale: str = "auto", allow_mixed_tol: bool = False, color_order=None,
                           show: bool = True, save: Optional[str] = None):
    """kappa(H_k) = lambda_max / lambda_min at each iterate (log y). Needs cond_numbers=... in make_run."""
    runs = _prepare(runs, allow_mixed_tol)
    sty = _style_for(runs, color_order)
    have = [r for r in runs if r.cond_numbers is not None]
    if not have:
        raise ValueError("None of the runs has condition numbers. Pass cond_numbers=... to make_run "
                         "(np.linalg.cond(H) at each iterate).")
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    for r in have:
        c, ls, mk = sty[r.name]
        y = r.cond_numbers
        k = np.arange(len(y))
        step = max(1, len(k) // 20000)
        ax.plot(k[::step], y[::step], color=c, ls=ls, lw=1.8, zorder=3)
        if len(k) <= 60:
            ax.plot(k, y, ls="none", marker=mk, ms=6, mfc=c, mec=_SURFACE, mew=1.5, zorder=4)
    ax.set_yscale("log")
    _iter_axis(ax, have, xscale)
    ax.set_ylabel(r"$\kappa(H_k)$  (log scale)")
    ax.set_title(title)
    ax.legend(handles=_handles(have, sty, with_end_markers=False), loc="best")
    fig.tight_layout()
    return _finish(fig, show, save)


@_styled
def plot_descent_check(run: OptRun, title: Optional[str] = None,
                       show: bool = True, save: Optional[str] = None):
    """
    g_k . d_k at every iteration for ONE run (needs dirderivs=...). Negative = descent direction.
    Iterations with g.d >= 0 are marked with a cross and counted in the legend.
    """
    if run.dirderivs is None:
        raise ValueError("This run has no dirderivs. Record g_k . d_k at each iteration "
                         "(before any fallback) and pass dirderivs=... to make_run.")
    c, _, _ = _style_for([run])[run.name]
    y = run.dirderivs
    k = np.arange(len(y))
    bad = y >= 0
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    ax.axhline(0.0, color=_INK2, lw=1.0)
    ax.plot(k, y, color=c, lw=1.6, zorder=3)
    ax.plot(k[~bad], y[~bad], ls="none", marker="o", ms=6, mfc=c, mec=_SURFACE, mew=1.5, zorder=4)
    ax.plot(k[bad], y[bad], ls="none", marker="X", ms=10, mfc=c, mec=_SURFACE, mew=1.5, zorder=5)
    nz = np.abs(y[y != 0])
    ax.set_yscale("symlog", linthresh=max(1e-8, float(nz.min()) if nz.size else 1e-8))
    ax.set_xlabel("iteration k")
    ax.set_ylabel(r"$g_k^{\top} d_k$  (symlog scale)")
    ax.set_title(title or f"Is the Newton direction a descent direction?  ({run.name})")
    ax.legend(handles=[
        Line2D([0], [0], marker="o", ls="none", mfc=c, mec=_SURFACE, ms=7, label="g.d < 0: descent direction"),
        Line2D([0], [0], marker="X", ls="none", mfc=c, mec=_SURFACE, ms=9,
               label=f"g.d >= 0: NOT a descent direction ({int(bad.sum())} of {len(y)})")],
        loc="best")
    fig.tight_layout()
    return _finish(fig, show, save)


@_styled
def plot_shifts(runs: Sequence[OptRun], title: str = "Diagonal shift used by the safeguarded Newton step",
                allow_mixed_tol: bool = False, color_order=None,
                show: bool = True, save: Optional[str] = None):
    """lambda_k per iteration (log y) for runs recorded with shifts=...; lambda = 0 means no shift."""
    runs = _prepare(runs, allow_mixed_tol)
    sty = _style_for(runs, color_order)
    have = [r for r in runs if r.shifts is not None]
    if not have:
        raise ValueError("None of the runs has shifts. Pass shifts=... (lambda per iteration, 0 if none).")
    fig, ax = plt.subplots(figsize=(8.6, 4.4))
    lines = []
    for r in have:
        c, ls, mk = sty[r.name]
        k = np.arange(len(r.shifts))
        used = r.shifts > 0
        ax.plot(k[used], r.shifts[used], ls="none", marker=mk, ms=6, mfc=c, mec=_SURFACE, mew=1.2, zorder=4)
        lines.append(f"{r.name}: {int(used.sum())} of {len(r.shifts)} iterations shifted")
    ax.set_yscale("log")
    ax.yaxis.set_minor_formatter(LogFormatterSciNotation(minor_thresholds=(2, 0.5)))
    _iter_axis(ax, have, "linear")
    ax.set_xlabel("iteration k  (a marker = an iteration where H + lambda I was used)")
    ax.set_ylabel(r"shift $\lambda_k$  (log scale)")
    ax.set_title(title)
    ax.legend(handles=[Line2D([0], [0], marker=sty[r.name][2], ls="none", mfc=sty[r.name][0],
                              mec=_SURFACE, ms=7, label=ln) for r, ln in zip(have, lines)], loc="best")
    if all((r.shifts > 0).sum() == 0 for r in have):
        ax.text(0.5, 0.5, "no shifts were needed", transform=ax.transAxes, ha="center", color=_INK2)
    fig.tight_layout()
    return _finish(fig, show, save)


# --------------------------------------------------------------------------------------
# Rosenbrock paths
# --------------------------------------------------------------------------------------
def rosenbrock_xy(x, y, a: float = 1.0, b: float = 100.0):
    """Vectorised Rosenbrock f(x, y) = (a - x)^2 + b (y - x^2)^2 (works on arrays)."""
    return (a - x) ** 2 + b * (y - x ** 2) ** 2


def _mark_indices(n_points: int, max_marks: int = 12) -> np.ndarray:
    n = n_points - 1
    if n_points <= max_marks + 3:
        return np.arange(n_points)
    idx = np.unique(np.round(np.logspace(0, math.log10(n), max_marks)).astype(int))
    return np.unique(np.r_[0, idx, n])


@_styled
def plot_rosenbrock_paths(runs: Sequence[OptRun], a: float = 1.0, b: float = 100.0,
                          contour_fn: Optional[Callable] = None,
                          xlim=(-2.0, 2.0), ylim=(-1.0, 3.0), max_extent: float = 6.0,
                          title: str = "Optimization paths on the Rosenbrock function",
                          allow_mixed_tol: bool = False, color_order=None,
                          show: bool = True, save: Optional[str] = None):
    """
    Level curves of the Rosenbrock function with every run's path overlaid. One panel per distinct
    start point (shared axes), one colour/line style per method (the same in every panel).

    * Markers sit at iterations 0, 1, 2, ... spread logarithmically (about 12), so you can see the
      early steps of a 100,000-iteration run without 100,000 dots.
    * The start point is a diamond; the end of each run is a circle (converged) or a cross
      (did not converge). The minimizer (a, a^2) is the star.
    * The view starts at xlim x ylim and grows to include iterates up to max_extent away from the
      origin; any iterate still outside is counted in a note at the bottom of the panel.
    * contour_fn(X, Y) can replace the built-in Rosenbrock if you use another function (2-D only).
    """
    runs = _prepare(runs, allow_mixed_tol, disambiguate=False)
    for r in runs:
        if r.xs.shape[1] != 2:
            raise ValueError(f"{r.name}: path plots need 2-D iterates, got dimension {r.xs.shape[1]}.")
    sty = _style_for(runs, color_order)
    cf = contour_fn or (lambda X, Y: rosenbrock_xy(X, Y, a, b))

    groups: Dict[tuple, List[OptRun]] = {}
    for r in runs:
        groups.setdefault(tuple(np.round(r.start, 10)), []).append(r)

    # view: default window, expanded to include nearby iterates
    pts = np.vstack([r.xs for r in runs])
    inside_cap = (np.abs(pts) <= max_extent).all(axis=1)
    xl = [xlim[0], xlim[1]]
    yl = [ylim[0], ylim[1]]
    if inside_cap.any():
        p = pts[inside_cap]
        pad = 0.06
        xl = [min(xl[0], p[:, 0].min() - pad), max(xl[1], p[:, 0].max() + pad)]
        yl = [min(yl[0], p[:, 1].min() - pad), max(yl[1], p[:, 1].max() + pad)]
    gx, gy = np.meshgrid(np.linspace(xl[0], xl[1], 500), np.linspace(yl[0], yl[1], 500))
    Z = cf(gx, gy)
    hi = max(3, int(math.ceil(math.log10(max(float(np.nanmax(Z)), 10.0)))))
    levels = np.logspace(-1, hi, 2 * (hi + 1) + 1)

    ng = len(groups)
    ncols = min(3, ng)
    nrows = math.ceil(ng / ncols)
    fig, axs = plt.subplots(nrows, ncols, figsize=(5.0 * ncols + 0.6, 4.7 * nrows + 0.6),
                            sharex=True, sharey=True, squeeze=False)
    for ax in axs.ravel()[ng:]:
        ax.set_visible(False)

    for ax, (_, grp) in zip(axs.ravel(), groups.items()):
        ax.grid(False)
        cs = ax.contour(gx, gy, Z, levels=levels, colors="#c4c3bd", linewidths=0.7, zorder=1)
        ax.plot([a], [a ** 2], marker="*", ms=15, mfc=_INK, mec=_SURFACE, mew=1.5, ls="none", zorder=10)
        n_out_total = 0
        for r in grp:
            c, ls, mk = sty[r.name]
            P = r.xs
            step = max(1, len(P) // 20000)
            idx = np.unique(np.r_[np.arange(0, len(P), step), len(P) - 1])
            ax.plot(P[idx, 0], P[idx, 1], color=c, ls=ls, lw=1.5, alpha=0.95, zorder=4)
            mi = _mark_indices(len(P))
            ax.plot(P[mi, 0], P[mi, 1], ls="none", marker=mk, ms=5.5, mfc=c, mec=_SURFACE, mew=1.2, zorder=5)
            _end_marker(ax, P[-1, 0], P[-1, 1], r, c)
            n_out_total += int(((P[:, 0] < xl[0]) | (P[:, 0] > xl[1]) | (P[:, 1] < yl[0]) | (P[:, 1] > yl[1])).sum())
        s = grp[0].start
        ax.plot([s[0]], [s[1]], marker="D", ms=9, mfc="#ffffff", mec=_INK, mew=1.8, ls="none", zorder=9)
        ax.set_xlim(xl)
        ax.set_ylim(yl)
        ax.set_title(r"start $x_0 = (" + f"{s[0]:g},\\ {s[1]:g}" + r")$", fontsize=11)
        if n_out_total:
            ax.text(0.98, 0.02, f"{n_out_total:,} iterate(s) outside this view", transform=ax.transAxes,
                    ha="right", va="bottom", fontsize=8, color=_INK2)
    for ax in axs[-1, :]:
        ax.set_xlabel("$x_1$")
    for ax in axs[:, 0]:
        ax.set_ylabel("$x_2$")

    names = []
    for r in runs:
        if r.name not in names:
            names.append(r.name)
    handles = [Line2D([0], [0], color=sty[n][0], ls=sty[n][1], lw=2.2, marker=sty[n][2], ms=6,
                      mfc=sty[n][0], mec=_SURFACE, label=n) for n in names]
    handles += [
        Line2D([0], [0], marker="D", ls="none", mfc="#ffffff", mec=_INK, mew=1.6, ms=7, label="start"),
        Line2D([0], [0], marker="*", ls="none", mfc=_INK, mec=_SURFACE, ms=12, label=f"minimizer ({a:g}, {a * a:g})"),
        Line2D([0], [0], marker="o", ls="none", mfc=_INK2, mec=_SURFACE, ms=7, label="end, converged"),
        Line2D([0], [0], marker="X", ls="none", mfc=_INK2, mec=_SURFACE, ms=8, label="end, did not converge"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=min(4, len(handles)), bbox_to_anchor=(0.5, -0.02), fontsize=9.5)
    # per-run counts (taken from the data) in a footnote
    lines = []
    for key, grp in groups.items():
        for r in grp:
            lines.append(f"{r.name} from {_fmt_point(r.start)}: {r.iterations:,} it., "
                         + ("converged" if r.converged else f"did not converge ({r.status})"))
    fig.suptitle(title, x=0.01, ha="left", fontweight="bold", fontsize=13)
    fig.tight_layout(rect=(0, 0.1 + 0.015 * len(handles) // 4, 1, 0.97))
    fig.text(0.01, 0.0, _tol_note(runs) + ". Grey curves: level sets of f (0.1 to 10^%d, two per decade). Markers: iterations spread logarithmically." % hi,
             fontsize=8.5, color=_INK2, ha="left", va="top")
    return _finish(fig, show, save)


# --------------------------------------------------------------------------------------
# Part A: iterations vs condition number
# --------------------------------------------------------------------------------------
@_styled
def plot_kappa_scaling(results, title: str = "Iterations to converge vs condition number",
                       show_reference: bool = False, color_order=None,
                       show: bool = True, save: Optional[str] = None):
    """
    Iterations needed against kappa on log-log axes, one line per method.

    results: a pandas DataFrame with columns kappa, method, iterations, converged
             (and optional cap = iteration cap used), or a list of dicts with those keys.
    Runs that did not converge are drawn as a cross at the iteration cap and listed in the legend,
    so a capped GD run can never be read as "took 200,000 iterations to converge".
    show_reference=True adds a dotted line proportional to kappa through the first point of the
    slowest method, to compare slopes. Off by default.
    """
    import pandas as pd
    df = results if isinstance(results, pd.DataFrame) else pd.DataFrame(list(results))
    need = {"kappa", "method", "iterations", "converged"}
    if not need <= set(df.columns):
        raise ValueError(f"results needs columns {sorted(need)}; got {sorted(df.columns)}.")
    methods = list(color_order) if color_order else []
    for m in df["method"]:
        if m not in methods:
            methods.append(m)
    if len(methods) > 3:
        warnings.warn("More than 3 methods: consider splitting the figure.", stacklevel=2)
    fig, ax = plt.subplots(figsize=(7.8, 5.0))
    any_failed = False
    for i, m in enumerate(methods):
        d = df[df["method"] == m].sort_values("kappa")
        c, ls, mk = _SERIES[i], _LINESTYLES[i % len(_LINESTYLES)], _MARKERS[i]
        ax.plot(d["kappa"], d["iterations"], color=c, ls=ls, lw=1.8, zorder=3)
        ok = d["converged"].astype(bool)
        ax.plot(d["kappa"][ok], d["iterations"][ok], ls="none", marker=mk, ms=8, mfc=c, mec=_SURFACE, mew=1.5, zorder=4)
        if (~ok).any():
            any_failed = True
            ax.plot(d["kappa"][~ok], d["iterations"][~ok], ls="none", marker="X", ms=11, mfc=c, mec=_SURFACE, mew=1.5, zorder=5)
        ax.annotate(m, xy=(d["kappa"].iloc[-1], d["iterations"].iloc[-1]), xytext=(8, 0),
                    textcoords="offset points", va="center", fontsize=9, color=_INK)
    if show_reference:
        slow = df.groupby("method")["iterations"].max().idxmax()
        d = df[df["method"] == slow].sort_values("kappa")
        k0, y0 = float(d["kappa"].iloc[0]), float(d["iterations"].iloc[0])
        ks = np.array([d["kappa"].min(), d["kappa"].max()], dtype=float)
        ax.plot(ks, y0 * ks / k0, color=_INK2, lw=1.0, ls=":", zorder=2)
        ax.annotate("slope 1 reference", xy=(ks[-1], y0 * ks[-1] / k0), xytext=(-6, -12),
                    textcoords="offset points", ha="right", fontsize=8.5, color=_INK2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"condition number $\kappa$  (log scale)")
    ax.set_ylabel("iterations to reach tolerance  (log scale)")
    ax.set_title(title)
    ax.set_xticks(sorted(df["kappa"].unique()))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.xaxis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
    handles = [Line2D([0], [0], color=_SERIES[i], ls=_LINESTYLES[i % len(_LINESTYLES)], lw=2.2, marker=_MARKERS[i],
                      mfc=_SERIES[i], mec=_SURFACE, ms=7, label=m) for i, m in enumerate(methods)]
    if any_failed:
        handles.append(Line2D([0], [0], marker="X", ls="none", mfc=_INK2, mec=_SURFACE, ms=9,
                              label="did not converge (value shown is the iteration cap)"))
    ax.legend(handles=handles, loc="upper left")
    ax.margins(x=0.12)
    fig.tight_layout()
    return _finish(fig, show, save)


# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Self-test with SYNTHETIC histories (not real optimizer output): draws every figure once.
    import matplotlib
    matplotlib.use("Agg")
    rng = np.random.default_rng(0)

    def fake(name, x0, n, decay, conv=True):
        t = np.arange(n + 1)
        xs = np.array([1 + (np.array(x0) - 1) * decay ** k + 0.02 * rng.standard_normal(2) * decay ** k for k in t])
        fs = rosenbrock_xy(xs[:, 0], xs[:, 1])
        g = np.maximum(np.linalg.norm(xs - 1, axis=1), 1e-12) * (1.0 if conv else 5e3)
        g[-1] = 1e-7 if conv else 1e-2
        return make_run(name, xs, fs=fs, gnorms=g, tol=1e-6, max_iter=n, alphas=np.full(n, 0.5))
    runs = [fake("method A", (-1.2, 1), 40, 0.7), fake("method B", (-1.2, 1), 3000, 0.995, conv=False)]
    plot_convergence(runs, show=False, save="selftest_convergence.png")
    plot_rosenbrock_paths(runs, show=False, save="selftest_paths.png")
    print("self-test figures written")