from bs4 import BeautifulSoup

import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import tqdm

import typing

TEMP_DIR = "temp"
TEXT_DIR = "text"

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(TEXT_DIR, exist_ok=True)

def process_granule(granule: typing.Tuple[str, str]):
    source_path = os.path.dirname(granule[0])
    source_text_path = os.path.join(source_path, os.path.basename(granule[0].replace(".pdf", ".txt")))
    target_text_path = f"{TEXT_DIR}/{granule[1]}.txt"

    subprocess.run(["pdftotext", granule[0]])
    subprocess.run(f"cat {source_text_path} ff.txt >> {target_text_path}", shell=True)

for i in range(7, 132):
    source_zip_path = os.path.join(TEMP_DIR, f"STATUTE-{i}.zip")
    source_unzipped_path = os.path.join(TEMP_DIR, f"STATUTE-{i}")

    subprocess.run(["wget", "-O", source_zip_path, f"https://www.govinfo.gov/content/pkg/STATUTE-{i}.zip"])
    subprocess.run(["unzip", "-q", source_zip_path, "-d", TEMP_DIR])

    granules = []

    with open(os.path.join(source_unzipped_path, "mods.xml"), "r") as f:
        soup = BeautifulSoup(f.read(), "lxml")
        for granule in soup.find_all("relateditem", { "type": "constituent" }):
            granules.append([
                os.path.join(
                    source_unzipped_path,
                    "pdf",
                    granule.find("identifier", { "type": "uri" }).text.split("/")[-1] + ".pdf"
                ),
                granule.find("granuledate").text.split("-")[0]
            ])

    progress_bar = tqdm.tqdm(total=len(granules))

    with ThreadPoolExecutor() as executor:
        for result in executor.map(process_granule, granules):
            progress_bar.update(1)

    progress_bar.close()

    subprocess.run(f"yes | rm -rf {source_unzipped_path}*", shell=True)
