from flask import Flask, render_template, request
import requests
import re
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import io
import base64

app = Flask(__name__)

def clean_text(text):
    text = re.sub(r'\[.*?\]', '', text)  # Remove square brackets
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    text = re.sub(r'(?<!^)([A-Z])', r' \1', text)  # Add space before capital letters
    return text

def generate_wordcloud(word_list, title,number):
    wcstring = ' '.join(word_list)
    wc = WordCloud(max_words= int(number),width=800, height=400, background_color='white').generate(wcstring)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wc, interpolation='bilinear')
    ax.axis('off')
    ax.set_title(f'Word Cloud for the top {number} lyrics of "{title}"', fontsize=16)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    img_data = base64.b64encode(buf.read()).decode('utf-8')
    plt.close(fig)
    return img_data

@app.route('/', methods=['GET', 'POST'])
def index():
    img_data = None
    title = None
    error = None

    if request.method == 'POST':
        url = request.form['url'].strip()
        number = request.form['number'].strip()
        if "genius" in url.lower():
            try:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                title_tag = soup.find('h1')
                lyrics_divs = soup.find_all('div',id='lyrics-root')
                if lyrics_divs:
                    for div in lyrics_divs:
                        text = div.get_text().strip()
                        match = re.search(r'\[.*?\]', text)
                        if match:
                            lyrics_text = text[match.start():] if match else text
                            break

                    title = title_tag.text.strip() if title_tag else "Untitled"

                    result_list = lyrics_text.split(" ")
                    cleaned_list = [item for item in result_list if item]
                    cleaned_text = clean_text(' '.join(cleaned_list)).split()
                    img_data = generate_wordcloud(cleaned_text, title,number)
                else:
                    error = "Cannot find lyrics!"
            except Exception as e:
                error = f"Error: {e}"
        else:
            error = "Must be a Genius.com URL!"

    return render_template('index.html', img_data=img_data, title=title, error=error)

if __name__ == '__main__':
    app.run(debug=True)