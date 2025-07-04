import streamlit as st
import requests
import json

st.set_page_config(page_title="Email Classifier", layout="centered")
st.title("📬 Email Thread Classifier")

# Form input
with st.form("email_form"):
    subject = st.text_input("Subject")
    ordinary_body = st.text_area("Body Of Email")
    raw_html = st.text_area("Raw HTML")

    submitted = st.form_submit_button("Classify Email")

# On submit
if submitted:
    payload = {
        "batch": [
            {
                "Subject": subject,
                "Ordinary_Body": ordinary_body,
                "Raw_html": raw_html
            }
        ]
    }

    st.write("🔁 Sending request to the classification API...")
    try:
        response = requests.post(
            "https://classifier.model.soemailsecurity.com/batch-categorizer",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload)
        )

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Classification Successful!")
            email = result["batch_response"][0]
            st.markdown(f"**Subject:** {email['Subject']}")
            st.markdown(f"**Category:** `{email['category']}`")
            st.text_area("Thread Summary", email["body"], height=250)
        else:
            st.error(f"API Error: {response.status_code}")
            st.json(response.text)

    except Exception as e:
        st.error("Request failed. Check your internet or the endpoint.")
        st.exception(e)
