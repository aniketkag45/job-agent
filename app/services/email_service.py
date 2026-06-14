import os
import smtplib
import logging  
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL", SMTP_USERNAME or "")
SMTP_FROM_NAME = os.getenv("SMTP_FROM_NAME", "AI Job Agent")

def is_configured() -> bool:
    return bool([SMTP_USERNAME and SMTP_PASSWORD])

def send_email(to_email: str, subject: str, body_html: str,body_text: Optional[str] = None) -> bool:
    if not is_configured():
        logger.warning("Email service is not configured. Please set SMTP_USERNAME and SMTP_PASSWORD in the environment variables.")
        return False
    if body_text is None:
        import re
        body_text = re.sub('<[^<]+?>', '', body_html)
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{SMTP_FROM_NAME} <{SMTP_FROM_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body_text, 'plain', 'utf-8'))
    msg.attach(MIMEText(body_html, 'html', 'utf-8'))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_FROM_EMAIL, to_email, msg.as_string())
        logger.info(f"Email sent to {to_email} with subject '{subject}'")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
    
def send_verification_email(to_email: str, verification_link: str) -> bool:
     subject = "Verify your email — AI Job Agent"

     body_html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 30px;">
            <h2 style="color: #2563eb;">AI Job Agent</h2>
            <h3>Verify your email address</h3>
            <p>Thanks for signing up! Click the button below to verify your email and start using the AI Job Agent.</p>
            
            <a href="{verification_link}" 
            style="display: inline-block; padding: 14px 28px; 
                    background-color: #2563eb; color: white; 
                    text-decoration: none; border-radius: 8px;
                    font-weight: bold; margin: 20px 0;">
                Verify Email
            </a>
            
            <p style="color: #666; font-size: 14px;">
                Or copy and paste this link:<br>
                <code>{verification_link}</code>
            </p>
            
            <p style="color: #999; font-size: 12px; margin-top: 30px;">
                If you didn't create this account, you can ignore this email.
            </p>
        </div>
        """

     return send_email(to_email, subject, body_html)
