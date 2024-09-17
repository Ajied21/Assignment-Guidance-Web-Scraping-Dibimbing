import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor

# Input URL untuk konsol PlayStation dan game PlayStation
url_console_playstation = "https://www.tokopedia.com/p/gaming/game-console/playstation"
url_game_playstation    = "https://www.tokopedia.com/p/gaming/cd-game/cd-playstation"

# Inisialisasi driver Chrome dengan opsi untuk memaksimalkan jendela browser
def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

# Fungsi untuk scraping data produk PlayStation dari halaman Tokopedia
def playstation(url_PS):
    click_pages = 5  # Jumlah halaman yang akan diklik
    list_product_ps = []  # List untuk menyimpan data produk

    if url_PS:  # Jika URL valid
        driver = init_driver()  # Inisialisasi driver
        driver.get(url_PS)  # Membuka URL

        # Tunggu hingga elemen halaman muncul
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#zeus-root')))
        time.sleep(3)  # Tambahan jeda untuk memastikan halaman termuat

        # Loop untuk melakukan scroll halaman
        for ps in range(click_pages):
            for page in range(18):
                driver.execute_script("window.scrollBy(0, 250)")  # Scroll ke bawah
                time.sleep(2)

            driver.execute_script("window.scrollBy(50, 0)")  # Scroll horizontal sedikit
            time.sleep(2)

            # Ambil source HTML halaman untuk di-parsing dengan BeautifulSoup
            soup_playstation = BeautifulSoup(driver.page_source, "html.parser")

            # Loop untuk mengambil setiap produk dari halaman
            for items in soup_playstation.findAll('div', class_="css-bk6tzz e1nlzfl2"):
                
                # Fungsi untuk mengambil nama produk
                def extract_name_product():
                    try:
                        name_tag = items.find('div', class_='css-ouykaq')
                        if name_tag:
                            names_tags = name_tag.find('img')
                            name_product = names_tags['alt'] if names_tags else "No Name"
                        else:
                            name_product = "No Name"
                    except Exception as e:
                        print(f"Error extracting name: {e}")
                        name_product = "Error"
                    return name_product

                # Fungsi untuk mengambil badge (contoh: official store, power merchant)
                def extract_badge(soup):
                    badge_map = {
                        "https://images.tokopedia.net/img/official_store_badge.png": "official store badge",
                        "https://images.tokopedia.net/img/power_merchant_badge.png": "power merchant badge",
                        "https://images.tokopedia.net/img/goldmerchant/pm_activation/badge/PM%20Pro%20Small.png": "gold merchant"
                    }

                    badge_element = soup.find('div', class_='css-1hy7m5k').find('img')
                    if badge_element:
                        badge_src = badge_element.get('src')
                        return badge_map.get(badge_src, "unknown badge")
                    else:
                        return "no badge"

                # Fungsi untuk mengambil harga produk
                def extract_price():
                    try:
                        prices = items.find("div", class_="css-pp6b3e")
                        if prices:
                            price_text = prices.get_text(strip=True)
                            price = price_text.replace('Rp', '').replace('.', '')
                            price = float(price) if price else None
                        else:
                            price = None
                    except Exception as e:
                        print(f"Error extracting price: {e}")
                        price = None
                    return price

                # Fungsi untuk mengambil rating produk
                def extract_rating():
                    try:
                        rating_imgs = items.find_all("img", class_="css-177n1u3", alt="star")
                        ratings = len(rating_imgs)
                        rating_value = float(ratings)
                        rating_values = round(rating_value, 1)
                    except Exception as e:
                        print(f"Error extracting rating: {e}")
                        rating_values = None
                    return rating_values

                # Fungsi untuk mengambil URL gambar produk
                def extract_images():
                    try:
                        name_tag = items.find('div', class_='css-ouykaq')
                        names_tags = name_tag.find('img')
                        images = names_tags['src'] if names_tags else "No Image"
                    except Exception as e:
                        images = "No Image"
                    return images
                
                # Memanggil fungsi-fungsi ekstraksi data
                name = extract_name_product()
                brand = "Sony"
                variant = "PlayStation"
                power_badge = extract_badge(soup_playstation)
                status_official = True jika "official store badge" ditemukan

                # Mengambil lokasi toko dan nama toko
                store_info = items.find("div", class_="css-vbihp9")
                if store_info:
                    location = store_info.findAll("span", class_="css-ywdpwd")[0].text
                    shop_name = store_info.findAll("span", class_="css-ywdpwd")[1].text
                else:
                    location = "Unknown"
                    shop_name = "Unknown"

                price = extract_price()  # Ambil harga
                rating = extract_rating()  # Ambil rating

                # Mengambil jumlah produk yang sudah terjual
                sold = items.find("div", class_="css-1riykrk")
                if sold:
                    span_element = sold.find("span")
                    if span_element:
                        sold = int(span_element.text.replace('(', '').replace(')', '').strip())
                    else:
                        sold = None
                else:
                    sold = None

                # Mengambil URL toko dan URL gambar produk
                url_shop = items.select_one("a").get("href").replace('""','')
                url_image = extract_images()

                # Menyimpan data produk ke dalam list
                list_product_ps.append(
                    (name, brand, variant, power_badge, status_official, 
                    location, shop_name, price, rating, sold, url_shop, url_image)
                )
                                        
            # Klik tombol halaman berikutnya jika ada
            if ps < click_pages - 1:
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
                    next_button.click()
                    time.sleep(3)
                except Exception as e:
                    print(f"Error clicking next button: {e}")
                    break
            
        driver.quit()  # Tutup driver setelah scraping selesai

        # Buat DataFrame dari list produk
        data_ps = pd.DataFrame(list_product_ps, columns=["name", "brand", "variant", "power_badge", 
                                                         "status_official", "location", "shop_name",
                                                         "price", "rating", "sold", "url_shop", "url_image"])

        print(data_ps)  # Tampilkan DataFrame
            
        return data_ps  # Return data dalam bentuk DataFrame
    
    return None

# Fungsi untuk menyimpan data ke dalam file CSV dan JSON
def save_data(data, url_PS):
    # Tentukan nama file berdasarkan URL yang digunakan
    if "playstation" in url_PS and "console" in url_PS:
        file_name = "console_PS"
    elif "playstation" in url_PS and "cd-game" in url_PS:
        file_name = "game_ps"
    else:
        file_name = "unknown_data"
    
    # Simpan data dalam format CSV
    csv_file_name = f"{file_name}.csv"
    data.to_csv(csv_file_name, index=False)
    print(f"Data telah disimpan ke {csv_file_name}")
    
    # Simpan data dalam format JSON
    json_file_name = f"{file_name}.json"
    data.to_json(json_file_name, orient="records", indent=4)
    print(f"Data telah disimpan ke {json_file_name}")

# Fungsi untuk menjalankan scraping secara multithreaded
def run_multithreaded_scraping(urls):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(playstation, urls))
    
    # Simpan setiap hasil scraping ke dalam file
    for data, url in zip(results, urls):
        if data is not None:
            save_data(data, url)

# Main function untuk menjalankan program
if __name__ == "__main__":
    
    urls = [url_console_playstation, url_game_playstation]
    run_multithreaded_scraping(urls)  # Jalankan scraping dengan multithreading
