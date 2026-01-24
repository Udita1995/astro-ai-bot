from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# Zodiac Calculator
# -------------------------------
def get_zodiac_sign(dob):
    date = datetime.strptime(dob, "%Y-%m-%d")
    d, m = date.day, date.month
    zodiac = [
        ("Capricorn",1,20),("Aquarius",2,19),("Pisces",3,20),
        ("Aries",4,20),("Taurus",5,21),("Gemini",6,21),
        ("Cancer",7,22),("Leo",8,23),("Virgo",9,23),
        ("Libra",10,23),("Scorpio",11,22),("Sagittarius",12,22),
        ("Capricorn",12,31)
    ]
    for s, mo, da in zodiac:
        if m == mo and d <= da:
            return s
    return "Capricorn"

# -------------------------------
# Universal Jyotish AI
# -------------------------------
def jyotish_ai(topic, details):
    prompt = f"""
You are a senior Vedic astrologer.
Do NOT mention AI or technology.

Topic: {topic}
Details:
{details}

Give clear, practical astrology guidance.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a master Jyotish astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# -------------------------------
# BASIC PAGES
# -------------------------------
@app.route("/")
def home(): return render_template("home.html")

@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "GET":
        return render_template("index.html")
    d = request.json
    z = get_zodiac_sign(d["dob"])
    return jsonify({"reply": jyotish_ai("General Astrology Question",
        f"DOB:{d['dob']} Time:{d['time']} Place:{d['place']} Zodiac:{z} Question:{d['question']}")})

@app.route("/daily-horoscope")
def daily_page(): return render_template("daily.html")

@app.route("/daily", methods=["POST"])
def daily():
    d = request.json
    return jsonify({"reply": jyotish_ai("Daily Horoscope", f"Zodiac:{d['sign']}")})

@app.route("/love")
def love(): return render_template("love.html")

@app.route("/kundli")
def kundli(): return render_template("kundli.html")

@app.route("/lucky")
def lucky(): return render_template("lucky.html")

@app.route("/tarot")
def tarot(): return render_template("tarot.html")

# -------------------------------
# JYOTISH SPECIAL
# -------------------------------
@app.route("/jyotish-special")
def jyotish_special():
    return render_template("jyotish_special.html")

@app.route("/moon-sign")
def moon_sign(): return render_template("moon_sign.html")

@app.route("/numerology")
def numerology(): return render_template("numerology.html")

@app.route("/career")
def career(): return render_template("career.html")

@app.route("/marriage")
def marriage(): return render_template("marriage.html")

@app.route("/health")
def health(): return render_template("health.html")

@app.route("/yearly")
def yearly(): return render_template("yearly.html")

@app.route("/gemstone")
def gemstone(): return render_template("gemstone.html")

@app.route("/muhurat")
def muhurat(): return render_template("muhurat.html")

# -------------------------------
# JYOTISH AI ROUTES
# -------------------------------
@app.route("/moon-sign-ai", methods=["POST"])
def moon_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Moon Sign",
        f"DOB:{d['dob']} Time:{d['time']} Place:{d['place']}")})

@app.route("/numerology-ai", methods=["POST"])
def numerology_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Numerology",
        f"Name:{d['name']} DOB:{d['dob']}")})

@app.route("/career-ai", methods=["POST"])
def career_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Career Guidance",
        f"Zodiac:{d['zodiac']}")})

@app.route("/marriage-ai", methods=["POST"])
def marriage_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Marriage Timing",
        f"DOB:{d['dob']}")})

@app.route("/health-ai", methods=["POST"])
def health_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Health Astrology",
        f"Zodiac:{d['zodiac']}")})

@app.route("/yearly-ai", methods=["POST"])
def yearly_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Yearly Horoscope",
        f"Zodiac:{d['zodiac']} Year:{d['year']}")})

@app.route("/gemstone-ai", methods=["POST"])
def gemstone_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Gemstone Recommendation",
        f"Zodiac:{d['zodiac']}")})

@app.route("/muhurat-ai", methods=["POST"])
def muhurat_ai():
    d = request.json
    return jsonify({"reply": jyotish_ai("Muhurat Finder",
        f"Purpose:{d['purpose']} Date:{d['date']}")})

# -------------------------------
# SEO
# -------------------------------
@app.route("/robots.txt")
def robots():
    return send_from_directory(".", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml")

# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
