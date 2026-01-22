# FORCE FULL REDEPLOY
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OpenAI client
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
# Ask Astrology AI
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
Zodiac Sign: {zodiac}

Question:
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

# -------------------------
# Daily Horoscope AI
# -------------------------
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

# -------------------------
# Love Compatibility AI
# -------------------------
def love_compatibility_ai(boy_dob, girl_dob):
    boy_sign = get_zodiac_sign(boy_dob)
    girl_sign = get_zodiac_sign(girl_dob)

    prompt = f"""
You are a professional astrologer.

Analyze love compatibility using zodiac psychology.

Boy Zodiac Sign: {boy_sign}
Girl Zodiac Sign: {girl_sign}

Explain:
- Emotional compatibility
- Love bond
- Relationship stability
- Long-term potential

Do NOT mention AI or technology.
Keep tone warm and realistic.
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

# -------------------------
# Kundli / Birth Chart AI
# -------------------------
def kundli_ai(dob, time, place):
    zodiac = get_zodiac_sign(dob)

    prompt = f"""
You are a professional Vedic astrologer.

Create a Kundli-style birth chart analysis.

Birth Details:
Date: {dob}
Time: {time}
Place: {place}
Zodiac Sign: {zodiac}

Explain clearly:
- Personality traits
- Career direction
- Marriage & relationships
- Health tendencies
- Strengths and challenges

Do NOT mention AI or technology.
Give calm, realistic guidance.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an expert Vedic astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------
# Routes
# -------------------------

@app.route("/")
def home():
    return render_template("home.html")

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

@app.route("/daily-horoscope")
def daily_page():
    return render_template("daily.html")

@app.route("/daily", methods=["POST"])
def daily():
    data = request.json
    reply = daily_horoscope_ai(data["sign"])
    return jsonify({"reply": reply})

@app.route("/love-compatibility")
def love_page():
    return render_template("love.html")

@app.route("/love", methods=["POST"])
def love():
    data = request.json
    reply = love_compatibility_ai(
        data["boy_dob"],
        data["girl_dob"]
    )
    return jsonify({"reply": reply})

@app.route("/kundli", methods=["GET", "POST"])
def kundli():
    if request.method == "GET":
        return render_template("kundli.html")

    data = request.json
    reply = kundli_ai(
        data["dob"],
        data["time"],
        data["place"]
    )
    return jsonify({"reply": reply})

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
