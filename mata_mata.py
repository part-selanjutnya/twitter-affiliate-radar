import json
import os
import requests
from bs4 import BeautifulSoup

# 1. Baca Konfigurasi
try:
    with open('config_twitter.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("File config_twitter.json tidak ditemukan!")
    exit()

if config.get("status_bot") == "OFF":
    print("Status bot sedang OFF. Pengintaian dihentikan.")
    exit()

GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
REPO_NAME = os.environ.get("GITHUB_REPOSITORY")

def kirim_notifikasi(judul, isi):
    if not GITHUB_TOKEN or not REPO_NAME:
        print(f"Simulasi Notifikasi: {judul}")
        return

    url = f"https://api.github.com/repos/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"title": judul, "body": isi}
    res = requests.post(url, headers=headers, json=data)
    if res.status_code == 201:
        print(f"✅ Notifikasi Issue berhasil dikirim: {judul}")
    else:
        print(f"❌ Gagal mengirim notifikasi: {res.text}")

def mulai_intai_direk():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Memulai radar pengintaian dengan metode pencarian langsung...")

    for akun in target_akun:
        print(f"🔍 Menyelidiki aktivitas terbaru dari @{akun}...")
        try:
            # Menggunakan peladen penelusuran publik alternatif untuk membaca cuitan
            url_search = f"https://html.duckduckgo.com/html/?q=site:twitter.com/{akun}"
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            
            response = requests.get(url_search, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"⚠️ Gagal menjangkau data untuk @{akun}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('div', class_='result')
            
            if not results:
                print(f"⚠️ Tidak ada hasil ditemukan untuk @{akun}")
                continue

            for res in results[:5]:
                snippet_elem = res.find('a', class_='result__snippet')
                link_elem = res.find('a', class_='result__url')
                
                if not snippet_elem:
                    continue
                
                teks_cuitan = snippet_elem.get_text().lower()
                link_tujuan = link_elem['href'] if link_elem else f"https://twitter.com/{akun}"

                # Pencocokan kata kunci
                for kw in kata_kunci:
                    if kw in teks_cuitan:
                        judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                        isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Konten:** {snippet_elem.get_text()}\n\n**Tautan Akses:** {link_tujuan}\n\n*Segera tinjau dan balas menggunakan strategi terbaik Anda!*"
                        
                        kirim_notifikasi(judul, isi)
                        break

        except Exception as e:
            print(f"⚠️ Terkendala saat memproses @{akun}: {e}")

if __name__ == "__main__":
    mulai_intai_direk()
