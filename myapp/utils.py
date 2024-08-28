import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_signup_email(to_email):
    smtp_server = "smtp.zoho.com"
    smtp_port = 465  # Zoho SMTP port for SSL
    smtp_user = "admin@codesignite.com"
    smtp_password = "Abayomi1994@"

    sender_email = "admin@codesignite.com"
    subject = "Welcome to VoiceCloning - Confirm Your Email"

    # HTML email body
    body = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333333;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333333;
            }
            p {
                font-size: 16px;
                line-height: 1.5;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                font-size: 16px;
                color: #ffffff;
                background-color: #007bff;
                border-radius: 5px;
                text-decoration: none;
            }
            .button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to CodesIgnite!</h1>
            <p>Thank you for signing up with CodesIgnite. We're excited to have you on board.</p>
            <p>Your email has been sent to admin for confirmation</p>
            <p>If you did not sign up for a CodesIgnite account, please ignore this email.</p>
            <p>Best Regards,<br>The CodesIgnite Team @ admin@codesignite.com</p>
        </div>
    </body>
    </html>
    """

    
    # HTML email body 2
    body2 = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                color: #333333;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #333333;
            }
            p {
                font-size: 16px;
                line-height: 1.5;
            }
            .button {
                display: inline-block;
                padding: 10px 20px;
                margin-top: 20px;
                font-size: 16px;
                color: #ffffff;
                background-color: #007bff;
                border-radius: 5px;
                text-decoration: none;
            }
            .button:hover {
                background-color: #0056b3;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Welcome to CodesIgnite!</h1>
            <p>Thank you for signing up with CodesIgnite. We're excited to have you on board.</p>
            <p>Please confirm your email address by clicking the button below:</p>
            <a href="https://naynobo.site/confirm?email=${to_email}" class="button">Confirm Email</a>
            <p>If you did not sign up for a CodesIgnite account, please ignore this email.</p>
            <p>Best Regards,<br>The CodesIgnite Team</p>
        </div>
    </body>
    </html>
    """
    msg_to_admin = MIMEMultipart()
    msg_to_admin['From'] = sender_email
    msg_to_admin['To'] = "banabaz.sk@gmail.com"
    msg_to_admin['Subject'] = subject
    msg_to_admin.attach(MIMEText(body2, 'html'))
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            server.sendmail(sender_email, "banabaz.sk@gmail.com", msg_to_admin.as_string())
        print("Signup email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
