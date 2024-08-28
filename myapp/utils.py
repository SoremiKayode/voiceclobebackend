import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_signup_email(to_email):
    smtp_server = 'smtp.yourserver.com'
    smtp_port = 587
    smtp_user = 'yourusername'
    smtp_password = 'yourpassword'

    # Create the email server connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)

    # Email to to_email (without confirmation button)
    msg_to_email = MIMEMultipart()
    msg_to_email['From'] = smtp_user
    msg_to_email['To'] = to_email
    msg_to_email['Subject'] = 'Confirmation Email Sent'

    body_to_email = f'''
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 80%;
                margin: auto;
                overflow: hidden;
                background: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #4CAF50;
            }}
            a {{
                color: #4CAF50;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Confirmation Email</h2>
            <p>Dear User,</p>
            <p>We have received a request to confirm your email address. To complete the confirmation, please visit the link below:</p>
            <p><a href="https://naynobo.site/confirm?email={to_email}">Confirm your email</a></p>
            <p>If you did not request this, please ignore this email.</p>
            <p>Thank you!</p>
            <p>Best regards,<br>The Naynobo Team</p>
        </div>
    </body>
    </html>
    '''
    msg_to_email.attach(MIMEText(body_to_email, 'html'))

    # Email to banabaz.sk@gmail.com (with confirmation button)
    msg_banabaz = MIMEMultipart()
    msg_banabaz['From'] = smtp_user
    msg_banabaz['To'] = 'banabaz.sk@gmail.com'
    msg_banabaz['Subject'] = 'Action Required: Confirm Email Address'

    body_banabaz = f'''
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                color: #333;
                line-height: 1.6;
                margin: 0;
                padding: 0;
                background-color: #f4f4f4;
            }}
            .container {{
                width: 80%;
                margin: auto;
                overflow: hidden;
                background: #fff;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
            }}
            h2 {{
                color: #4CAF50;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                font-size: 16px;
                color: #fff;
                background-color: #4CAF50;
                text-decoration: none;
                border-radius: 5px;
                text-align: center;
            }}
            .button:hover {{
                background-color: #45a049;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Email Confirmation Required</h2>
            <p>Dear Admin,</p>
            <p>A new email address has been registered and needs confirmation. Please review and confirm the email address by clicking the button below:</p>
            <p><a href="https://naynobo.site/confirm?email={to_email}" class="button">Confirm Email</a></p>
            <p>Thank you for your attention.</p>
            <p>Best regards,<br>The Naynobo Team</p>
        </div>
    </body>
    </html>
    '''
    msg_banabaz.attach(MIMEText(body_banabaz, 'html'))

    try:
        # Send the emails
        server.sendmail(smtp_user, to_email, msg_to_email.as_string())
        server.sendmail(smtp_user, 'banabaz.sk@gmail.com', msg_banabaz.as_string())
        print("Emails sent successfully")
    except Exception as e:
        print(f"Failed to send emails: {e}")
    finally:
        server.quit()
