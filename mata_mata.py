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

def mulai_intai_stabil():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Menjalankan radar dengan jalur akses stabil...")

    # Menggunakan identitas peramban seluler standar
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'application/json,text/html'
    }

    for akun in target_akun:
        print(f"🔍 Menyelidiki aktivitas @{akun}...")
        try:
            # Menggunakan peladen proksi publik nitter alternatif yang ramah server
            url_target = f"https://nitter.poast.org/{akun}/rss"
            
            response = requests.get(url_target, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"⚠️ Jalur utama tertutup untuk @{akun} (Status: {response.status_code}). Mencoba jalur data cadangan...")
                # Jalur cadangan menggunakan arsip teks ringan
                url_backup = f"https://r.jina.ai/https://nitter.poast.org/{akun}"
                response = requests.get(url_backup, headers=headers, timeout=10)

            if response.status_code == 200:
                teks_data = response.text.lower()
                lines = response.text.split('\n')

                for line in lines:
                    line_lower = line.lower()
                    for kw in kata_kunci:
                        if kw in line_lower:
                            judul = f"🚨 TARGET: '{kw.upper()}' di @{akun}"
                            isi = f"**Peluang Afiliasi Terdeteksi!**\n\n**Konten Ditemukan:** {line.strip()}\n\n**Akun Target:** @{akun}\n\n*Segera tinjau dan balas menggunakan strategi terbaik Anda!*"
                            
                            kirim_notifikasi(judul, isi)
                            break
            else:
                print(f"⚠️ Gagal total menjangkau data untuk @{akun}")

        except Exception as e:
            print(f"⚠️ Terkendala saat memproses @{akun}: {e}")

if __name__ == "__main__":
    mulai_intai_stabil()
