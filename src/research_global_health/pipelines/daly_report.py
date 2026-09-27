"""Build a local DALY table and figure from the extracted CSV."""

import argparse
import csv
import math
from pathlib import Path

from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure

from research_global_health.pipelines.daly import YEARS


def read_series(source: Path, through_year: int) -> list[tuple[int, float]]:
    """Validate the selected series and return it in chronological order."""
    if through_year not in (2020, 2021):
        raise ValueError("through_year must be 2020 or 2021")
    values: dict[int, float] = {}
    with source.open(encoding="utf-8", newline="") as stream:
        for row in csv.DictReader(stream):
            if (row["country_iso3"], row["sex"], row["age"], row["ghe_code"]) != (
                "RUS",
                "Persons",
                "All ages",
                "0",
            ):
                raise ValueError("Expected RUS / Persons / All ages / All Causes")
            year, total = int(row["year"]), float(row["daly_thousands"])
            if year not in YEARS or year in values:
                raise ValueError("Unexpected or duplicate year")
            if not math.isfinite(total) or total <= 0:
                raise ValueError("DALY must be finite and positive")
            values[year] = total
    expected = [year for year in YEARS if year <= through_year]
    if any(year not in values for year in expected):
        raise ValueError("Missing required year")
    return [(year, values[year]) for year in expected]


def build_report(source: Path, output_dir: Path, through_year: int = 2020) -> None:
    """Write Markdown and PNG locally; recalculate changes from raw totals."""
    series = read_series(source, through_year)
    baseline = series[0][1]
    lines = [
        f"# DALY в России: 2000–{through_year}",
        "",
        "Оба пола, все возрасты, все причины. DALY указаны в тысячах.",
        "",
        "| Год | DALY, тыс. | Изменение к 2000 году, % |",
        "| --- | ---: | ---: |",
    ]
    for year, total in series:
        lines.append(f"| {year} | {total:.2f} | {(total / baseline - 1) * 100:.2f} |")
    lines += [
        "",
        "![Динамика абсолютного объёма DALY в России](daly.png)",
        "",
        "Изменение: `(DALY / DALY_2000 - 1) × 100%`.",
        "",
        "Это абсолютный объём DALY, не показатель на душу населения и не "
        "возраст-стандартизованный показатель. Линии соединяют доступные годы; "
        "промежуточные годовые оценки не представлены.",
        "",
        "Источник: Global Health Estimates 2021: Disease burden by Cause, Age, Sex, "
        "by Country and by Region, 2000–2021. Geneva: World Health Organization; 2024.",
        "",
        "[Источник WHO GHE](https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates/global-health-estimates-leading-causes-of-dalys).",
        "",
        "Исходные оценки принадлежат WHO; проценты и визуализация подготовлены "
        "автором учебного проекта. WHO не является автором этого анализа и не "
        "подтверждает его выводы. Использование данных регулируется "
        "[условиями WHO](https://www.who.int/about/policies/publishing/data-policy/terms-and-conditions), "
        "а не лицензией кода проекта.",
        "",
    ]
    figure = Figure(figsize=(9, 5), layout="constrained")
    FigureCanvasAgg(figure)
    axes = figure.subplots()
    axes.plot(
        [year for year, _ in series],
        [total for _, total in series],
        color="#245e58",
        marker="o",
        linewidth=2,
    )
    axes.set(
        title=f"DALY в России, 2000–{through_year}", xlabel="Год", ylabel="DALY, тыс."
    )
    axes.set_xticks([year for year, _ in series])
    axes.tick_params(axis="x", labelrotation=45)
    axes.set_ylim(bottom=0)
    axes.grid(axis="y", alpha=0.25)
    axes.spines[["top", "right"]].set_visible(False)
    output_dir.mkdir(parents=True, exist_ok=True)
    figure.savefig(output_dir / "daly.png", dpi=160)
    (output_dir / "results.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    """Run local report generation."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("data/local/daly_rus.csv"))
    parser.add_argument("--through-year", type=int, choices=(2020, 2021), default=2020)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    output = args.output_dir or Path(f"data/local/report-{args.through_year}")
    build_report(args.source, output, args.through_year)
    print(f"Saved local report to {output}")


if __name__ == "__main__":
    main()
