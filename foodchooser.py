import random
import requests 
from bs4 import BeautifulSoup
from requests_html import HTMLSession

def init_session(ZIP):
    SESSION = HTMLSession()
    URL = f'https://www.google.com/search?sca_esv=80979d232755066a&sca_upv=1&hl=en&tbs=lf:1,lf_ui:9&tbm=lcl&sxsrf=ACQVn0-HHIPhe-jDMfPHFL-EuEhFof2NmA:1712516433329&q=restaurant+near+{ZIP}&rflfq=1&num=10&sa=X&ved=2ahUKEwj5wrjt5LCFAxUVPUQIHWLxB_gQjGp6BAgfEAE&biw=1207&bih=827&dpr=1.5#rlfi=hd:;si:;mv:[[34.0465963,-117.81601669999998],[33.9946974,-117.8996284]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3mexican_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3american_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!1m4!1u22!2m2!21m1!1e1!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAlVT,lf:1,lf_ui:9'
    AGENT = SESSION.get(URL, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'})
    return AGENT

def get_food(AGENT):
    food_elements = AGENT.html.find("span.OSrXXb")
    restaurant_list = []
    for foods in food_elements:
        if(not(foods.text == 'Price' or foods.text == 'Rating' or foods.text == 'My Ad Center' or foods.text == 'Hours' or foods.text == 'Cuisine')):
            restaurant_list.append(foods.text)
    return restaurant_list

def get_rating(AGENT):
    ratings = AGENT.html.find("span.yi40Hd.YrbPuc")
    rating = []
    for curr_rating in ratings:
        rating.append(curr_rating.text)
    return rating

def get_cuisine_type():
    return

def food_chooser():
    return

ZIP = 91789
AGENT = init_session(ZIP)

'''
restaurant_list = get_food(AGENT)
rand = int(len(restaurant_list)*random.random())
print(get_food(AGENT))
print(get_rating(AGENT))
'''
