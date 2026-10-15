"""Latihan web scraping menggunakan BeautifulSoup: data negara -> CSV.

Sumber adalah situs sandbox latihan, bukan data demografi mutakhir.
Jalankan: pip install requests beautifulsoup4
         python scraping_negara_beautifulsoup.py
"""
import csv
import requests
from bs4 import BeautifulSoup

URL = "https://www.scrapethissite.com/pages/simple/"
OUTPUT = "data_negara_beautifulsoup.csv"
MAX_RECORDS = 50  # Ganti ke None jika ingin semua 250 entri dari situs.

response = requests.get(URL, timeout=30, headers={"User-Agent": "EducationalDataScraper/1.0"})
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
rows = []

for country in soup.select("div.country"):
    name = country.select_one(".country-name")
    capital = country.select_one(".country-capital")
    population = country.select_one(".country-population")
    area = country.select_one(".country-area")
    if not all([name, capital, population, area]):
        continue
    rows.append({
        "Nama_Negara": name.get_text(strip=True),
        "Ibu_Kota": capital.get_text(strip=True),
        "Populasi_Referensi": int(population.get_text(strip=True)),
        "Luas_km2": float(area.get_text(strip=True)),
        "Sumber": URL,
    })
    if MAX_RECORDS is not None and len(rows) >= MAX_RECORDS:
        break

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Nama_Negara", "Ibu_Kota", "Populasi_Referensi", "Luas_km2", "Sumber"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Berhasil menyimpan {len(rows)} baris ke {OUTPUT}")
print("\n=== HASIL WEB SCRAPING ===")

for row in rows[:10]:
    print(row)

print(f"\nTotal data berhasil diambil: {len(rows)}")
