# Force redeploy
from flask import Flask, render_template, request, jsonify, send_from_directory
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

# -------------------------
# App Setup
# -------------------------
load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# Zodiac Helper
# -------------------------
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

# -------------------------
# AI FUNCTIONS
# -------------------------
def astrology_ai(dob, time, place, question):
    zodiac = get_zodiac_sign(dob)
    prompt = f"""
You are a professional Vedic astrologer.
Do NOT mention AI or technology.

Birth Details:
Date: {dob}
Time: {time}
Place: {place}
Zodiac: {zodiac}

Question:
{question}

Give calm, realistic astrology advice.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def daily_horoscope_ai(sign):
    prompt = f"""
You are an astrologer.
Give today's horoscope for {sign}.
Keep it short and positive.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def love_ai(boy, girl):
    prompt = f"""
You are a love astrologer.
Boy zodiac: {boy}
Girl zodiac: {girl}
Give compatibility and advice.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def kundli_ai(dob, time, place):
    prompt = f"""
You are a Vedic astrologer.
Birth Date: {dob}
Birth Time: {time}
Birth Place: {place}
Give kundli overview.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def lucky_ai(sign):
    prompt = f"""
You are an astrologer.
For zodiac {sign}, give lucky color, number and advice.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

def tarot_ai(question, cards):
    prompt = f"""
You are a tarot reader.
Question: {question}
Cards drawn: {cards}
Give card meanings and guidance.
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# -------------------------
# PAGE ROUTES
# -------------------------
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/chat", methods=["GET","POST"])
def chat():
    if request.method == "GET":
        return render_template("index.html")
    data = request.json
    return jsonify({"reply": astrology_ai(
        data["dob"], data["time"], data["place"], data["question"]
    )})

@app.route("/daily-horoscope")
def daily_page():
    return render_template("daily.html")

@app.route("/daily", methods=["POST"])
def daily():
    return jsonify({"reply": daily_horoscope_ai(request.json["sign"])})

@app.route("/love-compatibility")
def love_page():
    return render_template("love.html")

@app.route("/love", methods=["POST"])
def love():
    data = request.json
    return jsonify({"reply": love_ai(data["boy"], data["girl"])})

@app.route("/kundli")
def kundli_page():
    return render_template("kundli.html")

@app.route("/kundli", methods=["POST"])
def kundli():
    data = request.json
    return jsonify({"reply": kundli_ai(data["dob"], data["time"], data["place"])})

@app.route("/lucky")
def lucky_page():
    return render_template("lucky.html")

@app.route("/lucky", methods=["POST"])
def lucky():
    return jsonify({"reply": lucky_ai(request.json["sign"])})

@app.route("/tarot")
def tarot_page():
    return render_template("tarot.html")

@app.route("/tarot-reading", methods=["POST"])
def tarot_reading():
    data = request.json
    return jsonify({"reply": tarot_ai(data["question"], data["cards"])})

# -------------------------
# SEO FILE ROUTES (CRITICAL)
# -------------------------
@app.route("/sitemap.xml")
def sitemap():
    return send_from_directory(".", "sitemap.xml")

@app.route("/robots.txt")
def robots():
    return send_from_directory(".", "robots.txt")

# -------------------------
# RUN APP
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
