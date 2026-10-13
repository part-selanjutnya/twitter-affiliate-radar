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

def mulai_intai_api_terbuka():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Menjalankan radar dengan proksi API terbuka...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/json'
    }

    for akun in target_akun:
        print(f"🔍 Menyelidiki aktivitas @{akun}...")
        try:
            # Menggunakan API publik alternatif berbasis pembaca RSS universal
            url_api = f"https://api.allorigins.win/get?url=https://vxtwitter.com/{akun}"
            
            response = requests.get(url_api, headers=headers, timeout=15)
            
            if response.status_code != 200:
                print(f"⚠️ Gagal menjangkau kanal @{akun} (Status: {response.status_code})")
                continue

            data_json = response.json()
            teks_konten = data_json.get('contents', '').lower()

            for kw in kata_kunci:
                if kw in teks_konten:
                    judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                    isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Akun Target:** @{akun}\n\n*Segera tinjau linimasa akun tersebut dan balas menggunakan strategi terbaik Anda!*"
                    
                    kirim_notifikasi(judul, isi)
                    break

        except Exception as e:
            print(f"⚠️ Terkendala saat memproses @{akun}: {e}")

if __name__ == "__main__":
    mulai_intai_api_terbuka()
