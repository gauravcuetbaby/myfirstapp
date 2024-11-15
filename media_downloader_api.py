from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/download', methods=['POST'])
def download():
    # Get URL from request data
    data = request.get_json()
    url = data.get("url")

    # Check if URL is provided
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Set up yt-dlp options
    ydl_opts = {
        'format': 'best',  # Get the best available quality
        'noplaylist': True,  # Only download a single video if the URL contains a playlist
        'quiet': True,
        'skip_download': True,  # Don't download, just extract info
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video information
            info = ydl.extract_info(url, download=False)

            # Construct the response with details
            video_details = {
                "title": info.get("title"),
                "duration": info.get("duration"),
                "uploader": info.get("uploader"),
                "thumbnail": info.get("thumbnail"),
                "download_url": info.get("url"),  # Direct download link
                "description": info.get("description"),
                "views": info.get("view_count"),
                "like_count": info.get("like_count"),
                "dislike_count": info.get("dislike_count"),
            }
            return jsonify(video_details)

    except yt_dlp.utils.DownloadError as e:
        return jsonify({"error": "Failed to extract video info", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
