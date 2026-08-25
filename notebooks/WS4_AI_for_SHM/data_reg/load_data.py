import logging
import requests
import polars as pl
from pathlib import Path


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

url = "https://zenodo.org/records/15700928/files/Aventa_AV7_IET_OST_SCADA.csv?download=1"

# Store data next to this script
data_dir = Path(__file__).parent
raw_path = data_dir / "Aventa_AV7_IET_OST_SCADA.csv"
processed_path = data_dir / "Aventa_AV7_IET_OST_SCADA_10min.parquet"


# Download raw data
if not raw_path.exists() or raw_path.stat().st_size == 0:
    logger.info("Downloading raw SCADA data...")

    with requests.get(url, stream=True) as response:
        response.raise_for_status()

        with raw_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)

    logger.info("Raw data saved to %s", raw_path)
else:
    logger.info("Raw data already available.")


# Compute 10-minute statistics
if not processed_path.exists():
    logger.info("Computing 10-minute statistics...")

    (
        pl.scan_csv(raw_path, try_parse_dates=True)
        .group_by_dynamic("Datetime", every="10m")
        .agg(
            # Continuous variables
            pl.all()
            .exclude("Datetime", "StatusAnlage")
            .mean()
            .name.suffix("_mean"),

            pl.all()
            .exclude("Datetime", "StatusAnlage")
            .std()
            .name.suffix("_std"),

            # Categorical variable
            pl.col("StatusAnlage")
            .mode()
            .first()
            .alias("StatusAnlage"),
        )
        .sink_parquet(processed_path)
    )

    logger.info("Processed data saved to %s", processed_path)
else:
    logger.info("Processed data already available.")