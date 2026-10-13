import json
import os
import requests

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

def mulai_intai_universal():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Menjalankan radar dengan mesin pencari data universal...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    for akun in target_akun:
        print(f"🔍 Memindai lini masa publik untuk @{akun}...")
        try:
            # Menggunakan jalur agregator arsip terbuka universal yang aktif
            url_arsip = f"https://r.jina.ai/https://x.com/{akun}"
            
            response = requests.get(url_arsip, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"⚠️ Gagal menjangkau kanal @{akun} (Status: {response.status_code})")
                continue

            lines = response.text.split('\n')
            for line in lines:
                line_lower = line.lower()
                for kw in kata_kunci:
                    if kw in line_lower:
                        judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                        isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Konten Ditemukan:** {line.strip()}\n\n**Akun Target:** @{akun}\n\n*Segera tinjau dan balas menggunakan strategi terbaik Anda!*"
                        
                        kirim_notifikasi(judul, isi)
                        break

        except Exception as e:
            print(f"⚠️ Terkendala saat memproses @{akun}: {e}")

if __name__ == "__main__":
    mulai_intai_universal()
