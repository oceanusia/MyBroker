import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st
import time
import random

def send_verification_email(receiver_email, verification_code):
    # SMTP Configuration
    smtp_server = "smtp.gmail.com"  # Change to your provider's SMTP server
    smtp_port = 587  # Use 465 for SSL or 587 for TLS
    sender_email = "nessira161@gmail.com"  # Replace with your email
    sender_password = "vnrb gmhw oapy pfer"  # Replace with your password or app password

    try:
        # Create the email
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = "Your Verification Code"
        body = f"Your verification code is: {verification_code}"
        message.attach(MIMEText(body, "plain"))

        # Connect to the SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        print("Verification email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Verify University Email Function
def verify_email():
    st.title("Verify Your University Email")

    # Sending Verification Code
    email = st.text_input("University Email", key="input_email")
    if st.button("Send Verification Code"):
        if email.endswith("@yale.edu"):
            code = random.randint(100000, 999999)
            st.session_state['verification_code'] = code
            st.session_state['verified_email']  = email

            # Display Loading Spinner
            with st.spinner("Sending verification code..."):
                send_verification_email(email, code)
                time.sleep(3)
            
            st.success("Verification code sent!")
        else:
            st.error("Please use a valid university email address.")

    # Entering Verification Code
    if 'verification_code' in st.session_state:
        st.markdown("---")
        st.subheader("Enter the 6‑digit code you received")

        with st.form("verify_form"):
            code_input = st.text_input("Code", max_chars=6, key="input_code")
            verify_clicked = st.form_submit_button("Verify Code")

            if verify_clicked:
                if code_input == str(st.session_state['verification_code']):
                    # don’t rerun yet – just set a flag
                    st.session_state['show_continue'] = True
                else:
                    st.error("❌ Invalid code. Please try again.")

        # Outside the form: let them click to continue
        if st.session_state.get('show_continue', False):
            st.success("✅ Email verified! Click to continue.")
            if st.button("Continue to Account Creation"):
                st.session_state['current_page'] = "create_account"
                st.rerun()