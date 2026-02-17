import subprocess, json, os
from flask import Flask, request, render_template_string

app = Flask(__name__)

# 🔥 function: get direct video URL
def get_video_url(url):
    result = subprocess.run(
        ["yt-dlp", "-J", url],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    return data["formats"][-1]["url"]

# 🌐 Home page UI
@app.route("/")
def home():
    return '''
    <h2>YouTube Direct Downloader 📱</h2>
    <form action="/getlink" method="POST">
        <input name="link" placeholder="Paste YouTube link" style="width:300px">
        <button>Get Download Link</button>
    </form>
    '''

# 🎬 generate download link
@app.route("/getlink", methods=["POST"])
def get_link():
    link = request.form["link"]
    real_link = get_video_url(link)

    return f"""
    <h3>✅ Video Ready</h3>
    <a href="{real_link}">⬇️ Click here to download</a>
    <br><br>
    <a href="/">⬅️ Back</a>
    """

# 🔥 IMPORTANT for Render deployment (dynamic port)
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
