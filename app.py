# Force redeploy
from flask import Flask, render_template, request, jsonify
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
Keep it positive, calm, and practical.
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
def love_ai(boy, girl):
    prompt = f"""
You are an expert love astrologer.
Do NOT mention AI or technology.

Boy Zodiac: {boy}
Girl Zodiac: {girl}

Give love compatibility analysis with advice.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a love astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------
# Kundli AI
# -------------------------
def kundli_ai(dob, time, place):
    prompt = f"""
You are a professional Vedic astrologer.
Do NOT mention AI or technology.

Birth Details:
Date: {dob}
Time: {time}
Place: {place}

Generate a basic Kundli interpretation:
- Personality
- Career
- Marriage
- Strengths
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a Vedic astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------
# Lucky Color & Number AI
# -------------------------
def lucky_ai(sign):
    prompt = f"""
You are an astrologer.
Do NOT mention AI or technology.

For zodiac sign {sign}, give:
- Lucky Color
- Lucky Number
- One line advice for today.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an astrologer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content

# -------------------------
# Tarot Card AI
# -------------------------
def tarot_ai(question, cards):
    prompt = f"""
You are a professional Tarot card reader.
Do NOT mention AI or technology.

User Question:
{question}

Number of cards drawn: {cards}

Give Tarot reading with:
- Card name(s)
- Meaning
- Advice
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a tarot reader."},
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
    return jsonify({"reply": daily_horoscope_ai(data["sign"])})

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
    data = request.json
    return jsonify({"reply": lucky_ai(data["sign"])})

@app.route("/tarot")
def tarot_page():
    return render_template("tarot.html")

@app.route("/tarot-reading", methods=["POST"])
def tarot_reading():
    data = request.json
    return jsonify({"reply": tarot_ai(data["question"], data["cards"])})

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
