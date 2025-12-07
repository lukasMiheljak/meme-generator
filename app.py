from flask import Flask, render_template, request
from PIL import Image, ImageDraw, ImageFont
import textwrap

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generation", methods=["POST"])
def generate():
    file = request.files["image"]
    top_text = request.form["top"]
    bottom_text = request.form["bottom"]

    image = Image.open(file.stream)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype("OpenSans.ttf", size=int(image.width/16))
    stroke_w = max(1, int(image.width/12 * 0.06))
    margin = 0
    max_chars = int(image.width // (font.size * 0.6))

    for line in textwrap.wrap(top_text, max_chars):
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_w)
        text_width = bbox[2] - bbox[0]

        x = (image.width - text_width) // 2
        draw.text((x, margin), line, font=font,
                            fill="white", stroke_width=stroke_w, stroke_fill="black", align="center")
        margin += image.height/16

    h_bottom = 0
    lines = textwrap.wrap(bottom_text, max_chars)
    for line in lines:
        h_bottom += image.height/16

    h_bottom += 20

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font, stroke_width=stroke_w)
        text_width = bbox[2] - bbox[0]

        x = (image.width - text_width) // 2

        draw.text((x, image.height - h_bottom), line, font=font,
                  fill="white", stroke_width=stroke_w, stroke_fill="black", align="center")
        h_bottom -= image.height/16

    out = "static/meme.png"
    image.save(out)

    return render_template("index.html", meme_out=out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
