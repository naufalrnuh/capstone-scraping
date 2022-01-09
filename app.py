from flask import Flask, render_template
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from bs4 import BeautifulSoup 
import requests

#don't change this
matplotlib.use('Agg')
app = Flask(__name__) #do not change this

#insert the scrapping here
url_get = requests.get('https://www.imdb.com/search/title/?release_date=2021-01-01,2021-12-31')
soup = BeautifulSoup(url_get.content,"html.parser")

#scraping
temp = []

for i in range(0,7):
    title = soup.find_all('div',attrs='lister-item-content')[i]
    titles = title.h3.a.text
    rating = soup.find_all('div',attrs='inline-block ratings-imdb-rating')[i]
    ratings = rating.text[2:5]
    metascore = soup.find_all('div',attrs='inline-block ratings-metascore')[i]
    metascores = metascore.text[1:3]
    vote = soup.find_all('div',attrs='lister-item-content')[i]
    votes = vote.select('p.sort-num_votes-visible > span:nth-child(2)')[0].text
    temp.append((titles,ratings,metascores,votes))

#change into dataframe
top7 = pd.DataFrame(temp, columns = ('Title', 'IMDb Rating', 'Metascores', 'Votes'))

#data cleaning
top7['IMDb Rating'] = top7['IMDb Rating'].astype('float64')
top7['Metascores'] = top7['Metascores'].astype('float64')
top7votes = top7['Votes'].values.tolist()
top7['Votes'] = top7votes
top7['Votes'] = top7['Votes'].astype('str')
top7['Votes'] = top7['Votes'].str.replace(',','')
top7['Votes'] = top7['Votes'].astype('float64')

#end of data cleaning 

@app.route("/")
def index(): 
	
	movie_data = f'{top7["Metascores"].mean().round(2)}' #be careful with the " and ' 

	# generate plot
	plt.bar(top7['Title'], top7['Metascores'])
	plt.title('Metascores of the top 7 films in 2021')
	ax1 = plt.xticks(rotation=90)
	
	# Rendering plot
	# Do not change this
	figfile = BytesIO()
	plt.savefig(figfile, format='png', transparent=True)
	figfile.seek(0)
	figdata_png = base64.b64encode(figfile.getvalue())
	plot_result = str(figdata_png)[2:-1]

	# render to html
	return render_template('index.html',
		movie_data = movie_data, 
		plot_result=plot_result
		)


if __name__ == "__main__": 
    app.run(debug=True)