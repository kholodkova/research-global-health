"""Report validation uses synthetic data only."""

import csv
from pathlib import Path

import pytest

from research_global_health.pipelines.daly import YEARS
from research_global_health.pipelines.daly_report import build_report, read_series


def write_source(path: Path, years: tuple[int, ...] = YEARS) -> None:
    with path.open("w", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(
            ["year", "country_iso3", "sex", "age", "ghe_code", "daly_thousands"]
        )
        for year in reversed(years):
            writer.writerow([year, "RUS", "Persons", "All ages", 0, 100 + year - 2000])


def test_versions_and_calculation(tmp_path: Path) -> None:
    source = tmp_path / "input.csv"
    write_source(source)
    assert len(read_series(source, 2020)) == 5
    assert len(read_series(source, 2021)) == 6
    for end in (2020, 2021):
        output = tmp_path / str(end)
        build_report(source, output, end)
        text = (output / "results.md").read_text()
        assert f"| {end} | {100 + end - 2000:.2f} | {end - 2000:.2f} |" in text
        assert ("| 2021 |" in text) == (end == 2021)
        assert (output / "daly.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n")


@pytest.mark.parametrize("years", [YEARS[1:], (*YEARS, 2021)])
def test_missing_or_duplicate_year_does_not_write(
    tmp_path: Path, years: tuple[int, ...]
) -> None:
    source, output = tmp_path / "input.csv", tmp_path / "report"
    write_source(source, years)
    with pytest.raises(ValueError):
        build_report(source, output)
    assert not output.exists()


@pytest.mark.parametrize("old,new", [("RUS", "USA"), ("121", "nan"), ("121", "-1")])
def test_rejects_wrong_population_or_invalid_value(
    tmp_path: Path, old: str, new: str
) -> None:
    source = tmp_path / "input.csv"
    write_source(source)
    source.write_text(source.read_text().replace(old, new))
    with pytest.raises(ValueError):
        read_series(source, 2021)
