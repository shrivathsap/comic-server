from flask import Flask, render_template
from bs4 import BeautifulSoup
import requests, urllib.request
import json

app = Flask(__name__)

image_list = []

websites = {"Popeye":'https://www.comicskingdom.com/popeye',
            "Hagar the horrible":'https://www.comicskingdom.com/hagar-the-horrible',
            "Blondie":'https://www.comicskingdom.com/blondie',
            "Marvin":'https://www.comicskingdom.com/marvin',
            "Moose and Molly":'https://www.comicskingdom.com/moose-and-molly',
            "Beetle Bailey":'https://www.comicskingdom.com/beetle-bailey-1',
            "Tiger":'https://www.comicskingdom.com/tiger'}

websites2 = {"Calvin and Hobbes":'https://www.gocomics.com/calvinandhobbes',
             "Peanuts":'https://www.gocomics.com/peanuts',
             "Pooch cafe":'https://www.gocomics.com/poochcafe',
             "Pearls before swine":'https://www.gocomics.com/pearlsbeforeswine',
             "Garfield":'https://www.gocomics.com/garfield',
             "Wumo":'https://www.gocomics.com/wumo'}

def update_list():
	with open('url_info.json', "r") as f:
		data = json.load(f)
	for key in list(websites.keys()):
		source = requests.get(websites[key]).text
		soup = BeautifulSoup(source, 'lxml')
		data[key]["url"] = soup.find('slider-image')['image-url']
		data[key]["alt"] = ""
		image_list.append(soup.find('slider-image')['image-url'])

	for key in list(websites2.keys()):
		source = requests.get(websites2[key]).text
		soup = BeautifulSoup(source, 'lxml')
		image = soup.find('div', class_ = "row").picture.img['data-srcset']
		data[key]["url"] = image.split(' ')[0]
		data[key]["alt"] = ""
		image_list.append(image.split(' ')[0])

	dilbert = requests.get('https://dilbert.com').text
	soup = BeautifulSoup(dilbert, 'lxml')
	data["Dilbert"]["url"] = soup.find('div', class_ = "img-comic-container").img['src']
	data["Dilbert"]["alt"] = ""

	xkcd = requests.get('https://xkcd.com').text
	soup = BeautifulSoup(xkcd, 'lxml')
	image = soup.find('div', id = "comic").img
	data["xkcd"]["url"] = 'https:{}'.format(image['src'])
	data["xkcd"]["alt"] = image['title']
	# r = requests.get('https:{}'.format(image['src']))
	# with open('xkcd.png', 'wb') as f:
	#     f.write(r.content)
	# print(image['alt'])
	# print(image['title'])
	with open('url_info.json', "w") as f:
		json.dump(data, f, indent=2)

# @app.route('/')
# def hello():
# 	if image_list == []:
# 		update_list()
# 	return render_template('home.html', title='Log in', url_list = image_list)
#
# if __name__ == "__main__":
# 	app.run(debug=True)
update_list()
