"""Input/output utilities for the ETL pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import pandas as pd


class DataLoader(Protocol):
    """Contract for loader components."""

    def load(self) -> pd.DataFrame:  # pragma: no cover - interface
        ...


class DataWriter(Protocol):
    """Contract for writer components."""

    def write(self, data: pd.DataFrame, destination: Path) -> Path:  # pragma: no cover - interface
        ...


@dataclass(frozen=True)
class CSVDataSource:
    """Load data from CSV files with explicit configuration."""

    path: Path
    delimiter: str = ","
    encoding: str = "utf-8"

    def load(self) -> pd.DataFrame:
        if not self.path.exists():
            raise FileNotFoundError(f"No se encontró el archivo de origen: {self.path}")
        return pd.read_csv(self.path, delimiter=self.delimiter, encoding=self.encoding)


@dataclass(frozen=True)
class CSVDataWriter:
    """Persist DataFrames into CSV format."""

    def write(self, data: pd.DataFrame, destination: Path) -> Path:
        destination.parent.mkdir(parents=True, exist_ok=True)
        data.to_csv(destination, index=False)
        return destination
