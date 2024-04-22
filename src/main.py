from scrape_twitter import TwitterBot
import streamlit as st
from dotenv import dotenv_values

config = dotenv_values(".env")
bot = TwitterBot(config['TWITTER_UNAME'], config['TWITTER_PASS'])
bot.login()
bot.search_topic("IPL\n")
results = bot.collect_tweets()
st.write(results)
bot.close()