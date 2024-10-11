from flask import Flask, render_template, request
from youtube_transcript_api import YouTubeTranscriptApi

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_transcript', methods=['POST'])
def get_transcript():
    video_id = request.form.get('video_id')

    # Proxy configuration (replace with actual proxy details if needed)
    proxies = {
        'http': 'http://189.124.85.217:7171',
    }

    try:
        # Fetch the transcript using the provided video_id
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'], proxies=proxies)
        
        # Combine transcript text into a single string
        # transcript_text = " ".join([entry['text'] for entry in transcript_list])
        return f"<h2>Transcript for video {video_id}:</h2><p>{transcript_list}</p>"
    
    except Exception as e:
        return f"<h2>Error fetching transcript for video {video_id}:</h2><p>{str(e)}</p>"

if __name__ == '__main__':
    app.run(debug=True)
