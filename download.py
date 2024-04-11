import requests
from bs4 import BeautifulSoup

import os
import subprocess

import numpy as np
import cv2

import dotenv

dotenv.load_dotenv()

PDFS_DIR = "pdfs"


def download_file_if_needed(url: str, file_name=None):
    file_name = (
        file_name if file_name is not None else os.path.basename(url.split("?")[0])
    )
    pdf_path = os.path.join(PDFS_DIR, file_name)
    if not os.path.exists(pdf_path):
        subprocess.run(["wget", "-O", pdf_path, url])
    else:
        print(f"File {pdf_path} already exists")


os.makedirs(PDFS_DIR, exist_ok=True)

# Volumes 1-64 from Google Books
GOOGLE_BOOKS_VOLUMES = {
    1: "tpA_AAAAYAAJ",
    2: "SEMFAAAAYAAJ",
    3: "KJE_AAAAYAAJ",
    4: "mDcFAAAAYAAJ",
    5: "2hEuAAAAIAAJ",
    6: "ojkFAAAAYAAJ",
    7: "CG0DAAAAQAAJ",
    8: "tzoFAAAAYAAJ",
    9: "WNW0TeczPTUC",
    10: "IpvZ0poDVGwC",
    11: "zNjyHmRLTgYC",
    12: "g7wsAQAAMAAJ",
    13: "EyM3AAAAIAAJ",
    14: "kyY3AAAAIAAJ",
    15: "VC43AAAAIAAJ",
    16: "6rQ0AQAAMAAJ",
    17: "pSA3AAAAIAAJ",
    "18-1": "EWA2AQAAMAAJ",
    # "18-2": "",
    "18-3": "pSE3AAAAIAAJ",
    19: "ty43AAAAIAAJ",
    20: "bAcuAAAAIAAJ",
    21: "ijA3AAAAIAAJ",
    22: "eDE3AAAAIAAJ",
    23: "9AcuAAAAIAAJ",
    24: "Y0MFAAAAYAAJ",
    25: "kzQ3AAAAIAAJ",
    26: "biU3AAAAIAAJ",
    27: "ozU3AAAAIAAJ",
    28: "kDk3AAAAIAAJ",
    29: "uwguAAAAIAAJ",
    30: "fR7HIQzmH_IC",
    31: "CGY2AQAAMAAJ",
    "32-1": "ICU3AAAAIAAJ",
    "32-2": "MQsuAAAAIAAJ",
    "33-1": "6yI3AAAAIAAJ",
    "33-2": "T0cFAAAAYAAJ",
    "34-1": "ZyA3AAAAIAAJ",
    "34-2": "nkkFAAAAYAAJ",
    "34-3": "hzM3AAAAIAAJ",
    "35-1": "y0IFAAAAYAAJ",
    "35-2": "MkoFAAAAYAAJ",
    "36-1-1": "EEkFAAAAYAAJ",
    "36-1-2": "Fq9IAQAAMAAJ",
    "36-2": "tK9IAQAAMAAJ",
    "37-1": "J4uXBdTswXUC",
    "37-2": "DUI3AAAAIAAJ",
    "38-1": "1Qba7itYf5sC",
    "38-2": "_T83AAAAIAAJ",
    "39-1": "szo3AAAAIAAJ",
    "39-2": "q0YFAAAAYAAJ",
    "40-1": "TgPe1KVUj2sC",
    "40-2": "y0IFAAAAYAAJ",
    "41-1": "qJHn1oq64YEC",
    "41-2": "IEMFAAAAYAAJ",
    "42-1": "v9St9TTmLpYC",
    "42-2": "biNnRvf_zhUC",
    "43-1": "qwpAjsm7uDgC",
    "43-2": "3M4dmWhS1B0C",
    "44-1": "NjKHEdaA-XQC",
    "44-1-sup7": "C9q4yVkTGXQC",
    "44-2": "95rCBxsW6R0C",
    "44-3": "gG0cx4RXTpcC",
    "45-1": "S18m5ozyxSkC",
    "45-2": "st3Ff2wvndUC",
    "46-1": "AyFPp5IWBVoC",
    "46-2": "1w9sABPMhYoC",
    "47-1": "GhRmcGX1OdoC",
    "47-2": "njZTabXRD8IC",
    "48-1": "Mui4h1rIJEcC",
    "48-2": "2BDvJzoggTsC",
    # "49-1": "dlcpXiQJeHYC",
    "49-2": "jkxBe6o7uX8C",
    "50-1": "yBGaV09CnQMC",
    "50-2": "fBqZpITr_H0C",
    51: "gNN52yaQRM8C",
    52: "J200wTpvGW0C",
    "53-1": "WHyPjkIBCrIC",
    "53-2": "DEsmTC1cCxYC",
    "53-3": "N-7VSAMak7sC",
    "54-1": "eTEkRoqcrKwC",
    "54-2": "Jfv8-V_NCX0C",
    "55-1": "ZXTvc5fTd7IC",
    "55-2": "a7UNTqmDBTkC",
    # "56-1": "igpQxE4JgLkC",
    "56-2": "WaKfVLeHHBkC",
    "57-1": "_kVwANdU0RUC",
    "57-2": "KRJkyL2n4lUC",
    "58-1": "MajQ1VTeN9kC",
    "58-2": "yVT--rETULQC",
    "59-1": "FCZNY8LpqJgC",
    "59-2": "98Thb1Yzc4oC",
    # "60-1": "F6F_K4C2tZoC",
    "60-2": "B_bQ_5LePswC",
    "61-1": "mU1eSbWKbhIC",
    # "61-2": "ftnlW523PF8C",
    "61-3": "jooGtTfAbGgC",
    "61-4": "KTO1yKHVbkAC",
    "61-5": "oUIG9i_Qxn8C",
    "61-6": "8lqjPjgLtV0C",
    "62-1": "sK5lnXYaBMkC",
    "62-2": "EZtXGXZbH4cC",
    "62-3": "SLuluZQurCYC",
    "63-1": "gOf9CBxINzkC",
    "63-2": "9P9KA-9fJZ0C",
    "63-3": "VL74odqHIq0C",
    "64-1": "BcnNrYBlTAoC",
    # "64-2": "Kpbx7QJuvB4C",
    "64-3": "O0TtaZ_kI44C",
}

for key, value in GOOGLE_BOOKS_VOLUMES.items():
    file_name = f"STATUTE-{key}.pdf"
    pdf_path = os.path.join(PDFS_DIR, file_name)
    if os.path.exists(pdf_path):
        print(f"File {pdf_path} already exists")
        continue
    r = requests.get(
        f"https://www.googleapis.com/books/v1/volumes/{value}?key={os.getenv('GOOGLE_API_KEY')}"
    )
    download_link = r.json()["accessInfo"]["pdf"]["downloadLink"]

    r = requests.get(download_link)
    soup = BeautifulSoup(r.text, "html.parser")
    capid_input = soup.find("input", attrs={"name": "capid"})
    capid = capid_input["value"]

    capid_image_url = f"https://books.google.com/books?capid={capid}"
    capid_image_array = np.asarray(
        bytearray(requests.get(capid_image_url).content), dtype=np.uint8
    )

    cv2.imshow("Captcha Image", cv2.imdecode(capid_image_array, -1))
    cv2.waitKey(1)
    captcha = input("Please enter the captcha: ")

    download_link = f"{download_link}&capid={capid}&captcha={captcha}"
    download_file_if_needed(download_link, f"STATUTE-{key}.pdf")

# Volumes 65-132 from GovInfo
for i in range(65, 133):
    download_file_if_needed(
        f"https://www.govinfo.gov/content/pkg/STATUTE-{i}/pdf/STATUTE-{i}.pdf"
    )
