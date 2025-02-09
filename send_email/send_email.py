#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
import argparse
from getpass import getpass  # For secure password input

def send_email(sender_email, sender_password, from_name, to_emails, subject, message):
    try:
        # Create the email
        msg = MIMEText(message)
        msg["From"] = f"{from_name} <{sender_email}>"
        msg["To"] = ", ".join(to_emails)  # Join multiple recipients with a comma
        msg["Subject"] = subject

        # Send the email
        print("Wait, sending your email...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_emails, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

def get_multiline_input(prompt):
    """Get multi-line input from the user."""
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip().lower() == "end":
            break
        lines.append(line)
    return "\n".join(lines)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Send an email via Gmail.")
    parser.add_argument(
        "-m", "--multiple", 
        action="store_true", 
        help="Send email to multiple recipients"
    )
    args = parser.parse_args()

    # Get sender details
    sender_email = input("Enter your Gmail address: ").strip()
    sender_password = getpass("Enter your Gmail app password: ")  # Hide password input
    from_name = input("Enter the 'From Name' the recipient will see: ").strip()

    # Get recipient(s)
    if args.multiple:
        print("Enter recipient email addresses (one per line). Type 'END' when done:")
        to_emails = []
        while True:
            email = input().strip()
            if email.lower() == "end":
                break
            to_emails.append(email)
    else:
        to_emails = [input("Enter recipient email address: ").strip()]

    # Get subject and message
    subject = input("Enter the email subject: ").strip()
    print("Enter the email message (type 'END' on a new line when done):")
    message = get_multiline_input("")

    # Send the email
    send_email(sender_email, sender_password, from_name, to_emails, subject, message)