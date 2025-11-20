# Observatorio FONDEQUIP · Región de Los Ríos

Repositorio oficial del pipeline ETL y del dashboard estático que resume el equipamiento científico financiado por FONDEQUIP con foco en la Región de Los Ríos. El flujo automatiza la limpieza de datos, genera tablas resumidas y publica visualizaciones interactivas en `docs/index.html`.

## Contenido principal

- **Pipeline ETL** (`src/`, `scripts/run_etl.py`): normaliza la base original, valida campos críticos y produce tablas consolidadas por región, tipo, institución y año.
- **Visualizaciones Highcharts** (`docs/*.html`): cinco componentes (regiones, tipos, instituciones, evolución y treemap) con modo claro/oscuro y encabezados consistentes, incrustados en la landing `docs/index.html`.
- **Notebook de apoyo** (`notebooks/etl_report.ipynb`): bitácora exploratoria que respalda las decisiones del ETL y permite replicar análisis ad-hoc.

## Requisitos

- Python 3.10+
- pip ≥ 23

### Instalar dependencias

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Ejecutar el ETL

```bash
PYTHONPATH=src python scripts/run_etl.py --config config/base.yaml
```

Salidas relevantes:

- `data/processed/fondequip_clean.csv`
- `data/processed/fondequip_resumen_region.csv`
- `data/processed/fondequip_resumen_tipo.csv`
- `data/processed/fondequip_resumen_anio.csv`

Estas tablas alimentan las visualizaciones incluidas en `docs/`.

## Visualizaciones

1. Ejecuta el ETL (o actualiza los CSV según corresponda).
2. Abre `docs/index.html` en tu navegador o sirve la carpeta con:

	```bash
	cd docs
	python -m http.server 9000
	```

3. Navega por las secciones usando la barra superior (regiones, tipos, instituciones, evolución y treemap). Cada iframe apunta a su HTML dedicado para facilitar el mantenimiento.

## Estructura del proyecto

```
config/             # Parámetros YAML del pipeline
data/raw/           # Fuentes originales (solo lectura)
data/processed/     # Resultados del ETL
docs/               # Dashboard estático y activos web
notebooks/          # Exploración y análisis
scripts/            # Entrypoints ejecutables
src/                # Código fuente del pipeline
tests/              # Cobertura con pytest
```

## Pruebas automatizadas

```bash
PYTHONPATH=src pytest
```

## Despliegue en GitHub Pages (opcional)

1. Ejecuta el ETL si necesitas datos frescos.
2. Verifica `docs/index.html` localmente.
3. Haz push a la rama `main`. GitHub Pages puede apuntar directamente a la carpeta `docs/` del repositorio `ObservaLosRios/anid-fondequip-equipment` para exponer el dashboard.
