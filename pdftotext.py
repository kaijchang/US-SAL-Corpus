import os
import subprocess
import re

PDFS_DIR = 'pdfs'
TEXT_DIR = 'text'

os.makedirs(TEXT_DIR, exist_ok=True)

for filename in os.listdir(PDFS_DIR):
    pdf_path = os.path.join(PDFS_DIR, filename)
    text_path = os.path.join(TEXT_DIR, f'{os.path.splitext(filename)[0]}.txt')
    
    if not os.path.exists(text_path):
        print(f'Converting {pdf_path} to {text_path}')
        options = []
        subprocess.run(['pdftotext', *options, pdf_path, text_path])

    else:
        print(f'File {text_path} already exists')
