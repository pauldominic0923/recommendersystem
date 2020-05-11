import requests
import time
from bs4 import BeautifulSoup
import re
import json
import urllib

switch_counter = 0
product_id = 0
constJSON=[{"store_name":"zara", "clothing":[]}]



def url_link(switch_counter):
    switcher = {
        0: 'https://www.zara.com/ca/en/man-special-prices-l806.html?v1=1445025',  # men special prices
        1: 'https://www.zara.com/ca/en/man-blazers-l608.html?v1=1445002', #men blazers
    }
    return switcher.get(switch_counter, "Invalid link")

while switch_counter < 2:
        page = requests.get(url_link(switch_counter))
        # Parse HTML and save to BeautifulSoup object
        soup = BeautifulSoup(page.text, 'html.parser')

        for i in range(len(soup.find_all('div', class_='product-info _product-info'))):  # 'a' tags are for items

            if url_link(switch_counter).replace('https://www.zara.com/ca/en', '').startswith("/woman") is True:
                product_gender = "FEMALE"
            elif url_link(switch_counter).replace('https://www.zara.com/ca/en', '').startswith("/man") is True:
                product_gender = "MALE"
            else:
                product_gender = "UNISEX"

            if switch_counter == 0:
                product_category = "BLAZERS"
            elif switch_counter == 1:
                product_category = "SKIRTS"
            else:
                product_category = "NOT AVAILABLE"


            product_name = soup.find_all('a', attrs={'class': 'name _item'})[i].text
            product_price_parse = soup.find_all("div", {"class": 'price _product-price'})[i].find_all("span", recursive=False)

            if str(product_price_parse).find("sale") != -1:
                marked_down = ("YES")

                original_price_text = str(
                    soup.find_all("div", {"class": 'price _product-price'})[i].find_next("span",recursive=False))
                original_price = float(re.sub("[^0123456789\.]", "", original_price_text).strip())

                product_price_text = str(
                    soup.find_all("div", {"class": 'price _product-price'})[i].find_next().find_next("span", recursive=False))
                product_price = float(re.sub("[^0123456789\.]", "", product_price_text).strip())

                discount_percent = round(((1-(product_price/original_price))*100),0)

            else:
                marked_down = ("NO")
                discount_percent = 0

                product_price_text = str(
                    (soup.find_all("div", {"class": 'price _product-price'})[i].find_all("span", recursive=False)))
                product_price = re.sub("[^0123456789\.]", "", product_price_text).strip()

            product_link = soup.find_all('a', attrs={'class': 'name _item'})[i]['href']
            # product_img_link = soup.find_all('img', attrs={'class': 'product-media _img _imgImpressions _imageLoaded'})[j]['src']

            # j = 0
            # visit_for_image = requests.get(product_link)
            # soup2 = BeautifulSoup(visit_for_image.text, 'html.parser')
            # product_img_link = soup2.find_all('meta', attrs={'property': 'og:image'})[j]['content']
            # ++j


            print("\nproduct ID:") + str(product_id)
            print("gender: ") + product_gender
            print("category: ") + product_category
            print ("name: ") + product_name
            #print ("product price_parse: ") + str(product_price_parse) #this is the main tag for prices, it shows the price whether is on sale or not, uncomment to check if 'product_price' is correct
            print ("marked-down: ") + marked_down
            print ("price: %f") % (float(product_price))
            print ("discount percent: ")+str(discount_percent)
            print ("link: ") + product_link
            #print ("imgage link: https://") + (product_img_link.replace('//','')) #removes the first '//' from image link

            dataDict = {
                    "product_id":str(product_id),
                    "gender":product_gender,
                    "category":product_category,
                    "name":product_name,
                    "sale": marked_down,
                    "discount percent":discount_percent,
                    "price":float(product_price),
                    "link":product_link,
                    #"img":(product_img_link.replace('//',''))
            }

            product_id += 1

            constJSON[0]["clothing"].append(dataDict)
            # #time.sleep(1.5)  # pause the code for 1.5 sec, so we dont get blocked for spamming

        print(json.dumps(constJSON))
        switch_counter += 1

        if switch_counter > 1:
            with open("zara.json", "w") as f:
                print(json.dumps(constJSON))
                json.dump(constJSON, f)




