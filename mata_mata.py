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

def mulai_intai_sindikasi():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Menjalankan radar menembus Cloudflare via API Sindikasi Resmi...")

    # Headers yang meniru identitas pemanggilan widget web standar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5'
    }

    for akun in target_akun:
        print(f"🔍 Memindai widget resmi @{akun}...")
        try:
            # Menggunakan endpoint resmi Twitter untuk embed timeline (kebal blokir IP)
            url_sindikasi = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{akun}"
            
            response = requests.get(url_sindikasi, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"⚠️ Gagal menjangkau sindikasi @{akun} (Status: {response.status_code})")
                continue

            # API Sindikasi merender struktur JSON di dalam HTML, kita ekstrak teks mentahnya
            teks_mentah = response.text.lower()

            for kw in kata_kunci:
                if kw in teks_mentah:
                    judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                    isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Kata Kunci:** {kw}\n**Akun Target:** @{akun}\n\n*Sistem mendeteksi aktivitas yang relevan. Segera buka X/Twitter untuk membalas menggunakan strategi terbaik Anda!*\n\n🔗 Tautan: https://twitter.com/{akun}"
                    
                    kirim_notifikasi(judul, isi)
                    break

        except Exception as e:
            print(f"⚠️ Terkendala saat memproses @{akun}: {e}")

if __name__ == "__main__":
    mulai_intai_sindikasi()
