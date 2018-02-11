from bs4 import BeautifulSoup as soup
from urllib.request import urlopen


# removing non ascii characters to avoid unicode conflicts with csv files
def reformat(text):
    return ''.join([i if ord(i) < 128 else '' for i in text])


itemToBeFound = "1070"
maxPrice = 35000
# Entering the main url
url = 'https://www.newegg.com/global/in/Video-Cards-Video-Devices/Category/ID-38'
page = urlopen(url)
page_html = page.read()
page.close()

# passing the html content into a beautifulsoup object
page_soup = soup(page_html, "html.parser")
# limiting the search to the class that contains item information
container = page_soup.findAll("div", {"class": "item-container"})

# The file which we write scraped content to
f = open("Products.csv", "w")
f.write("Brand, Product Name, Price\n")

# Iterating through the soup object for every line in the csv file
for item in container:
    # scraping the title and name from their respective tags
    brand = item.div.div.a.img["title"]

    item_container = item.findAll("a", {"class": "item-title"})
    # findall returns an array
    item_name = item_container[0].text

    item_price = item.findAll("li", {"class": "price-current"})
    price = item_price[0].text
    price = reformat(price).strip()

    # filtering for your item
    if itemToBeFound in item_name and (int(price.replace(',', '')) < maxPrice):
    # printing to console to check output
        print("Consider buying: " + item_name + "for " + price)
    print('Brand: ' + brand)
    print('Name: ' + item_name)
    print('Price: ' + str(price))

    # writing the final contents to the file
    f.write(brand.replace(",", "|") + "," + item_name.replace(",", "|") + "," + price.replace(",", "|") + "\n")

f.close()
