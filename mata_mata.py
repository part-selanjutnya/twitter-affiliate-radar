import json
import os
import datetime
import requests

# 1. Baca Konfigurasi Kata Kunci
try:
    with open('config_twitter.json', 'r') as f:
        config = json.load(f)
except FileNotFoundError:
    print("File config_twitter.json tidak ditemukan!")
    exit()

if config.get("status_bot") == "OFF":
    print("Status bot sedang OFF. Pengintaian dihentikan.")
    exit()

# 2. Muat Database JSON yang ada
DB_FILE = 'data_target.json'
try:
    with open(DB_FILE, 'r') as f:
        database_target = json.load(f)
except FileNotFoundError:
    database_target = []

def simpan_ke_database(keyword_ditemukan, teks_konten, tautan_tujuan):
    waktu_sekarang = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Buat data baru
    data_baru = {
        "waktu": waktu_sekarang,
        "keyword": keyword_ditemukan,
        "konten": teks_konten,
        "link": tautan_tujuan
    }
    
    # Masukkan ke urutan paling atas (terbaru)
    database_target.insert(0, data_baru)
    
    # Batasi database maksimal 50 data terakhir agar tidak terlalu besar
    if len(database_target) > 50:
        database_target.pop()
        
    # Simpan kembali ke file JSON
    with open(DB_FILE, 'w') as f:
        json.dump(database_target, f, indent=4)
    print(f"✅ Data baru berhasil dimasukkan ke {DB_FILE}!")

def jalankan_radar_otomatis():
    kata_kunci = [k.lower() for k in config.get("kata_kunci", [])]
    target_akun = config.get("target_akun", [])
    
    print("🚀 Menjalankan radar pengintai untuk Command Center...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    # Menggunakan metode pemindaian arsip/sumber publik yang aman
    for akun in target_akun:
        print(f"🔍 Memindai aktivitas @{akun}...")
        try:
            # Menggunakan titik akses cache terbuka
            url_arsip = f"https://r.jina.ai/https://nitter.cz/{akun}"
            response = requests.get(url_arsip, headers=headers, timeout=15)
            
            if response.status_code == 200:
                lines = response.text.split('\n')
                for line in lines:
                    line_lower = line.lower()
                    for kw in kata_kunci:
                        if kw in line_lower:
                            # Cek apakah konten ini sudah ada di database agar tidak duplikat
                            sudah_ada = any(item['konten'] == line.strip() for item in database_target)
                            if not sudah_ada:
                                simpan_ke_database(kw, line.strip(), f"https://twitter.com/{akun}")
                            break
        except Exception as e:
            print(f"⚠️ Kendala pada @{akun}: {e}")

if __name__ == "__main__":
    jalankan_radar_otomatis()
