"""Business transformations for the FONDEQUIP dataset."""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass

import pandas as pd
from pandas._libs.missing import NAType

from .configuration import ProcessingConfig


@dataclass
class FondequipTransformer:
    """Clean and summarize the raw registry following SOLID principles."""

    config: ProcessingConfig

    def clean(self, frame: pd.DataFrame) -> pd.DataFrame:
        cleaned = frame.copy()
        cleaned = self._strip_string_columns(cleaned)
        cleaned = self._rename_columns(cleaned)
        if self.config.normalize_ascii:
            cleaned = self._normalize_column_names(cleaned)
        cleaned["anio_convocatoria"] = cleaned["folio"].map(self._infer_year).astype("Int64")
        return cleaned

    def summarize_by_region(self, frame: pd.DataFrame) -> pd.DataFrame:
        return (
            frame.groupby("region_instalacion", dropna=False)
            .size()
            .reset_index(name="total_equipos")
            .sort_values("total_equipos", ascending=False)
        )

    def summarize_by_type(self, frame: pd.DataFrame) -> pd.DataFrame:
        return (
            frame.groupby("tipo_equipamiento", dropna=False)
            .size()
            .reset_index(name="total_equipos")
            .sort_values("total_equipos", ascending=False)
        )

    def summarize_by_year(self, frame: pd.DataFrame) -> pd.DataFrame:
        valid_years = frame.dropna(subset=["anio_convocatoria"])
        return (
            valid_years.groupby("anio_convocatoria")
            .size()
            .reset_index(name="total_equipos")
            .sort_values("anio_convocatoria")
        )

    def _strip_string_columns(self, frame: pd.DataFrame) -> pd.DataFrame:
        for column in self.config.string_columns:
            if column in frame.columns:
                frame[column] = frame[column].astype(str).str.strip()
        return frame

    def _rename_columns(self, frame: pd.DataFrame) -> pd.DataFrame:
        rename_map = self.config.column_aliases
        return frame.rename(columns=rename_map)

    def _normalize_column_names(self, frame: pd.DataFrame) -> pd.DataFrame:
        normalized = {
            column: self._normalize_ascii(column)
            for column in frame.columns
        }
        return frame.rename(columns=normalized)

    @staticmethod
    def _normalize_ascii(label: str) -> str:
        normalized = unicodedata.normalize("NFKD", label)
        ascii_only = "".join(ch for ch in normalized if not unicodedata.combining(ch))
        return ascii_only.lower().replace(" ", "_")

    @staticmethod
    def _infer_year(folio: str) -> int | NAType:
        if not isinstance(folio, str) or len(folio) < 5:
            return pd.NA
        try:
            year_digits = int(folio[3:5])
        except ValueError:
            return pd.NA
        return 2000 + year_digits
