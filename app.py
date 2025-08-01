from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

app = Flask(__name__)

@app.route('/transcript', methods=['GET'])
def transcript():
    video_id = request.args.get('video_id')
    if not video_id:
        return jsonify({'error': 'Missing video_id parameter'}), 400
    try:
        ytt_api = YouTubeTranscriptApi()
        ft = ytt_api.fetch(video_id, languages=['es', 'en'])
        full = " ".join([item['text'] for item in ft])
        return jsonify({'video_id': video_id, 'transcript': full})
    except TranscriptsDisabled:
        return jsonify({'error': 'Transcripts are disabled for this video'}), 403
    except NoTranscriptFound:
        return jsonify({'error': 'No transcript found for this video'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def home():
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
