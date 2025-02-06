import streamlit as st
import pandas as pd
import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# File to store feedback
feedback_log_file = "feedback_log.csv"

# Function to log feedback
def log_feedback(feedback, issue=""):
    with open(feedback_log_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([feedback, issue])

def send_email(feedback, issue):
    sender_email = "malayjain1234@gmail.com"  # Replace with your email
    receiver_email = "malayjain1234@gmail.com"  # Replace with your email
    app_password = "cujh wnzj yzmr vjtw"  # Use the generated app password

    subject = "New Feedback Received"
    body = f"Feedback: {feedback}\n\nIssue Description: {issue if issue else 'No description provided.'}"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Set up SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        st.success("Feedback sent successfully! ✅")
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")


# Feedback Section
st.markdown('<div class="feedback-section">', unsafe_allow_html=True)

# Radio button with no default selection
feedback = st.radio("Give your feedback:", ["👍 Thumbs Up", "👎 Thumbs Down"], index=None)

# Handle feedback
if feedback == "👍 Thumbs Up":
    st.success("Thanks for your feedback! 😊")
    st.balloons()  # Animation
    log_feedback("Thumbs Up")
    send_email("Thumbs Up", "")

elif feedback == "👎 Thumbs Down":
    issue = st.text_area("Please describe the issue:", "")
    
    if st.button("Submit"):
        if issue.strip() == "":
            st.warning("Please describe the issue before submitting. ⚠")
        else:
            log_feedback("Thumbs Down", issue)
            send_email("Thumbs Down", issue)
            st.success("Thanks for your feedback! We will work on it. 🤔")
