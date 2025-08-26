import streamlit as st
import requests
import re
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plot


def clean_text(text):
    text = re.sub(r'\[.*?\]', '', text) #Remove square brackets
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    text = re.sub(r'(?<!^)([A-Z])', r' \1', text) # Add space before capital letters (except at the start)
    return text

def to_wordcloud(list,title):
    wcstring = (' ').join(list)
    wc = WordCloud(width=800, height=400, background_color='white').generate(wcstring)
    st.subheader(f'Word Cloud for "{title}"')
    fig, ax = plot.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)


st.title("Genius Lyrics Word Cloud")
user_input = st.text_input("Enter Genius.com lyrics URL")
#user_input= input("Enter URL (Retrieve it from Genius.com): ")

url = user_input.strip()
if "genius" in url.lower():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    lyrics = soup.find('div', id= 'lyrics-root')
    title = soup.find('h1').text
    if lyrics:
        lyrics_text = lyrics.text
        word_start_index = re.search(r'\[.*?\]', lyrics_text).start() #find first verse etc
        result = lyrics_text[word_start_index:]
        result_list = result.split(" ")
        cleaned_list = [item for item in result_list if item != ""]
        to_wordcloud(cleaned_list,title)
    else:
        print("Cannot find lyrics!")
else:
    print("Must be from Genius!")

