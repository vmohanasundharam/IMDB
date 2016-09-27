from __future__ import division
import requests
import json
from bs4 import BeautifulSoup
class IMDBparser:

	all_movies_details={}
	mov_list=[]
	final_list={}
	count=0
	user_gen=[['Love','Action','Drama'],[0,0,0]]

	def __init__(self,mov_list):
		self.movies_list=mov_list
		self.mov_list=mov_list
		self.movies_count=len(mov_list)
	
	
	def prioritizing_movies(self):
		self.final_list=sorted(self.all_movies_details.items(), key=lambda a: a[1]['sys_rating'], reverse=True)
		return self.final_list


	def calculate_genre_rating(self):
		for allmovies in self.all_movies_details:
			self.count=0
			genval=0
			for usergen in self.user_gen[0]:
				for movgen in self.all_movies_details[allmovies]["movie_genre"]:
					if usergen == movgen:
						self.count = self.count + self.user_gen[1][genval]
				genval +=  1
			self.all_movies_details[allmovies]["sys_rating"] += float(self.count)
			
	
	def init_user_genre(self,usr_gen):
			self.user_gen=usr_gen

	
	def get_each_movie_name(self):
		
		for movies in self.movies_list:
			id=self.get_movie_id(movies)
			info=self.get_movie_details(id)			
			self.all_movies_details.update({movies:info})
		

	def get_movie_id(self,movie_name):
		results = requests.get('http://www.omdbapi.com/?t='+movie_name+'&y=&plot=short&r=json')
		dictionary = json.loads(results.content)
		movie_id=str(dictionary["imdbID"])
		return movie_id

	def get_movie_details(self,movie_id):

		results = requests.get('http://www.imdb.com/title/'+movie_id)
		soup = BeautifulSoup(results.content,"html.parser")
		genre_list = self.get_movie_genre(soup)
		r_val = self.get_rating(soup)
		meta_score = self.get_meta_score(soup)
		year = self.get_release_year(soup)
		name = self.get_movie_name(soup)
		our_rate = (year/1000)+(r_val/10)+(meta_score/100)

		dic={'movie_name':name,
		'movie_rating':r_val,
		'movie_genre':genre_list,
		'movie_year':year,
		'movie_meta_score':meta_score,
		'sys_rating':our_rate}
		return dic

	def get_movie_name(self, soup):
		name = soup.find('h1',attrs={"itemprop":"name"})
		name=name.text
		return name

	def get_rating(self, soup):
		r_val = soup.find('span',attrs={"itemprop":"ratingValue"})
		r_val=float(str(r_val.text))
		return r_val

	def get_release_year(self, soup):
		year = soup.find('span',attrs={"id":"titleYear"})
		year = year.find('a')
		year = int((year.text).strip())
		return year

	def get_meta_score(self, soup):
		meta_score = soup.find('div',attrs={"class":"metacriticScore score_favorable titleReviewBarSubItem"})
		meta_score1 = soup.find('div',attrs={"class":"metacriticScore score_mixed titleReviewBarSubItem"})
		m_score = -1
		c = len(str(meta_score))
		c1 = len(str(meta_score1))
		if ((c == 4) & (c1==4) ):
			m_score = 0
		elif(c==4):
			meta_score1 = str(meta_score1.text.strip())
			meta_score1 = int(meta_score1)
			m_score = meta_score1
		else :
			meta_score = str(meta_score.text.strip())
			meta_score = int(meta_score)
			m_score = meta_score
		
		return m_score

	def get_movie_genre(self, soup):
		genre = soup.find('div',attrs={"itemprop":"genre"})
		genre_li=genre.find_all('a')
		length=len(genre_li)
		i=0
		genre_list=[]

		for gen in genre_li:
			genre_list.append(str(gen.text).strip())

		return genre_list	

	

movie_list=['Suicide Squad','The Age of Adaline','pk']
user_genre = [['Love','Action','Sci-Fi','Drama','Romance'],[1,2,3,4,5]]
obj=IMDBparser(movie_list)
obj.get_each_movie_name()
obj.init_user_genre(user_genre)
obj.calculate_genre_rating()
res=obj.prioritizing_movies()
for r in res:
	print r