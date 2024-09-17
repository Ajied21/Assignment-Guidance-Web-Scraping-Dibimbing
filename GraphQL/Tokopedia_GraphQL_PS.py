import requests
import pandas as pd
import threading

# URL target dan header
url_target = 'https://gql.tokopedia.com/graphql/SearchProductQueryV4'

# Header HTTP untuk mengirimkan permintaan ke server Tokopedia
header = {
    'authority': 'gql.tokopedia.com',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.tokopedia.com',
    'referer': 'https://www.tokopedia.com',
    'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'tkpd-userid': '0',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, seperti Gecko) Chrome/108.0.0.0 Safari/537.36',
    'x-device': 'desktop-0.0',
    'x-source': 'tokopedia-lite',
    'x-tkpd-lite-service': 'zeus',
    'x-version': '68ba647'
}

# Fungsi untuk mengambil data dari satu halaman pencarian
def scrape_page(page, keyword, all_products):
    # Query GraphQL untuk mendapatkan data produk
    query = f'[{{"operationName":"SearchProductQueryV4","variables":{{"params":"device=desktop&navsource=&ob=23&page={page}\
              &q={keyword}&related=true&rows=60&safe_search=false&scheme=https&shipping=&source=search&srp_component_id=\
              04.06.00.00&srp_page_id=&srp_page_title=&st=&user_addressId=&user_cityId=&user_districtId=&user_id=&user_lat=\
              &user_long=&user_postCode=&user_warehouseId=&variants="}}, "query":"query SearchProductQueryV4($params: String!)\
              {{ ace_search_product_v4(params: $params) {{ data {{ products {{ id name price imageUrl rating countReview url shop \
              {{ city isOfficial isPowerBadge name }} }} }} }} }}"}}]'

    # Mengirim permintaan HTTP POST ke URL target dengan query
    response = requests.post(url_target, headers=header, data=query)
    response_data = response.json()

    # Mengambil data produk dari respons JSON
    products = response_data[0]['data']['ace_search_product_v4']['data']['products']
    all_products.extend(products)

# Fungsi utama untuk melakukan scraping dengan multithreading
def scrape_tokopedia_multithread(page_name, keyword):
    all_products = []
    threads = []
    
    # Membuat dan memulai 10 thread untuk scraping dari 10 halaman
    for page in range(1, 100):
        thread = threading.Thread(target=scrape_page, args=(page, keyword, all_products))
        threads.append(thread)
        thread.start()

    # Menunggu semua thread selesai
    for thread in threads:
        thread.join()

    # Membuat DataFrame dari produk yang di-scrape
    df = pd.DataFrame(all_products)

    # Menghapus prefix 'Rp' dari kolom 'price' dan mengonversinya ke tipe float
    df['price'] = df['price'].str.replace('Rp', '').str.replace('.', '').astype(float)

    # Memisahkan informasi 'shop' menjadi kolom terpisah
    df['location'] = df['shop'].apply(lambda x: x['city'])
    df['status_Official'] = df['shop'].apply(lambda x: x['isOfficial'])
    df['power_badge'] = df['shop'].apply(lambda x: x['isPowerBadge'])
    df['shop_name'] = df['shop'].apply(lambda x: x.get('name'))

    # Menghapus kolom 'shop' karena tidak diperlukan lagi
    df = df.drop(columns=['shop'])

    # Menambahkan kolom 'Brand' dan 'Variant'
    df['brand'] = "Sony"
    df['variant'] = "Playstation"

    # Mengganti nama kolom sesuai kebutuhan
    df = df.rename(columns={"countReview": "sold"})
    df = df.rename(columns={"imageUrl": "url_image"})
    df = df.rename(columns={"url": "url_shop"})

    # Menyusun ulang data untuk menyimpan hanya kolom yang diperlukan
    data_fixed = df[["id","name","brand","variant","power_badge","status_Official",
                    "location","shop_name","price","rating","sold","url_shop","url_image"]]
        
    # Konversi tipe data untuk kolom-kolom yang relevan
    data_fixed["id"] = data_fixed["id"].astype(int)
    data_fixed["name"]  = data_fixed["name"].astype(str)
    data_fixed["brand"] = data_fixed["brand"].astype(str)
    data_fixed["variant"] = data_fixed["variant"].astype(str)
    data_fixed["power_badge"] = data_fixed["power_badge"].astype(bool)
    data_fixed["status_Official"] = data_fixed["status_Official"].astype(bool)
    data_fixed["location"] = data_fixed["location"].astype(str)
    data_fixed["shop_name"] = data_fixed["shop_name"].astype(str)
    data_fixed["price"] = data_fixed["price"].astype(int)
    data_fixed["rating"] = data_fixed["rating"].astype(float)
    data_fixed["sold"] = data_fixed["sold"].astype(int)
    data_fixed["url_shop"] = data_fixed["url_shop"].astype(str)
    data_fixed["url_image"] = data_fixed["url_image"].astype(str)

    # Simpan hasil scraping ke file CSV dan JSON
    data_fixed.to_csv(f'{page_name}.csv', index=False)
    data_fixed.to_json(f'{page_name}.json', orient="records", indent=4)

    print(f"Data dari {keyword} telah berhasil disimpan ke {page_name}.csv dan {page_name}.json")


# Main function untuk menjalankan scraping
if __name__ == "__main__":

    try:
        # Scraping untuk produk PlayStation Console
        scrape_tokopedia_multithread('console_ps', 'playstation')

        # Scraping untuk produk CD PlayStation
        scrape_tokopedia_multithread('game_ps', 'cd%20playstation')

        print("Scraping website Tokopedia berhasil...")

    except Exception as e:
        # Menangkap dan mencetak pesan error jika ada kesalahan
        print(f"Terjadi kesalahan: {e}")
