import pandas as pd
import requests
from loguru import logger


def download():
    df = pd.read_csv("urls.csv")

    for r in df.iterrows():
        i, (doi, url, ext) = r
        ds_fname = f"ds-{i}{ext}"
        logger.info(f"getting dataset: {i}")
        r = requests.get(url)
        with open(ds_fname, "wb") as f:
            f.write(r.content)
        logger.info(f"write dataset: {ds_fname}")


if __name__ == '__main__':
    download()
