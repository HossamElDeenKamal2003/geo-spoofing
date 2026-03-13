from datetime import datetime
import sqlite3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, verify_user, add_user
from spoofing_ai import calculate_spoofing_score, verdict_from_score

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/login")
async def login(data: dict):
    username = data.get("username")
    password = data.get("password")

    if verify_user(username, password):
        return {"status": "success", "message": "Login OK"}

    # إضافة مستخدم جديد
    add_user(
        username,
        password,
        default_country="Egypt",
        default_ip="0.0.0.0",
        default_isp="Unknown",
        default_timezone="Africa/Cairo",
        default_lat=30.0444,
        default_lng=31.2357
    )
    return {"status": "success", "message": "User created and logged in"}

@app.post("/analyze")
async def analyze(data: dict):
    username = data.get("username")

    # بيانات افتراضية من DB
    user = {
        "default_country": "Egypt",
        "default_lat": 30.0444,
        "default_lng": 31.2357,
        "default_timezone": "Africa/Cairo",
        "device_id": data.get("device_id")  # Placeholder
    }

    score = calculate_spoofing_score(user, data)
    verdict = verdict_from_score(score)

    # تحديث DB
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        UPDATE users_table SET
            collected_ip=?,
            collected_isp=?,
            collected_timezone=?,
            collected_lat=?,
            collected_lng=?,
            distance_km=?,
            tz_match=?,
            ip_type=?,
            spoofing_score=?,
            verdict=?,
            login_timestamp=?,
            permission_granted=1
        WHERE username=?
    ''', (
        data.get("ip", "0.0.0.0"),
        data.get("isp", "Unknown"),
        data.get("timezone"),
        data.get("lat"),
        data.get("lng"),
        data.get("distance_km", 0),
        user["default_timezone"] == data.get("timezone"),
        data.get("ip_type"),
        score,
        verdict,
        datetime.now(),
        username
    ))
    conn.commit()
    conn.close()

    return {"spoofing_score": score, "verdict": verdict}
