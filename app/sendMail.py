import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from dotenv import load_dotenv
load_dotenv()
def send_email(receiver_email, subject, body):
    """
    Sends an email using Gmail's SMTP server.
    """
    # Replace these with your own email and app-specific password or less-secure app password
    sender_email = os.getenv('SENDER_EMAIL')  # Your email
    password = os.getenv('EMAIL_PASSWORD')    # Your app-specific password
    
    # Create a MIMEMultipart object to combine headers and content
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Use TLS encryption

        # Login to your Gmail account
        server.login(sender_email, password)
        
        # Convert message to string and send it
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        
        # Close the connection
        server.quit()

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")