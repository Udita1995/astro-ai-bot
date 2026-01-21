from flask import Flask, render_template, request, jsonify
from openai import OpenAI
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def astrology_ai(dob, time, place, question):
    zodiac = get_zodiac_sign(dob)

    prompt = f"""
You are a professional Vedic astrologer.
Use zodiac psychology and traditional astrology symbolism.
Do NOT mention AI, software, or technology.

Birth Details:
Date of Birth: {dob}
Time: {time}
Place: {place}
Zodiac Sign: {zodiac}

User Question:
{question}

Give a calm, realistic, astrology-based answer.
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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    reply = astrology_ai(
        data["dob"],
        data["time"],
        data["place"],
        data["question"]
    )
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
