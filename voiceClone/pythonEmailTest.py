import socket

try:
    socket.create_connection(("smtp.zoho.com", 465))
    print("Connected to SMTP server successfully")
except Exception as e:
    print("Failed to connect:", e)
