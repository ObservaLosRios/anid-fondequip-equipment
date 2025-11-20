"""Command-line entry point for running the ETL pipeline."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from etl import ETLConfig, ETLPipeline  # type: ignore # pylint: disable=wrong-import-position
from etl.io_handlers import CSVDataSource, CSVDataWriter  # type: ignore # pylint: disable=wrong-import-position
from etl.transformer import FondequipTransformer  # type: ignore # pylint: disable=wrong-import-position


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the FONDEQUIP ETL pipeline")
    parser.add_argument(
        "--config",
        default="config/base.yaml",
        type=str,
        help="Ruta al archivo de configuración YAML",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = PROJECT_ROOT / args.config
    config = ETLConfig.from_yaml(config_path)

    loader = CSVDataSource(
        path=PROJECT_ROOT / config.dataset.raw_path,
        delimiter=config.dataset.delimiter,
        encoding=config.dataset.encoding,
    )
    transformer = FondequipTransformer(config.processing)
    writer = CSVDataWriter()

    pipeline = ETLPipeline(
        loader=loader,
        transformer=transformer,
        writer=writer,
        outputs=config.outputs,
    )

    result = pipeline.run()
    print("Tablas generadas:")
    print(f" - Limpio: {result.clean_table}")
    print(f" - Resumen por región: {result.summary_by_region}")
    print(f" - Resumen por tipo: {result.summary_by_type}")
    print(f" - Resumen anual: {result.summary_by_year}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
