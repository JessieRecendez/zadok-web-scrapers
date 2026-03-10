#Dinh Van Jewelry
#Scrapping everything we can as a starting brand
#
#


from bs4 import BeautifulSoup
import time
from csv import writer
from selenium import webdriver


##### Web scrapper for infinite scrolling page #####
driver = webdriver.Chrome()
driver.get("https://www.dinhvan.com/en_us/catalog/category/view/s/joaillerie/id/63/")
time.sleep(2)  # Allow 2 seconds for the web page to open
# You can set your own pause time. My laptop is a bit slow so I use 1 sec
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
i = 1

while True:
    # scroll one screen height each time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
    i += 1
    time.sleep(scroll_pause_time)
    # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
    scroll_height = driver.execute_script("return document.body.scrollHeight;")
    # Break the loop when the height we need to scroll to is larger than the total scroll height
    if (screen_height) * i > scroll_height:
        break
##### End of Web scrapper for infinite scrolling page #####

soup = BeautifulSoup(driver.page_source, 'html.parser')
lists = soup.find_all('div', class_="product-item-info")

with open('dinh_van_jewelry_add_on.csv',  'w', encoding = 'utf-8', newline = '') as f: #save as file type in same folder
  thewriter = writer(f)
  header = ["URL", "Title", "SubTitleText", "MSRP", "Hero Image"]  # name columns
  thewriter.writerow(header)

  for list in lists:  #what are we scrapping for?
      webLink = list.find('a').get('href')
      title = list.find('a', class_="product-item-link").text.replace('\n', '')
      subdesc = list.find('div', class_="product-subtitle").text.replace('\n', '')
      heroImage = list.find('img', class_="product-image-photo").get('src')
      price = list.find('span', class_="price").text.replace('$', '').replace(' ', '')
      
      # make sure they match in the same order with the header
      info = [price]
      thewriter.writerow(info)
      print(len(info))
