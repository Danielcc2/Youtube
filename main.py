from flask import Flask, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>Descargar Audio de YouTube</h1>
    <form method="POST" action="/descargar">
        <input type="text" name="url" placeholder="Introduce la URL de YouTube">
        <input type="submit" value="Descargar">
    </form>
    '''

@app.route('/descargar', methods=['POST'])
def descargar():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return send_file('audio.mp3', as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
