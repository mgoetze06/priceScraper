from bs4 import BeautifulSoup
import requests
import json


def isAlreadyInJson(filename,newName):
    # Opening JSON file
    itemFound = False
    f = open(filename)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    for obj in data['objects']:
        #print(data)
        #print("isalready1")
        #print(obj)
        if itemFound==False:
            if obj['title']==newName:
                #print("is already there")
                itemFound = True
            else:
                itemFound = False
    return itemFound

# function to add to JSON
def write_json(new_data, filename, objects):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data[objects].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
          # default json file layout:
          # {"objects":[]}
          # new objects from ebay get added as an element to "object" root
          #

string1 = "https://www.ebay.de/sch/i.html?_nkw="
search = ["3d", "drucker"] #search terms
searchString = "+".join(search)
string2 = "&_udhi="
price = "40.00"
string3 = "&rt=nc&LH_PrefLoc=1'"

url = string1 + searchString + string2 + price + string3
data = requests.get(url)
#lenovos
#data = requests.get('https://www.ebay.de/sch/i.html?_nkw=lenovo+m92&_udhi=100.00&rt=nc&LH_PrefLoc=1')
soup = BeautifulSoup(data.text,'html.parser')


#element = soup.find('div', { 'class': 's-item__info clearfix' })
#title = element.find('h3', { 'class': 's-item__title' })
#title_2 = soup.find_all('h3', { 'class': 's-item__title' })


listitems = soup.find_all('li', { 'class': 's-item s-item__pl-on-bottom s-item--watch-at-corner' })
#infos = soup.find_all('div', { 'class': 's-item__info clearfix' })

for item in listitems:
    title = item.find('h3', { 'class': 's-item__title' })
    price = item.find('span', { 'class': 's-item__price' })
    purchase = item.find('span', { 'class': 's-item__purchase-options-with-icon' })
    shipping = item.find('span', { 'class': 's-item__shipping s-item__logisticsCost' })
    timeleft = item.find('span', { 'class': 's-item__time-left' })
    time = item.find('span', { 'class': 's-item__time-end' })
    bidCount = item.find('span', { 'class': 's-item__bids s-item__bidCount' })
    link = item.find('a', { 'class': 's-item__link' })
    

    #print(title.text, price.text,purchase.text,shipping.text,timeleft.text,time.text,bidCount.text)
    #print(title, price,purchase,shipping,timeleft,time,bidCount)
    float_price = float(price.text[4:].replace(',','.'))
    if float_price < 100:
        if bidCount is not None:
            print(title.text,price.text,bidCount.text,shipping.text,timeleft.text)
            #this is a new comment on line 34
            jsObject = {
                "title": title.text,
                "price": price.text,
                "purchase": purchase,
                "shipping": shipping.text,
                "timeleft": timeleft.text,
                "time": time,
                "bidCount": bidCount.text,
                "link": link['href']
            }
            if(isAlreadyInJson('data.json',title.text)):
                print("object is already in json")
            else:
                write_json(jsObject, 'data.json', 'objects')
                print("object added to json")
            #default json file layout:
            #{"objects":[]}
            #new objects from ebay get added as an element to "object" root
            #
            #
            #
        else:
            print("object not fitting parameters")
            #print(title.text, price.text, purchase.text)
        #print(link['href'])

    #with open('data.json', 'w') as f:
    #    json.dump(jsObject, f)
    #y = json.dumps(jsObject)
    #print(y)



#s-item__info clearfix
#print(title_2)

#for tr in tbody.find_all('tr'):
#	place = tr.find_all('td')[0].text.strip()

#https://automatetheboringstuff.com/2e/chapter14/
#google spreadsheet integration
#print()


