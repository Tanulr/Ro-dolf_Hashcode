
from bs4 import BeautifulSoup as BS
import requests
from random import randint
from time import sleep


url = ['http://thepregnantchef.com/avocado-mango-and-kale-smoothie/', 'http://thepregnantchef.com/coconut-and-dark-chocolate-truffles/', 'http://thepregnantchef.com/easy-peasy-broccoli-soup/', 'http://thepregnantchef.com/chickpea-and-spinach-stew/']
for i in range(0,4):
    r = requests.get(url[i])
    soup = BS(r.content, 'lxml')
    print(soup.title.text)
    
    image = soup.find("meta", property="og:image")
    print(image["content"] if image else "No meta image given")


"""
url = 'http://thepregnantchef.com/avocado-mango-and-kale-smoothie/'
r = requests.get(url)
soup = BS(r.content, 'lxml')
print(soup.title.text)

#for item in soup.find_all('img'):
  #  print(item['src'])


image = soup.find("meta", property="og:image")
print(image["content"] if image else "No meta image given")
"""