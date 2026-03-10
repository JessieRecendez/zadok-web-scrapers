# Pomellato
# 03-10-2026
# The products pages use a scroll down to upload more products into the pages.
##### So this loads ALL products by scrolling down then back up and keeps doing this
##### until no more products or page heights doesn't change anymore.
################################

# unicodes to watch for errors
# this might be a series of numbers incircled like a bullet point       \u2460 - \u2465 more to add maybe
# this is simply the degree symbol for the                              \u2103
# this is a simple bullet point black dot                               \u30fb
# this is just an empty space                                           \u2005
# this is the &nbsp;                                                    \xa0
# this is ~ a wavy dash used in approximate japanese price              \u301c
#

from bs4 import BeautifulSoup
import time, random, re
from csv import writer
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

STONE_MAP = {
    "citrine":          "Citrine",
    "tourmaline":       "Tourmaline",
    "tsavorite":        "Tsavorite",
    "malachite":        "Malachite",
    "jet":              "Jet",
    "garnet":           "Garnet",
    "emerald":          "Emerald",
    "peridot":          "Peridot",
    "ruby":             "Ruby",
    "amethyst":         "Amethyst",
    "agate":            "Agate",
    "turquoise":        "Turquoise",
    "diamond":          "Diamond",
    "rainbow-sapphire": "Rainbow Sapphire",
    "black-diamond":    "Black Diamond",
    "blue-diamond":     "Blue Diamond",
    "green-tourmaline": "Green Tourmaline",
    "pink-tourmaline":  "Pink Tourmaline",
    "red-carnelian":    "Red Carnelian"
}

# ==========================
# Logging Configuration
# ==========================
logging.basicConfig(
    filename='pomellato_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Pomellato scraper started")

driver = webdriver.Chrome()
url = "https://www.pomellato.com/us_en/pomellato-products/jewelry/discover-all"
delay = random.uniform(0, 1.5)
# Initialize a web driver (you may need to download a driver executable for your browser)
driver.get(url)

# ==========================
# Handle cookie popup
# ==========================
try:
    reject_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.ID, "onetrust-reject-all-handler"))
    )
    reject_button.click()
    logging.info("Cookie banner dismissed")
except TimeoutException:
    logging.info("No cookie banner found")

# ==========================
# Handle 'Load More' button loop
# ==========================
load_clicks = 0
while True:
    try:
        load_more = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-show-more-pagination"))
        )

        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", load_more)
        time.sleep(1)

        driver.execute_script("arguments[0].click();", load_more)

        load_clicks += 1
        logging.info(f"Clicked Load More ({load_clicks})")
        # Wait for new products to load
        time.sleep(3)

    except (TimeoutException, NoSuchElementException):
        logging.info("No more Load More button — all products loaded")
        break
    
# Get the page source and create a Beautiful Soup object
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Locate the product grid container
product_grid = soup.find("div", id="grid-products")

if not product_grid:
    logging.error("Product grid not found")
    driver.quit()
    exit()

# Extract products inside the grid
products = product_grid.select("div.grid-product")

logging.info(f"Total products detected: {len(products)}")

# save as file type in same folder
with open('pomellato.csv', 'w', encoding='utf-8', newline='') as f:
    thewriter = writer(f)
    header = ["SKU", "Hero Image", "URL", "Product Type", "MSRP", "Title", "Decription", "Collection", "Metal Type1", "Metal Type2", "Metal Type 3", "GemType1", "GemType2", "GemType3", "GemType4"]  # name columns
    thewriter.writerow(header)

    for product in products:
        # ==========================
        # Product Link
        # ==========================
        href = product.get("to")

        if not href:
            logging.warning("Missing product link")
            continue

        productLink = "https://www.pomellato.com" + href.replace("È", "E").replace('é', 'e')                                                                                                                                                                
            
        # ==========================
        # Hero Image
        # ==========================
        try:
            hero_tag = product.find('img')

            if hero_tag and hero_tag.get("src"):
                hero = hero_tag.get("src").replace("È", "E").replace('é', 'e').split("?")[0]
            else:
                hero = ""
                logging.warning(f"Missing hero image | URL={productLink}")

        except Exception as e:
            hero = ""
            logging.warning(f"Hero image error | URL={productLink} | {e}")
        
        # ==========================
        # Price
        # ==========================    
        price_tag = product.select_one("div.product-price p")

        if price_tag:
            price = price_tag.text.replace('$', '').replace(',', '').replace('\n', '').replace("\u301c", "").strip()
        else:
            price = ""
            logging.warning(f"Missing price | URL={productLink}")
        
        # ==========================
        # Title
        # ==========================   
        title_tag = product.select_one("p.product-name")

        if title_tag:
            productTitle = title_tag.text.replace('\u301c', '').replace("È", "E").replace("é", "e").strip()
        else:
            productTitle = ""
            logging.warning(f"Missing title | URL={productLink}")

        # ==========================
        # Product Type | Collections
        # ==========================
        titleMatch = r'\b(Ring|Bracelet|Bangle|Necklace|Pendant|Earrings|Ear Cuff|Earring)\b'
        collectionMatch = r'\b(Nudo|Brera|Victoria|Orsetto|Iconica|Pomellato Together|Pom Pom Dot|Sabbia|Catene|Fantina|M\'Ama Non M\'Ama)\b'
        productType = re.search(titleMatch, productTitle)
        # Extracting the found product type
        if productType:
            productType = productType.group(0)
        else:
            productType = ""
            
        # ==========================
        # Collections
        # ==========================
        collections = re.search(collectionMatch, productTitle)
        if collections:
            collections = collections.group(0)
        else:
            collections = ""

        # ==========================
        # SKU
        # ==========================
        try:
            sku_tag = product.find('img', class_='sc-iMWBiJ ehEtTy loaded')

            if sku_tag and sku_tag.get("src"):
                sku = sku_tag.get("src")
                filename = sku.split("/")[-1]

                match = re.match(r"([A-Za-z0-9]{7})_([A-Za-z0-9]{5})_([A-Za-z0-9]{5})", filename)

                if match:
                    newSKU = "_".join(match.groups())
                else:
                    newSKU = ""
                    logging.warning(f"SKU pattern not matched | URL={productLink}")
            else:
                newSKU = ""
                logging.warning(f"Missing SKU image | URL={productLink}")

        except Exception as e:
            newSKU = ""
            logging.warning(f"SKU extraction error | URL={productLink} | {e}")

        # make a request to the product page to get the SKU
        # Hence, click into each URL to get even more possible unique data
        # ==========================
        # Navigate to product page using Selenium
        # ==========================
        driver.get(productLink)
        time.sleep(1.5)  # small wait to let JS load

        # ==========================
        # Description
        # ==========================
        try:
            description_tag = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "p.ProductDescriptionSidebar__Description-sc-s1hh85-5")
                )
            )

            description = description_tag.text

            description = (description.replace('”', '"').replace('“', '"').replace("...", '').replace('\u2005', ' ').replace('\xa0', ' ').replace("’", "'").replace("‘", "'").replace('é', 'e'))

        except TimeoutException:
            description = ""
            logging.warning(f"Description not found for {productTitle}")

        # ==========================
        # Metals and Stones
        # ==========================
        metalType1 = metalType2 = metalType3 = ''
        stoneType1 = stoneType2 = stoneType3 = stoneType4 = ''

        try:
            component_div = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, 'div[class*="ProductComponent__BoxMaterials"]')
                )
            )
            component_paragraphs = component_div.find_elements(By.TAG_NAME, 'p')

            metals = []
            stones = []

            for p in component_paragraphs:
                text = p.text.strip().replace('18Kt', '18k').replace('18K', '18k').replace(',', '').replace('Rose Gold 18k', '18k Rose Gold').replace('White Gold 18k', '18k White Gold').replace('Yellow Gold 18k', '18k Yellow Gold')
                # Decide if it's a metal or a stone
                if re.search(r'\b(14k|18k|Platinum|Gold|White Gold|Rose Gold|Yellow Gold|Pink Gold)\b', text, re.IGNORECASE):
                    metals.append(text) 
                else:
                    stones.append(text)

            # Assign metals
            if len(metals) > 0:
                metalType1 = metals[0]
            if len(metals) > 1:
                metalType2 = metals[1]
            if len(metals) > 2:
                metalType3 = metals[2]

            # Assign stones
            if len(stones) > 0:
                stoneType1 = stones[0]
            if len(stones) > 1:
                stoneType2 = stones[1]
            if len(stones) > 2:
                stoneType3 = stones[2]
            if len(stones) > 3:
                stoneType4 = stones[3]

        except TimeoutException:
            logging.warning(f"Metals/Stones not found for {productLink}")

        # make sure they match in the same order with the header
        info = [newSKU, hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, '', stoneType1, stoneType2, stoneType3, stoneType4]
        thewriter.writerow(info)
        logging.info(f"Product scraped: SKU={newSKU} | Product Name={productTitle} | Price={price} | Link={productLink}")
# Close the web driver when we're done
logging.info("Pomellato scraper finished successfully")
driver.quit()
