# Marco Bicego
# 2023-04-28
##### need to fix scraping extra, but empty variants while still scraping variants the way I want them
# REMEMBER Pomellato was unique as far as their page scroll goes!!!!!!!!!!!!!!!!!!!!!!!!!

# unicodes to watch for errors
# this might be a series of numbers incircled like a bullet point       \u2460 - \u2465 more to add maybe
# this is simply the degree symbol  for the                             \u2103
# this is a simple bullet point black dot                               \u30fb
# this is just an empty space                                           \u2005
# this is the &nbsp;                                                    \xa0
# this is ~ a wavy dash used in approximate japanese price              \u301c
# this is ® the registered sign                                         \u00AE
# this is Â letter a with a circumflex                                  \u00C2
#

import requests
from bs4 import BeautifulSoup
import time
import re
from csv import writer
from selenium import webdriver


driver = webdriver.Chrome()
url = "https://us.marcobicego.com/collections/all"
driver.get(url)

# Get the initial height of the page
prev_height = driver.execute_script("return document.body.scrollHeight")

# Keep scrolling down the page until the page height no longer increases
while True:
    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
    time.sleep(1)    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == prev_height:
        break
    
    # Update the previous height of the page
    prev_height = new_height
    
# Get the page source
page_source = driver.page_source
soup = BeautifulSoup(page_source, "html.parser")
products = soup.find_all('div', class_='product-related')

with open('marco_bicego.csv', 'w', encoding='utf-8', newline='') as f:
    thewriter = writer(f)
    header = ["SKU", "True SKU", "Base SKU", "Hero Image", "URL", "Product Type", "MSRP", "Title", "Decription", "Collection", "Metal Type1", "Metal Type2", "Metal Type 3", "GemType1", "GemType2", "GemType3", "GemType4", "Shape", "Style", "Melee Stone Shape", "Link Type", "Earring Type", "Feature", "Melee Stone Continue", "Variant Stone", "VariantSKU", "Variants Price", "Variant Image"]  # name columns
    thewriter.writerow(header)

    for product in products:
        productLink = "https://us.marcobicego.com" + product.find('a').get("href")
        try:
            hero = product.find('img', class_='main-image').get('src').replace('_large', '')
            hero = re.sub(r'\?.*', '', hero)
        except:
            hero = ""
        try:
            price = product.find('span', class_='product-price').text.replace('$', '').replace(',', '').replace(".00", "").replace('\n', '').replace("\u301c", "").strip()
        except:
            price = ""

        # Hence, click into each URL to get even more possible unique data
        productPage = requests.get(productLink)
        productSoup = BeautifulSoup(productPage.content, 'html.parser')
        
        try:
            productTitle = productSoup.find('h1', class_="title").text.replace("18K", "18k").replace('\n', '').replace("\u301c", "").replace('\u00C2', '').replace('\u00AE', '').replace("\u00AE", "").replace("é", "e")
        except:
            productTitle = ''
        try:
            sku = productSoup.find('label', class_='product-option-value').text.replace('\n', '')
        except:
            sku = ''
        try:
            baseSKU = productSoup.find('label', class_='product-option-value').text.replace('\n', '').replace(" Y ", " ").replace(" W ", " ").replace(" R ", " ").replace(" YW ", " ").replace(" WR ", " ").replace(" Y", " ").replace(" W", " ").replace(" YW", " ")
        except:
            baseSKU = ''
        try:
            description = productSoup.find('span', class_="description product-description").text.replace('18K', '18k').replace('é', 'e').strip()
            description = re.sub(r'\xa0*', '', description)
        except:
            description = ''
        
        collectionMatch = r'\b(Africa|Alta|Bi49|Cairo|Jaipur Color|Jaipur Gold|Lucia|Lunaria|Marrakech|Marrakech Onde|Masai & Goa|Paradise|Petali|Siviglia|Unico|Uomo)\b'
        collections = re.search(collectionMatch, productTitle, re.IGNORECASE)
        if collections:
            collections = collections.group(0).replace("Goa", "Masai & Goa").replace("Jaipur Link", "Jaipur Gold").replace("Jaipur Collection", "Jaipur Color")
        else:
            collections = ""

        chainMatch = r'\b(Link|Paperclip|Rope|Braided|Cuban|Curb)\b'
        chainType = re.search(chainMatch, productTitle, re.IGNORECASE)
        if chainType:
            chainType = chainType.group(0)
        else:
            chainType = ""

        productShapeMatch = r'\b(Butterfly|Bar|Small Cirlce|Small Double Circle|Circle|Open Circle|Tablet|Leaf|Ribbon|Infinity|Peace Sign|Triangle|Square|Horse Shoe|Sunburst|Wishbone|Fish|Frog|Owl|Dog|Dog Bone|Arrow|Cat|Happy Face|Hamsa|Anchor|Palm Tree| Key|Skull & Crossbones|Skull|Skeleton|Flower|Heart|Slanted Heart|Open Heart|Locket|Bumble Bee|Dog Tag|Tassel|Snake|Cross|Circle|Starfish|Zipper|Texas|Boot)\b'
        itemShape = re.search(productShapeMatch, productTitle, re.IGNORECASE)
        if itemShape:
            itemShape = itemShape.group(0)
        else:
            itemShape = ""

        ContinMatch = r'\b(Eternity)\b'
        meleeStoneCont = re.search(ContinMatch, productTitle, re.IGNORECASE)
        if meleeStoneCont:
            meleeStoneCont = meleeStoneCont.group(0)
        else:
            meleeStoneCont = ""

        styleMatch = r'\b(Braided|Cathedral|Chunky|Cluster|Halo|Double Halo|Double Prong|Double Shank|Split Shank|East West|Filigree|Floral|Kite Set|Knife Edge|Lattice|Milgrain|Ribbon|Rope|Scallop)\b'
        productStyle = re.search(styleMatch, productTitle, re.IGNORECASE)
        if productStyle:
            productStyle = productStyle.group(0)
        else:
            productStyle = ""

        earringTypeMatch = r'\b(Stud|Hoop|Dangle|Drop|Chandelier|Cuff|Climber|Huggie|Huggie|Omega)\b'
        productEarringType = re.search(
            earringTypeMatch, productTitle, re.IGNORECASE)
        if productEarringType:
            productEarringType = productEarringType.group(0)
        else:
            productEarringType = ""

        shapeMatch = r'\b(Butterfly|Bar|Leaf|Flower|Heart|Bumble Bee|Feather|Safety Pin|Dog Tag|Dog Bone|Clover|Snake|Horseshoe|Star|Lightning Bolt)\b'
        productShape = re.search(shapeMatch, productTitle, re.IGNORECASE)
        if productShape:
            productShape = productShape.group(0)
        else:
            productShape = ""

        shapeMatch = r'\b(Baguette|Round|Princess|Asscher|Cushion|Oval|Emerald|Radiant|Heart)\b'
        gemShape = re.search(shapeMatch, productTitle, re.IGNORECASE)
        if gemShape:
            gemShape = gemShape.group(0).strip()
        else:
            gemShape = ""

        productMatch = r'\b(Ring|Bracelet|Bangle|Brooch|Cuff|Cufflinks|Necklace|Choker|Collar|Pendant|Earring|Hoop|Stud|Earrings|Charm|Charms)\b'
        productType = re.search(productMatch, productTitle, re.IGNORECASE)
        if productType:
            productType = productType.group(0).replace("Ring", "Fashion Ring").replace("Hoop", "Earrings").replace("Stud", "Earrings").replace("Collar", "Necklace")
        else:
            productType = ""

        featureMatch = r'\b(Lariat|Flat-Link|Tennis|Stretch|Overpass|Bypass|Convertable|Graduated|Twist|Twisted|2 Row|3 Row|4 Row|Adjustable|Station|3 Station|4 Station|5 Station|6 Station|7 Station|15 Station|19 Staion|Flex|Zodiac)\b'
        featureType = re.search(featureMatch, productTitle, re.IGNORECASE)
        if featureType:
            featureType = featureType.group(0).replace('\n', '').strip()
        else:
            featureType = ''
        
        stoneMatch = r'\b(Apatite|Rainbow Sapphire|Morganite|Citrine|Orange Citrine|Black Diamond|Blue Diamond|Brown Diamond|Champagne Diamond|Green Diamond|Pink Diamond|Yellow Diamond|Diamond|Emerald|Amazonite|Garnet|Green Tsavorite|Tsavorite|Rhodolite|Iolite|Black Jade|Green Jade|White Jade|Jade|Kunzite|Kyanite|Lapis|Lapis Lazuli|Green Malachite|Malachite|Hematite|Moonstone|Rainbow Moonstone|White Moonstone|Black Mother of Pearl|White Mother of Pearl|Mother of Pearl|Opal|Peridot|Agate|Green Amethyst|Amethyst|Chalcedony|Green Quartz|Lemon Quartz|Onyx|Prasiolite|Black Night Quartz|Rose de France|Rose Quartz|Ruby|Black Sapphire|Blue Sapphire|Light Blue Sapphire|Dark Blue Sapphire|Green Sapphire|Pink Sapphire|Orange Sapphire|Purple Sapphire|White Sapphire|Yellow Sapphire|Black Spinel|Tanzanite|Blue Topaz|English Blue Topaz|Green Envy Topaz|London Blue Topaz|Morganite Topaz|Pink Topaz|Sky Blue Topaz|Swiss Blue Topaz|White Topaz|Topaz|Green Tourmaline|Pink Tourmaline|Rubelite|Tourmaline|Turquoise|Red Carnelian)\b'
        stoneTypes = re.findall(stoneMatch, productTitle, re.IGNORECASE)
        stoneType1 = ""
        stoneType2 = ""
        stoneType3 = ""
        stoneType4 = ""
        if len(stoneTypes) > 1:
            try:
                stoneType1 = stoneTypes[0].title()
            except:
                stoneType1 = ''
            try:
                stoneType2 = stoneTypes[1].title()
            except:
                stoneType2 = ''
            try:
                stoneType3 = stoneTypes[2].title()
            except:
                stoneType3 = ''
            try:
                stoneType4 = stoneTypes[3].title()
            except:
                stoneType4 = ''
        else:
            try:
                stoneType1 = stoneTypes[0].title()
            except:
                stoneType1 = ''

        metalMatch = r'\b(14k White Gold|14k Yellow Gold|14k Rose Gold|14k Pink Gold|14k Gold|18k Yellow|18k White|18k Yellow and white|18k Yellow Gol& white|18k Gold|18k White Gold|18k Yellow Gold|18k Rose Gold|18k Pink Gold|Platinum)\b'
        metalTypes = re.findall(metalMatch, productTitle, re.IGNORECASE)
        metalType1 = ""
        metalType2 = ""
        metalType3 = ""
        if len(metalTypes) > 1:
            try:
                metalType1 = metalTypes[0]
            except:
                metalType1 = ''
            try:
                metalType2 = metalTypes[1]
            except:
                metalType2 = ''
            try:
                metalType3 = metalTypes[2]
            except:
                metalType3 = ''
        else:
            try:
                metalType1 = metalTypes[0]
            except:
                metalType1 = ''
                
        variations = productSoup.find('div', class_='stackable-stone-icon-list')
                        
        for variation in variations:
            try:
                variantHero = variation.find('div', class_='stackable-stone-icon').get('data-variant-image')
                variantHero = re.sub(r'\?.*', '', hero)
            except:
                variantHero = ''
            try:
                variantTitle = variation.find('div', class_='stackable-stone-icon').get('title')
            except:
                variantTitle = ''
            try:
                variantSku = variation.find('div', class_='stackable-stone-icon').get('data-variant-sku')
            except:
                variantSku = ''
            try:
                variantMSRP = variation.find('div', class_='stackable-stone-icon').get('data-display-price').replace('$', '').replace(',', '').replace(".00", "").replace('\n', '').replace("\u301c", "")
            except:
                variantMSRP = ''
            
            info = [sku, '', baseSKU, hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, gemShape, chainType, productEarringType, featureType, meleeStoneCont, variantTitle, variantSku, variantMSRP, variantHero]
            # write the row to the output file
            thewriter.writerow(info)
            print(len(info))
            print(sku, '', baseSKU, hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, gemShape, chainType, productEarringType, featureType, meleeStoneCont, variantTitle, variantSku, variantMSRP, variantHero)

# Close the web driver when we're done
driver.quit()
