import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st
import time
import random

# -- Email Sending Helper --
def send_verification_email(receiver_email: str, verification_code: int):
    smtp_server   = st.secrets.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port     = int(st.secrets.get("SMTP_PORT", 587))
    sender_email  = st.secrets.get("SMTP_SENDER")
    sender_password = st.secrets.get("SMTP_PASSWORD")

    if not sender_email or not sender_password:
        st.error("Email credentials not configured.")
        return

    try:
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Your Verification Code"
        body = f"Your verification code is: {verification_code}"
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

    except Exception as e:
        st.error(f"Failed to send verification email: {e}")

# -- Verification Page --
def verify_email():
    st.title("Verify Your University Email")

    email = st.text_input("University Email", key="input_email")
    if st.button("Send Verification Code"):
        if email.endswith("@yale.edu"):
            code = random.randint(100000, 999999)
            st.session_state['verification_code'] = code
            st.session_state['verified_email'] = email

            with st.spinner("Sending verification code..."):
                send_verification_email(email, code)
                time.sleep(1)

            st.success("Verification code sent!")
        else:
            st.error("Please use a valid @yale.edu email address.")

    # Once a code is in state, show the form
    if 'verification_code' in st.session_state:
        st.markdown("---")
        st.subheader("Enter the 6‑digit code you received")
        with st.form("verify_code_form"):
            code_input = st.text_input("Code", max_chars=6, key="input_code")
            submitted = st.form_submit_button("Verify Code")
            if submitted:
                if code_input == str(st.session_state['verification_code']):
                    st.success("✅ Email verified!")
                    # Move on to account creation
                    st.session_state.pop('verification_code')
                    st.session_state['current_page'] = "create_account"
                    st.rerun()
                else:
                    st.error("❌ Invalid code. Please try again.")
