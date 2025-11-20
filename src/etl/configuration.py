"""Configuration models for the ETL pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable

import yaml


@dataclass(frozen=True)
class DatasetConfig:
    """Represents the input dataset metadata."""

    raw_path: Path
    delimiter: str = ","
    encoding: str = "utf-8"


@dataclass(frozen=True)
class OutputsConfig:
    """Represents the destination tables produced by the ETL."""

    clean_table: Path
    summary_by_region: Path
    summary_by_type: Path
    summary_by_year: Path


@dataclass(frozen=True)
class ProcessingConfig:
    """Encapsulates business rules applied during transformations."""

    normalize_ascii: bool
    string_columns: Iterable[str]
    column_aliases: Dict[str, str]


@dataclass(frozen=True)
class ETLConfig:
    """Aggregate configuration for the ETL pipeline."""

    dataset: DatasetConfig
    outputs: OutputsConfig
    processing: ProcessingConfig

    @classmethod
    def from_yaml(cls, file_path: Path) -> "ETLConfig":
        with open(file_path, "r", encoding="utf-8") as handle:
            payload = yaml.safe_load(handle)

        dataset_cfg = DatasetConfig(
            raw_path=Path(payload["dataset"]["raw_path"]),
            delimiter=payload["dataset"].get("delimiter", ","),
            encoding=payload["dataset"].get("encoding", "utf-8"),
        )

        outputs_cfg = OutputsConfig(
            clean_table=Path(payload["outputs"]["clean_table"]),
            summary_by_region=Path(payload["outputs"]["summary_by_region"]),
            summary_by_type=Path(payload["outputs"]["summary_by_type"]),
            summary_by_year=Path(payload["outputs"]["summary_by_year"]),
        )

        processing_cfg = ProcessingConfig(
            normalize_ascii=payload["processing"].get("normalize_ascii", False),
            string_columns=tuple(payload["processing"].get("string_columns", [])),
            column_aliases=payload["processing"].get("column_aliases", {}),
        )

        return cls(
            dataset=dataset_cfg,
            outputs=outputs_cfg,
            processing=processing_cfg,
        )
