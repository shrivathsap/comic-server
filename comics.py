from flask import Flask, render_template
from bs4 import BeautifulSoup
import json, requests, warnings
from datetime import datetime

#ideally i shouldn't do this, but i'm burned out and i don't really care. But THE warning that occurs is about not verifying SSL certificates...
warnings.simplefilter("ignore")

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

def date_to_nicer_date(date_string, slash):#expects YYYY/MM/DD if slash == 1, and YYYY-MM-DD if slash==0
	if slash==1:
		date = datetime.strptime(date_string, '%Y/%m/%d')
	elif slash == 0:
		date = datetime.strptime(date_string, '%Y-%m-%d')
	else:
		pass
	return date.strftime('%A, %B %d, %Y')

def update_list():
	with open('url_info.json', "r") as f:
		data = json.load(f)
	for key in list(websites.keys()):
		try:#so far comicskingdom has had issues with SSL certificate verifications
			source = requests.get(websites[key]).text
		except:
			source = requests.get(websites[key], verify=False).text
		soup = BeautifulSoup(source, 'lxml')
		#data[key]["url"] = soup.find('slider-image')['image-url']
		data[key]["url"] = soup.find('div', class_="comic").img['src']#they changed the HTML and somehow didn't set up SSL certificate properly
		data[key]["alt"] = ""
		image_list.append([key, (soup.find('li', class_='comic-date').text), soup.find('div', class_="comic").img['src'],'', websites[key]])

	for key in list(websites2.keys()):
		source = requests.get(websites2[key]).text
		soup = BeautifulSoup(source, 'lxml')
		image = soup.find('div', class_ = "row").picture.img['data-srcset']
		date = soup.find('div', class_ = "row").find_all('a')[0]['href'][-10:]#getting date of comic bruteforce
		nicer_date = date_to_nicer_date(date, 1)
		data[key]["url"] = image.split(' ')[0]
		data[key]["alt"] = ""
		image_list.append([key, nicer_date, image.split(' ')[0],'', websites2[key]])

	dilbert = requests.get('https://dilbert.com').text
	soup = BeautifulSoup(dilbert, 'lxml')
	dilbert_url = soup.find('div', class_ = "img-comic-container").img['src']
	dilbert_date = date_to_nicer_date(soup.find('div', class_ = "img-comic-container").a['href'][-10:], 0)
	dilbert_desc = soup.find('div', class_ = "img-comic-container").img['alt']
	data["Dilbert"]["url"] = soup.find('div', class_ = "img-comic-container").img['src']
	data["Dilbert"]["alt"] = ""
	image_list.append(['Dilbert', dilbert_date, dilbert_url, dilbert_desc, 'https://dilbert.com'])

	xkcd = requests.get('https://xkcd.com').text
	soup = BeautifulSoup(xkcd, 'lxml')
	image = soup.find('div', id = "comic").img
	image_list.append(['xkcd', image['alt'], 'https:{}'.format(image['src']), image['title'], 'https://xkcd.com'])
	data["xkcd"]["url"] = 'https:{}'.format(image['src'])
	data["xkcd"]["alt"] = image['title']
	with open('url_info.json', "w") as f:
		json.dump(data, f, indent=2)

@app.route('/')
def hello():
	if image_list == []:
		update_list()
	return render_template('home.html', image_list = image_list)

if __name__ == "__main__":
	app.run(debug=True)
update_list()
