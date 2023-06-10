import favicon
import requests
import csv
import sys
import traceback
from loguru import logger

logger.remove()
logger.add(
    sys.stdout, format="{time:YYYY-MM-DD.HH:mm:ss} [{level}] {message}", level="INFO"
)
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD.HH:mm:ss} <red>[{level}] {message}</red>",
    level="ERROR",
)

with open("sites.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    for row in csv_reader:
        site = row[0].strip()
        url = row[1].strip()

        logger.info(f"Processing >>> {site} with URL {url}")

        logger.info("  Getting favicon...")

        try:
            icons = favicon.get(url)
        except:
            logger.error(f"  Encountered error when retrieving icons for url {url}")
            traceback.print_exc()
            continue

        i = 1
        ico_files_found = [i for i in icons if i.format == "ico"]

        if len(ico_files_found) == 0:
            logger.error(f"No ico file found for URL {url}")

        for icon in ico_files_found:
            response = requests.get(icon.url, stream=True)

            logger.info(f"  Writing icon to ./output/{site}_{i}.{icon.format}")

            with open(f"./output/{site}_{i}.{icon.format}", "wb") as image:
                for chunk in response.iter_content(1024):
                    image.write(chunk)

            i += 1
