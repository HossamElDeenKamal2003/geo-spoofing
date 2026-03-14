import streamlit as st
import requests
import uuid  # لإنشاء Device ID افتراضي

st.title("AI-Based Anti-Geo-Spoofing System")

# تعريف session_state من البداية
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# إنشاء Device ID ثابت لكل session (يمكن تغييره لاحقًا ليكون fingerprint حقيقي)
if "device_id" not in st.session_state:
    st.session_state["device_id"] = str(uuid.uuid4())

# --- Login Form ---
with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login")

    if submitted:
        try:
            res = requests.post(
                "https://geo-spoofing.onrender.com/login",
                json={"username": username, "password": password},
                timeout=5
            )
            res.raise_for_status()
            data = res.json()

            if data.get("status") == "success":
                st.success("Login successful! Proceeding to Permission screen...")
                st.session_state["logged_in"] = True
            else:
                st.error("Invalid credentials")
        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
        except ValueError:
            st.error("Server did not return valid JSON")

# --- Permission Screen ---
if st.session_state.get("logged_in"):
    st.subheader("Permission Request")
    st.write(
        "This app needs access to your IP, ISP, Timezone, and GPS location for security purposes."
    )

    allow = st.button("Allow")
    deny = st.button("Deny")

    if deny:
        st.error("You denied permission. Cannot continue.")
    elif allow:
        st.success("Permission granted! Collecting data...")

        # --- جمع البيانات (Data Catching) ---
        collected_data = {
            "username": username,
            "device_id": st.session_state["device_id"],  # Fingerprint placeholder
            "country": "US",          # يمكن تعويضه ببيانات حقيقية من IP geolocation
            "lat": 40.7128,
            "lng": -74.0060,
            "timezone": "America/New_York",
            "ip_type": "vpn",         # يمكن تحديثه من API كشف VPN
            "ip": "1.2.3.4",          # placeholder IP
            "isp": "Some ISP"         # placeholder ISP
        }

        try:
            # إرسال البيانات للـ API لتحليل Spoofing
            analyze_res = requests.post(
                "https://geo-spoofing.onrender.com/analyze",
                json=collected_data,
                timeout=5
            ).json()

            st.write(f"**Spoofing Score:** {analyze_res['spoofing_score']}")
            st.write(f"**Verdict:** {analyze_res['verdict']}")

            # عرض ملاحظات إضافية حسب النتيجة
            if analyze_res["spoofing_score"] >= 50:
                st.warning("Potential Geo-Spoofing detected! ⚠️")
            else:
                st.success("Device location appears genuine ✅")

        except requests.exceptions.RequestException as e:
            st.error(f"Request error: {e}")
        except ValueError:
            st.error("Server did not return valid JSON")
