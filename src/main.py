from scrape_twitter import TwitterBot # import the class TwitterBot from another file scrape_twitter
import streamlit as st
from dotenv import dotenv_values



config = dotenv_values(".env")
# text box for seaarch query
search_text = st.text_input('Search Topic', 'ipl')

# initialise an object of the class TwitterBot
bot = TwitterBot(config['TWITTER_UNAME'], config['TWITTER_PASS'])

bot.login()

# textbox for search topic
search_text = st.text_input('Search Topic', 'ipl')
bot.search_topic("IPL\n")

results = bot.collect_tweets()

st.write(results)

# terminate the object
bot.close()