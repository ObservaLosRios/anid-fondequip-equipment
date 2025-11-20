"""Unit tests for the ETL transformer."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from etl.configuration import ProcessingConfig  # type: ignore
from etl.transformer import FondequipTransformer  # type: ignore


@pytest.fixture()
def transformer() -> FondequipTransformer:
    config = ProcessingConfig(
        normalize_ascii=True,
        string_columns=("Folio", "Programa"),
        column_aliases={"Folio": "folio", "Programa": "programa"},
    )
    return FondequipTransformer(config)


def test_infer_year_valid(transformer: FondequipTransformer) -> None:
    assert transformer._infer_year("EQM210074") == 2021  # pylint: disable=protected-access


def test_clean_renames_columns_and_derives_year(transformer: FondequipTransformer) -> None:
    frame = pd.DataFrame(
        {
            "Folio": ["EQM210074"],
            "Programa": [" FONDEQUIP "],
        }
    )

    cleaned = transformer.clean(frame)

    assert "folio" in cleaned.columns
    assert cleaned.loc[0, "programa"] == "FONDEQUIP"
    assert cleaned.loc[0, "anio_convocatoria"] == 2021
