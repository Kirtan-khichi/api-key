import random
import requests
from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

# URL to fetch free proxies
PROXY_URL = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text"

def get_random_proxy():
    # Fetch proxies from the given URL
    proxy_list = requests.get(PROXY_URL).text.splitlines()
    
    # Choose a random proxy from the list
    proxy = random.choice(proxy_list)

    # Parse the proxy protocol and address
    proxy_type, proxy_address = proxy.split('://')
    return {proxy_type: f"{proxy_type}://{proxy_address}"}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    video_id = request.form.get('video_id')

    # Get a random proxy from the list
    proxies = get_random_proxy()

    try:
        # Fetch the transcript using the provided video_id with proxy
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], proxies=proxies)
        
        # Combine transcript text into a single string
        # transcript_text = " ".join([entry['text'] for entry in transcript_list])
        return f"<h2>Transcript for video {video_id} and proxy used {proxies}:</h2><p>{transcript_list}</p>"
    
    except Exception as e:
        return f"<h2>Error fetching transcript for video {video_id}:</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)