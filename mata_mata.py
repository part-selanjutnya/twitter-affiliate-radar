import json
import os
import requests
from xml.etree import ElementTree as ET

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

# Daftar peladen komunitas RSSHub publik yang aktif
RSSHUB_INSTANCES = [
    "https://rsshub.rssforever.com",
    "https://rsshub.moeyy.cn",
    "https://rss.shab.fun",
    "https://rss.mxd.cx",
    "https://rsshub.ktachibana.party"
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

def mulai_intai_rsshub():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Menjalankan radar melalui arsitektur multi-jembatan RSSHub...")

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

    for akun in target_akun:
        print(f"🔍 Mencari jalur yang bersih untuk @{akun}...")
        berhasil = False
        
        # Coba setiap jembatan satu per satu (Failover mechanism)
        for instance in RSSHUB_INSTANCES:
            try:
                url_rss = f"{instance}/twitter/user/{akun}"
                response = requests.get(url_rss, headers=headers, timeout=12)
                
                if response.status_code == 200:
                    print(f"   Terhubung melalui jembatan: {instance}")
                    root = ET.fromstring(response.content)
                    items = root.findall('.//item')
                    
                    for item in items[:5]: # Batasi 5 cuitan terbaru
                        title_elem = item.find('title')
                        link_elem = item.find('link')
                        
                        if title_elem is None or link_elem is None:
                            continue
                        
                        teks_cuitan = title_elem.text.lower()
                        link_tujuan = link_elem.text
                        
                        for kw in kata_kunci:
                            if kw in teks_cuitan:
                                judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                                isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Konten:** {title_elem.text}\n\n**Tautan Akses:** {link_tujuan}\n\n*Segera balas menggunakan strategi terbaik Anda!*"
                                
                                kirim_notifikasi(judul, isi)
                                break 
                    
                    berhasil = True
                    break # Hentikan loop instans jika sudah berhasil mendapat data
                
            except Exception:
                continue # Lanjut ke jembatan berikutnya jika gagal/timeout
        
        if not berhasil:
            print(f"⚠️ Semua jembatan gagal menembus keamanan untuk @{akun} saat ini.")

if __name__ == "__main__":
    mulai_intai_rsshub()
