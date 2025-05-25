import smtplib
from dotenv import load_dotenv
import os

load_dotenv()
EMAIL_FROM = os.getenv("EMAIL_FROM")
MY_PASSWORD = os.getenv("MY_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

def send_mail(message: str):
    if not EMAIL_FROM or not MY_PASSWORD or not EMAIL_TO:
        raise ValueError("One or more required environment variables (EMAIL_FROM, MY_PASSWORD, EMAIL_TO) are not set.")

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL_FROM, password=MY_PASSWORD)
        connection.sendmail(from_addr=EMAIL_FROM,
                            to_addrs=EMAIL_TO,
                            msg=message)
        print("Email sent successfully.")
