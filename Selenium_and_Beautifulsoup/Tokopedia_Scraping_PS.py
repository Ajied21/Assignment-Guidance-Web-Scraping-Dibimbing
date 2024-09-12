import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import json
from concurrent.futures import ThreadPoolExecutor

# Input URL PlayStation
url_console_playstation = "https://www.tokopedia.com/p/gaming/game-console/playstation"
url_game_playstation    = "https://www.tokopedia.com/p/gaming/cd-game/cd-playstation"

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def playstation(url_PS):
    
    click_pages = 5

    list_product_ps = []

    if url_PS:
        driver = init_driver()
        driver.get(url_PS)

        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#zeus-root')))
        time.sleep(3)

        for ps in range(click_pages):

            for page in range(18):
                driver.execute_script("window.scrollBy(0, 250)")
                time.sleep(2)
            
            driver.execute_script("window.scrollBy(50, 0)")
            time.sleep(2)

            # Ambil source halaman dengan BeautifulSoup
            soup_playstation = BeautifulSoup(driver.page_source, "html.parser")
            
            for items in soup_playstation.findAll('div', class_="css-bk6tzz e1nlzfl2"):

                def extract_name_product():

                    names = items.find('div', class_='css-ouykaq')
                    name_tag = names.find('img')
                    name_product = name_tag['alt']

                    return name_product

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

                def extract_price():

                    prices = items.find("div", class_="css-pp6b3e")
                    
                    if prices:
                        price_text = prices.get_text(strip=True)
                        price = price_text.replace('Rp', '').replace('.', '')
                    
                        try:
                            price = float(price)
                        except ValueError:
                            price = None
                    
                    else:
                        price = None
                    
                    return price

                def extract_rating():
                    
                    rating_imgs = items.find_all("img", class_="css-177n1u3", alt="star")
                    ratings = len(rating_imgs)
                    rating_value = float(ratings)
                    rating_values = round(rating_value, 1)
                    
                    return rating_values

                def extract_images():
                    
                    img = items.find('div', class_='css-ouykaq')
                    img_tag = img.find('img')
                    image = img_tag['src']

                    return image
                
                name            = extract_name_product()
                brand           = "Sony"
                variant         = "PlayStation"
                power_badge     = extract_badge(soup_playstation)
                status_official = True if "official store badge" in power_badge else False

                for store in items.findAll("div", class_="css-vbihp9"):
                    location    = store.findAll("span", class_="css-ywdpwd")[0].text
                    shop_name   = store.findAll("span", class_="css-ywdpwd")[1].text

                price           = extract_price()
                rating          = extract_rating() 
                sold            = items.find("div", class_="css-1riykrk")

                if sold:
                    span_element = sold.find("span")
                    if span_element:
                        sold = int(span_element.text.replace('(', '').replace(')', '').strip())
                    else:
                        sold = None
                else:
                    sold = None

                url_shop        = items.select_one("a").get("href").replace('""','')
                url_image       = extract_images()

                list_product_ps.append(
                (name, brand, variant, power_badge, status_official, 
                location, shop_name, price, rating, sold, url_shop, url_image)
                )
                                        
            if ps < click_pages - 1:
                try:
                    next_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label^='Laman berikutnya']")
                    next_button.click()
                    time.sleep(3)
                except Exception as e:
                    break
            
        driver.quit()

        data_ps = pd.DataFrame(list_product_ps, columns=["name", "brand", "variant", "power_badge", 
                                                         "status_official", "location", "shop_name",
                                                         "price","rating", "sold", "url_shop", "url_image"])

        print(data_ps)
            
        return data_ps
    
    return None

def save_data(data, url_PS):
    if "playstation" in url_PS and "console" in url_PS:
        file_name = "console_PS"
    elif "playstation" in url_PS and "cd-game" in url_PS:
        file_name = "game_ps"
    else:
        file_name = "unknown_data"
    
    csv_file_name = f"{file_name}.csv"
    data.to_csv(csv_file_name, index=False)
    print(f"Data telah disimpan ke {csv_file_name}")
    
    json_file_name = f"{file_name}.json"
    data.to_json(json_file_name, orient="records", indent=4)
    print(f"Data telah disimpan ke {json_file_name}")

def run_multithreaded_scraping(urls):
    with ThreadPoolExecutor() as executor:
        results = list(executor.map(playstation, urls))
    
    for data, url in zip(results, urls):
        if data is not None:
            save_data(data, url)

if __name__ == "__main__":
    
    urls = [url_console_playstation, url_game_playstation]
    run_multithreaded_scraping(urls)