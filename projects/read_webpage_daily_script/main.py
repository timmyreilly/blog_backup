import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time

# Email settings
SMTP_SERVER = 'smtp.gmail.com'  # Replace with your SMTP server
SMTP_PORT = 587  # Replace with your SMTP port if different
EMAIL_SENDER = 'your-email@gmail.com'  # Your email address
EMAIL_PASSWORD = 'your-app-password'  # App-specific password or account password
EMAIL_RECEIVER = 'receiver-email@gmail.com'  # Recipient's email address
SUBJECT = 'Daily Webpage Content'

# URL of the webpage to scrape
WEBPAGE_URL = 'https://example.com'  # Replace with the actual URL

def get_webpage_content(url):
    """Fetch the content of a webpage."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching webpage: {e}")
        return None

def send_email(subject, content):
    """Send an email with the given subject and content."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    # Attach the webpage content as plain text
    msg.attach(MIMEText(content, 'html'))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Secure the connection
            server.login(EMAIL_SENDER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_SENDER, EMAIL_RECEIVER, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def job():
    """Job to fetch webpage content and send it as an email."""
    print("Fetching webpage content...")
    content = get_webpage_content(WEBPAGE_URL)
    if content:
        print("Sending email...")
        send_email(SUBJECT, content)

# Schedule the job every day at a specific time
schedule.every().day.at("09:00").do(job)  # Set the time you want (24-hour format)

if __name__ == "__main__":
    print("Starting the schedule...")
    job()  # Optionally run once at startup
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute for scheduled tasks
