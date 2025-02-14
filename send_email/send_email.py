#!/usr/bin/env python3

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getpass import getpass
import time
import subprocess
import sys

#attempting the auto updates
# GitHub Repository URL
GITHUB_REPO_URL = "https://github.com/Christopher-Siatwiinda/send_email.git"

def update_script():
    """Pull the latest version of this script from GitHub."""
    print("\nUpdating the script from GitHub...")
    try:
        # Check if git is installed
        subprocess.run(["git", "--version"], check=True)
        
        # Pull the latest changes
        subprocess.run(["git", "pull", GITHUB_REPO_URL], check=True)
        
        print("\nScript updated successfully! Please restart the script.")
        sys.exit(0)
        
    except subprocess.CalledProcessError:
        print("Error: Failed to update the script. Make sure Git is installed.")
        sys.exit(1)

def send_email(sender_email, sender_password, from_name, to_emails, subject, message):
    try:
        # Create the email
        msg = MIMEMultipart("alternative")
        msg["From"] = f"{from_name} <{sender_email}>"
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = subject
        msg["Reply-To"] = sender_email
        msg["Return-Path"] = sender_email

        # Preserve paragraphs by maintaining line breaks
        plain_text = message
        
        # Convert message to HTML by preserving line breaks and paragraphs
        html_message = "<br>".join(
            [f"<p>{para}</p>" for para in message.split("\n") if para]
        )

        text_part = MIMEText(plain_text, "plain")
        html_part = MIMEText(f"<html><body>{html_message}</body></html>", "html")

        msg.attach(text_part)
        msg.attach(html_part)

        # Send the email
        print("Wait, sending your email...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            for email in to_emails:
                server.sendmail(sender_email, email, msg.as_string())
                print(f"Email sent to {email} successfully!")
                time.sleep(1)  # Pause to reduce spam detection

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
    # Welcome message
    print("\nWelcome! Select one option below:")
    print("1. Send a message")
    print("2. Update the script")

    main_choice = input("Enter your choice (1 or 2): ").strip()

    # Validate choice
    if main_choice not in ["1", "2"]:
        print("Invalid choice. Please run the script again and select 1 or 2.")
        sys.exit(1)

    # If choice is 2, update the script
    if main_choice == "2":
        update_script()

    # If choice is 1, proceed to sending a message
    print("\nSelect one option below:")
    print("1. Send to one email address")
    print("2. Send to multiple email addresses")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    # Validate choice
    if choice not in ["1", "2"]:
        print("Invalid choice. Please run the script again and select 1 or 2.")
        sys.exit(1)
    
    # Get sender details
    sender_email = input("Enter your Gmail address: ").strip()
    sender_password = getpass("Enter your Gmail app password: ")
    from_name = input("Enter the 'From Name' the recipient will see: ").strip()

    # Get recipient(s)
    if choice == "2":
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
