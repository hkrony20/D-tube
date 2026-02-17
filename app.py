import subprocess, json, os
from flask import Flask, request

app = Flask(__name__)

# 🔥 function: get direct video URL safely
def get_video_url(url):
    try:
        result = subprocess.run(
            ["yt-dlp", "-J", url],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return None

        data = json.loads(result.stdout)

        # best format url খুঁজে বের করা
        for f in reversed(data["formats"]):
            if "url" in f:
                return f["url"]

        return None

    except Exception as e:
        print("Error:", e)
        return None


# 🌐 Home page
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

    if not real_link:
        return "<h3>❌ Failed to fetch video link</h3><a href='/'>Back</a>"

    return f"""
    <h3>✅ Video Ready</h3>
    <a href="{real_link}">⬇️ Download Video</a>
    <br><br>
    <a href="/">⬅️ Back</a>
    """

# 🔥 Render dynamic port
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
