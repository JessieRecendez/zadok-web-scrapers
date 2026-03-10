# Suzanne Kalan
# 2023-05-31
# Next Page Type

# unicodes to watch for errors
# this might be a series of numbers incircled like a bullet point       \u2460 - \u2465 more to add maybe
# this is simply the degree symbol  for the                             \u2103
# this is a simple bullet point black dot                               \u30fb
# this is just an empty space                                           \u2005
# this is the &nbsp;                                                    \xa0
# this is ~ a wavy dash used in approximate japanese price              \u301c
#

import requests
from bs4 import BeautifulSoup
import re
from csv import writer

# double click to replace product type page
url = "https://suzannekalan.com/collections/earrings"
# "https://suzannekalan.com/collections/earrings"
# "https://suzannekalan.com/collections/rings"
# "https://suzannekalan.com/collections/necklaces"
# "https://suzannekalan.com/collections/bracelets"

next_page = 0   # always start at zero here, default sets it to the first page anyways

while True:
    next_page += 1
    response = requests.get(f"{url}?page={next_page}")
    soup = BeautifulSoup(response.content, "html.parser")

    products = soup.find_all('div', class_='ProductItem__Wrapper')

    # save as file type in same folder
    with open('suzanne_kalan_all.csv', 'w', encoding='utf-8', newline='') as f:
        thewriter = writer(f)
        header = ["SKU", "True SKU", "Hero Image", "URL", "Product Type", "MSRP", "Title", "Decription", "Collection", "Metal Type1", "Metal Type2", "Metal Type 3", "GemType1", "GemType2", "GemType3", "GemType4", "Shape", "Style", "Melee Stone Shape", "Link Type", "Clasp Type", "Earring Type", "Feature", "Melee Stone Continue"]  # name columns
        thewriter.writerow(header)

        if not products:
            break

        for product in products:
            productLink = "https://suzannekalan.com" + product.find('a').get("href")
            try:
                price = product.find('span', class_='boost-pfs-filter-product-item-regular-price').text.replace('$', '').replace(',', '').replace(".00", "").replace('\n', '')
            except:
                price = ""
                
            try:
                productTitle = productSoup.find("h1").text.replace('é', 'e')
            except:
                productTitle = ""
                
            hero = "https:" + product.find('img', class_="ProductItem__Image").get("data-src").replace('540x', "1080x")
            hero_without_extension = hero.split('?')[0] # remove everything after the ? after the file type

            # make a request to the product page to get the SKU
            productPage = requests.get(productLink)
            productSoup = BeautifulSoup(productPage.content, 'html.parser')
            try:
                description = productSoup.find('div', class_='Rte').find('p').text.replace('é', 'e').replace('\xa0', '').replace('\ufeff', '').replace('“', '"').replace('\u2005', ' ').replace('\n', '|')
            except:
                description = ''
                
            try:
                p_tags = productSoup.find('div', class_='Rte').find_all('p')
                if len(p_tags) > 1:
                    paraDescription = ' | '.join([tag.text.replace('é', 'e').replace('\xa0', '').replace('\ufeff', '').replace('“', '"').replace('\u2005', ' ').replace('\n', '|') for tag in p_tags[1:]])
                else:
                    paraDescription = ''
            except:
                paraDescription = ''
                
            try:
                hero = 'https:' + productSoup.find('a', class_='Product__SlideshowNavImage').get("href")
                hero = re.sub(r'\?.*', '', hero)
            except:
                hero = ""
            try:
                sku = productSoup.find('option').get('data-sku').replace('/n', '')
            except:
                sku = ""

            collectionMatch = r'\b(Amalfi|Nadima|Ann|Cierra|Classic|Golden Age|Bold|Frenzy|Shimmer|Short Stack|Princess|Inlay|Evil-Eye)\b'
            collections = re.search(collectionMatch, productTitle, re.IGNORECASE)
            if collections:
                collections = collections.group(0).title()
            else:
                collections = ""

            chainMatch = r'\b(Link|Paperclip|Rope|Braided|Cuban|Curb|Mariner|Rolo|Box)\b'
            chainType = re.search(chainMatch, paraDescription, re.IGNORECASE)
            if chainType:
                chainType = chainType.group(0).title()
            else:
                chainType = ""
                
            claspMatch = r'\b(Box Clasp|Spring Ring Clasp|Lobster Clasp|Magnetic Clasp|Slider Lock Clasp|Toggle Clasp|Fish Hook Clasp|Fold Over Clasp|Open Box Clasp|Bracelet Catch Clasp)\b'
            claspType = re.search(claspMatch, paraDescription, re.IGNORECASE)
            if claspType:
                claspType = claspType.group(0).title()
            else:
                claspType = ''

            productShapeMatch = r'\b(Butterfly|Bar|Ram Head|Door Knocker|Snake Head|Lion Head|Feather|Ice Pick|V|Safety Pin|Dog Bone|Clover|Horseshoe|Star|Lightning Bolt|Small Cirlce|Seashell|Dollar Sign|Lotus|Baseball|Soccer|Football|Basketball|Small Double Circle|Circle|Open Circle|Tablet|Leaf|Ribbon|Infinity|Peace Sign|Triangle|Square|Horse Shoe|Sunburst|Wishbone|Fish|Frog|Owl|Dog|Dog Bone|Arrow|Cat|Happy Face|Hamsa|Anchor|Palm Tree| Key|Skull & Crossbones|Skull|Skeleton|Flower|Heart|Slanted Heart|Open Heart|Locket|Bumble Bee|Dog Tag|Tassel|Snake|Cross|Circle|Starfish|Zipper|Texas|Boot)\b'
            itemShape = re.search(productShapeMatch, paraDescription, re.IGNORECASE)
            if itemShape:
                itemShape = itemShape.group(0).title()
            else:
                itemShape = ""

            ContinMatch = r'\b(Eternity)\b'
            meleeStoneCont = re.search(ContinMatch, paraDescription, re.IGNORECASE)
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

            productMatch = r'\b(Ring|Band|Bands|Bracelet|Bangle|Brooch|Cuff|Cufflinks|Necklace|Choker|Collar|Pendant|Earring|Earrings|Hoop|Hoops|Stud|Studs|Huggies|Charm|Charms)\b'
            productType = re.search(productMatch, productTitle, re.IGNORECASE)
            if productType:
                productType = productType.group(0).replace("Ring", "Fashion Ring").replace("Hoop", "Earrings").replace("Hoops", "Earrings").replace("Stud", "Earrings").replace("Studs", "Earrings").replace("Collar", "Necklace").replace('ss', 's').title()
            else:
                productType = ""

            earringTypeMatch = r'\b(Studs|Hoop|Hoops|Dangle|Drop|Chandelier|Cuff|Climber|Huggie|Huggies|Omega|Jacket)\b'
            productEarringType = re.search(earringTypeMatch, productTitle, re.IGNORECASE)
            if productEarringType:
                productEarringType = productEarringType.group(0).title()
            else:
                productEarringType = ""

            featureMatch = r'\b(Lariat|Flat-Link|Tennis|Stretch|Overpass|Bypass|Convertable|Graduated|Twist|Twisted|2 Row|3 Row|4 Row|Adjustable|Station|3 Station|4 Station|5 Station|6 Station|7 Station|15 Station|19 Staion|Flex|Zodiac)\b'
            featureType = re.search(featureMatch, productTitle, re.IGNORECASE)
            if featureType:
                featureType = featureType.group(0).replace('\n', '').strip().title()
            else:
                featureType = ''

            stoneMatch = r'\b(Red Mix|Green Mix|Blue Mix|Pink Mix|Purple Mix|Black Mix|Pastel Mix|Rainbow Mix|Apatite|Rainbow Sapphire|Morganite|Citrine|Orange Citrine|Black Diamond|Blue Diamond|Brown Diamond|Champagne Diamond|Green Diamond|Pink Diamond|Yellow Diamond|Diamond|\b(?!Cut Emerald\b)Emerald\b|Amazonite|Garnet|Green Tsavorite|Tsavorite|Rhodolite|Iolite|Black Jade|Green Jade|White Jade|Jade|Kunzite|Kyanite|Labradorite|Lapis|Lapis Lazuli|Green Malachite|Malachite|Hematite|Moonstone|Rainbow Moonstone|White Moonstone|Black Mother of Pearl|White Mother of Pearl|Mother of Pearl|Opal|Peridot|Agate|Green Amethyst|Amethyst|Chalcedony|Green Quartz|Lemon Quartz|Onyx|Green Onyx|Prasiolite|Black Night Quartz|Rose de France|Rose Quartz|Ruby|Black Sapphire|Blue Sapphire|Light Blue Sapphire|Dark Blue Sapphire|Green Sapphire|Pink Sapphire|Orange Sapphire|Purple Sapphire|White Sapphire|Yellow Sapphire|Black Spinel|Tanzanite|Topaz|Blue Topaz|English Blue Topaz|Green Envy Topaz|London Blue Topaz|Morganite Topaz|Pink Topaz|Sky Blue Topaz|Swiss Blue Topaz|White Topaz|Salmon Topaz|Green Tourmaline|Pink Tourmaline|Rubelite|Tourmaline|Turquoise|Red Carnelian)\b'
            stoneTypes = re.findall(stoneMatch, paraDescription, re.IGNORECASE)
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

            metalMatch = r'\b(14k White Gold|14k Yellow Gold|14k Rose Gold|14k Pink Gold|18k Yellow|18k White|18k Rose Gold|18k Pink Gold)\b'
            metalTypes = re.findall(metalMatch, paraDescription, re.IGNORECASE)
            metalType1 = ""
            metalType2 = ""
            metalType3 = ""
            if len(metalTypes) > 1:
                try:
                    metalType1 = metalTypes[0] + ' Gold'.replace(' Gold Gold', ' Gold').title()
                except:
                    metalType1 = ''
                try:
                    metalType2 = metalTypes[1].title() + ' Gold'.replace(' Gold Gold', ' Gold').title()
                except:
                    metalType2 = ''
                try:
                    metalType3 = metalTypes[2].title() + ' Gold'.replace(' Gold Gold', ' Gold').title()
                except:
                    metalType3 = ''
            else:
                try:
                    metalType1 = metalTypes[0].title() + ' Gold'.replace(' Gold Gold', ' Gold').title()
                except:
                    metalType1 = ''


            # make sure they match in the same order with the header
            info = [sku, '', hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, '', chainType, claspType, productEarringType, featureType, meleeStoneCont]
            # write the row to the output file
            thewriter.writerow(info)
            print(len(info))
            print(sku, '', hero, productLink, productType, price, productTitle, description, collections, metalType1, metalType2, metalType3, stoneType1, stoneType2, stoneType3, stoneType4, itemShape, productStyle, '', chainType, claspType, productEarringType, featureType, meleeStoneCont)
