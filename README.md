# Scraping Data Produk Tokopedia

<div style="text-align: center;">
    <img src="./images/Tokped.png" alt="Architecture Overview" width="500"/>
</div>

## Deskripsi

url tokopedia yang digunakan :

Console Playstation : https://www.tokopedia.com/p/gaming/game-console/playstation

<div style="text-align: center;">
    <img src="./images/PS.jpg" alt="Architecture Overview" width="500"/>
</div>__


Game Playstation    : https://www.tokopedia.com/p/gaming/cd-game/cd-playstation

<div style="text-align: center;">
    <img src="./images/game.jpg" alt="Architecture Overview" width="500"/>
</div>

Skrip ini digunakan untuk mengumpulkan data produk game konsol yang disukai para gamer khusus ya Playstation dari Tokopedia dengan dua metode berbeda:

1. **Selenium dan Beautifulsoap Web Scraping**: Menggunakan Selenium untuk mengakses dan mengambil data dari halaman web Tokopedia.
2. **GraphQL API Scraping**: Menggunakan GraphQL API Tokopedia untuk mengambil data produk secara langsung.

## Fitur

- **Selenium Web Scraping**:
  - Mengambil data produk dari halaman PlayStation Console dan CD PlayStation.
  - Menggunakan multithreading untuk meningkatkan kecepatan pengambilan data.
  - Menyimpan data dalam format CSV dan JSON.
  
- **GraphQL API Scraping**:
  - Mengambil data produk dari halaman pencarian Tokopedia menggunakan GraphQL API.
  - Menyimpan data dalam format CSV dan JSON.

## Cara Menggunakan

### Prasyarat

1. **Python**: Pastikan Python 3.x sudah terinstal di sistem Anda.
2. **Library**:
   - Untuk Selenium Web Scraping:
     ```bash
     pip install requests
     pip install pandas
     pip install selenium
     pip install beautifulsoup4
     ```
   - Untuk GraphQL API Scraping:
     ```bash
     pip install requests
     pip install pandas
     ```
3. **WebDriver**: Unduh dan pasang [ChromeDriver](https://sites.google.com/chromium.org/driver/) atau WebDriver lain yang sesuai dengan browser Anda.

### Konfigurasi

1. **Selenium dan Beautifulsoap**:
   - Sesuaikan URL target dalam skrip sesuai dengan kategori produk yang ingin diambil.
   - Pastikan WebDriver sesuai dengan versi browser yang Anda gunakan.

2. **GraphQL API Scraping**:
   - Sesuaikan parameter GraphQL API jika diperlukan, seperti header dan query.

### Menjalankan Skrip

1. **Selenium dan Beautifulsoap**:
   - Jalankan skrip menggunakan terminal atau code editor yang berlaku.
   - Skrip ini akan mengambil data dari halaman PlayStation Console dan CD PlayStation, lalu menyimpan data dalam format CSV dan JSON.

2. **GraphQL API Scraping**:
   - Jalankan skrip menggunakan terminal atau code editor yang berlaku.
   - Skrip ini akan mengambil data dari pencarian produk Tokopedia dengan GraphQL API dan menyimpan data dalam format CSV dan JSON.

### Struktur Data

- **CSV dan JSON**: Data yang diambil disimpan dalam dua format:
  - **CSV**: `console_ps.csv` dan `game_ps.csv`
  - **JSON**: `console_ps.json` dan `game_ps.json`

- **Kolom Data untuk Selenium dan Beautifulsoap**:
  - `name`: Nama produk
  - `brand`: Merek produk
  - `variant`: Varian produk
  - `power_badge`: Status badge power
  - `status_Official`: Status official
  - `location`: Lokasi toko
  - `shop_name`: Nama toko
  - `price`: Harga produk
  - `rating`: Rating produk
  - `sold`: Jumlah produk terjual
  - `url_shop`: URL toko
  - `url_image`: URL gambar produk__

- **Kolom Data untuk GraphQL API**:
  - `id`: ID produk
  - `name`: Nama produk
  - `brand`: Merek produk
  - `variant`: Varian produk
  - `power_badge`: Status badge power
  - `status_Official`: Status official
  - `location`: Lokasi toko
  - `shop_name`: Nama toko
  - `price`: Harga produk
  - `rating`: Rating produk
  - `sold`: Jumlah produk terjual
  - `url_shop`: URL toko
  - `url_image`: URL gambar produk
