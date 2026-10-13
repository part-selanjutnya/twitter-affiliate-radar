import json
import os
import requests
from xml.etree import ElementTree as ET

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

NITTER_INSTANCES = [
    "https://nitter.poast.org",
    "https://nitter.catsarch.com",
    "https://nitter.lucideer.com",
    "https://nitter.woodland.coffee"
]

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

def mulai_intai_tangguh():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])

    print("🚀 Memulai radar pengintaian dengan sistem multi-server tangguh...")

    for akun in target_akun:
        berhasil = False
        print(f"🔍 Menyelidiki kanal publik untuk @{akun}...")

        for instance in NITTER_INSTANCES:
            try:
                url_feed = f"{instance}/{akun}/rss"
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

                response = requests.get(url_feed, headers=headers, timeout=7)

                if response.status_code == 200:
                    root = ET.fromstring(response.content)
                    items = root.findall('.//item')

                    if items:
                        print(f"   Berhasil terhubung via server: {instance}")
                        for item in items[:5]:
                            title_elem = item.find('title')
                            link_elem = item.find('link')

                            if title_elem is None or link_elem is None:
                                continue

                            teks_tweet = title_elem.text.lower()
                            link_tweet = link_elem.text
                            for inst in NITTER_INSTANCES:
                                link_tweet = link_tweet.replace(inst, 'https://twitter.com')

                            for kw in kata_kunci:
                                if kw in teks_tweet:
                                    judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                                    isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Konten:** {title_elem.text}\n\n**Tautan Akses:** {link_tweet}\n\n*Segera buka tautan di atas dan balas menggunakan strategi terbaik Anda!*"

                                    kirim_notifikasi(judul, isi)
                                    break 

                        berhasil = True
                        break 
            except Exception:
                continue 

        if not berhasil:
            print(f"⚠️ Semua server alternatif gagal merespons untuk @{akun}.")

if __name__ == "__main__":
    mulai_intai_tangguh()
