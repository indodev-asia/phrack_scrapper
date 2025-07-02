#!/usr/bin/env python3
import os
import time
import requests
from fake_useragent import UserAgent
from weasyprint import HTML

BASE_URL = "https://phrack.org/issues"
VOLUMES = range(67, 72)
ua = UserAgent()

output_dir = "phrack"
os.makedirs(output_dir, exist_ok=True)

def scrap_banner():
    try:
        print("""
        \tIndoDev Phrack Scrapper 2025 
        \tDeveloped by Anton (Indodev - www.indodev.asia)
        \tFetch articles from phrack.org from phrack 67 until phrack 72\n\n
        """)
    except Exception as e:
        raise e
    
def fetch_article_html(vol, art_num):
    url = f"{BASE_URL}/{vol}/{art_num}"
    headers = {"User-Agent": ua.random}
    resp = requests.get(url, headers=headers)
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.text

def save_pdf(html_content, pdf_number):
    filepath = os.path.join(output_dir, f"{pdf_number}.pdf")
    HTML(string=html_content).write_pdf(filepath)
    print(f"    ✔ Saved: {filepath}")

pdf_counter = 1
scrap_banner()

for vol in VOLUMES:
    print(f"[+] Scraping Phrack")
    article_number = 2  # skip intro

    while True:
        print(f"    → Fetching article {article_number}")
        try:
            html = fetch_article_html(vol, article_number)
            if html is None:
                print(f"    × Done with volume {vol}")
                break
            save_pdf(html, pdf_counter)
            pdf_counter += 1
            article_number += 1
            time.sleep(1)
        except Exception as e:
            print(f"    × Error on {vol}/{article_number}: {e}")
            break
