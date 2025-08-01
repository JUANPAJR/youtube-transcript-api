from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/transcript', methods=['GET'])
def get_transcript():
    video_id = request.args.get('video_id')

    if not video_id:
        return jsonify({'error': 'video_id is required'}), 400

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es', 'es-419', 'en'])
        text = ' '.join([segment['text'] for segment in transcript])
        return jsonify({'transcript': text})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    return "YouTube Transcript API - Working"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
