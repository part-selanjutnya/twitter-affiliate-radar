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

def mulai_intai_advanced():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Menjalankan radar dengan penyamaran browser tingkat lanjut...")

    # Menggunakan headers browser desktop lengkap untuk menghindari blokir bot-detection
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    for akun in target_akun:
        print(f"🔍 Menyelidiki aktivitas terbaru dari @{akun}...")
        try:
            # Menggunakan jalur pencarian alternatif berbasis penjelajahan publik
            url_search = f"https://lite.duckduckgo.com/lite/"
            data_payload = {'q': f'site:twitter.com/{akun}'}
            
            response = requests.post(url_search, headers=headers, data=data_payload, timeout=12)
            if response.status_code != 200:
                print(f"⚠️ Gagal menjangkau titik pencarian untuk @{akun} (Status: {response.status_code})")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Parsing struktur tabel hasil pencarian versi lite
            links = soup.find_all('a', class_='result-link')
            snippets = soup.find_all('td', class_='result-snippet')
            
            if not snippets:
                print(f"⚠️ Tidak ada cuplikan data ditemukan untuk @{akun}")
                continue

            for i in range(min(5, len(snippets))):
                teks_cuitan = snippets[i].get_text().lower()
                link_tujuan = links[i]['href'] if i < len(links) else f"https://twitter.com/{akun}"

                for kw in kata_kunci:
                    if kw in teks_cuitan:
                        judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                        isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Konten:** {snippets[i].get_text()}\n\n**Tautan Akses:** {link_tujuan}\n\n*Segera tinjau dan balas menggunakan strategi terbaik Anda!*"
                        
                        kirim_notifikasi(judul, isi)
                        break

        except Exception as e:
            print(f"⚠️ Terkendala saat memproses @{akun}: {e}")

if __name__ == "__main__":
    mulai_intai_advanced()
