# ===============================
# AstroRashi - app.py (FINAL)
# ===============================

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

# OpenAI Client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------------
# Helper: Zodiac Sign Calculator
# -------------------------------
def get_zodiac_sign(dob):
    date = datetime.strptime(dob, "%Y-%m-%d")
    day = date.day
    month = date.month

    zodiac = [
        ("Capricorn", 1, 20), ("Aquarius", 2, 19), ("Pisces", 3, 20),
        ("Aries", 4, 20), ("Taurus", 5, 21), ("Gemini", 6, 21),
        ("Cancer", 7, 22), ("Leo", 8, 23), ("Virgo", 9, 23),
        ("Libra", 10, 23), ("Scorpio", 11, 22), ("Sagittarius", 12, 22),
        ("Capricorn", 12, 31)
    ]

    for sign, m, d in zodiac:
        if month == m and day <= d:
            return sign
    return "Capricorn"

# -------------------------------
# Ask Astrology AI
# -------------------------------
def astrology_ai(dob, time, place, question):
    zodiac = get_zodiac_sign(dob)

    prompt = f"""
You are a professional Vedic astrologer.
Your name is Cosmic Guide.
Do NOT mention AI or technology.

Birth Details:
Date: {dob}
Time: {time}
Place: {place}
Zodiac Sign: {zodiac}

User Question:
{question}

Give a calm, realistic astrology-based answer.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------------
# Daily Horoscope AI
# -------------------------------
def daily_horoscope_ai(sign):
    prompt = f"""
You are a professional astrologer.
Give today's horoscope for {sign}.
Do NOT mention AI or technology.
Keep it positive and realistic.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------------
# ROUTES
# -------------------------------

# Home Page
@app.route("/")
def home():
    return render_template("home.html")

# Ask Astrology
@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return render_template("index.html")

    data = request.json
    reply = astrology_ai(
        data["dob"],
        data["time"],
        data["place"],
        data["question"]
    )
    return jsonify({"reply": reply})

# Daily Horoscope
@app.route("/daily-horoscope")
def daily_page():
    return render_template("daily.html")

@app.route("/daily", methods=["POST"])
def daily():
    data = request.json
    reply = daily_horoscope_ai(data["sign"])
    return jsonify({"reply": reply})

# Love Compatibility
@app.route("/love")
def love():
    return render_template("love.html")

# Kundli
@app.route("/kundli")
def kundli():
    return render_template("kundli.html")

# Lucky Color / Number
@app.route("/lucky")
def lucky():
    return render_template("lucky.html")

# Tarot Reading
@app.route("/tarot")
def tarot():
    return render_template("tarot.html")

# ⭐ Jyotish Special (NEW SECTION)
@app.route("/jyotish-special")
def jyotish_special():
    return render_template("jyotish_special.html")

# -------------------------------
# SEO FILES
# -------------------------------
@app.route("/robots.txt")
def robots():
    return send_from_directory(".", "robots.txt")

@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml")

# -------------------------------
# RUN SERVER
# -------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
