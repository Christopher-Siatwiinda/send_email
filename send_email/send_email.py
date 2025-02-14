#!/usr/bin/env python3

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from getpass import getpass
import json
import os
import subprocess

TEMPLATES_FILE = "email_templates.json"

def load_templates():
    """Load email templates from JSON file."""
    if not os.path.exists(TEMPLATES_FILE):
        print("No templates found.")
        return {}
    
    with open(TEMPLATES_FILE, "r") as file:
        return json.load(file)

def display_templates(templates):
    """Display available templates."""
    print("\nAvailable Templates:")
    for i, (title, content) in enumerate(templates.items(), start=1):
        print(f"{i}. {title}")
    print("")

def select_template(templates):
    """Let the user select a template."""
    display_templates(templates)
    choice = int(input("Select a template by number: "))
    template_title = list(templates.keys())[choice - 1]
    return templates[template_title]

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

def add_attachments(msg):
    """Add attachments to the email."""
    attachments = []
    
    # Ask if the user wants to add attachments
    add_attach = input("Do you want to add attachments? (y/N): ").strip().lower()
    if add_attach == "y":
        while True:
            file_path = input("Enter the file path to attach (or type 'END' to finish): ").strip()
            if file_path.lower() == "end":
                break
            if not os.path.exists(file_path):
                print("File not found. Try again.")
                continue
            
            attachments.append(file_path)

            # Add file to email
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(file_path)}",
                )
                msg.attach(part)
    
    return msg

def send_email(sender_email, sender_password, from_name, to_emails, subject, message):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = f"{from_name} <{sender_email}>"
        msg["To"] = ", ".join(to_emails)
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Add attachments if chosen
        msg = add_attachments(msg)

        # Send the email
        print("Wait, sending your email...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_emails, msg.as_string())

        print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email: {e}")

def update_script():
    """Update the script from GitHub."""
    print("\nUpdating the script from GitHub...")
    try:
        result = subprocess.run(["git", "--version"], capture_output=True, text=True)
        print(result.stdout)

        result = subprocess.run(["git", "pull"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Error:", result.stderr)
        else:
            print("Script updated successfully!")

    except FileNotFoundError:
        print("Error: Git is not installed. Install Git to use this feature.")

def main_menu():
    """Display the main menu."""
    print("\nWelcome to the Email Sender!")
    print("Select one option below:")
    print("1. Send a message")
    print("2. Update the script")
    choice = input("Enter your choice: ").strip()

    if choice == "1":
        # Choose recipient type
        print("\nSelect the recipient type:")
        print("1. Send to one email address")
        print("2. Send to multiple email addresses")
        recipient_choice = input("Enter your choice: ").strip()

        multiple = recipient_choice == "2"

        # Get sender details
        sender_email = input("Enter your Gmail address: ").strip()
        sender_password = getpass("Enter your Gmail app password: ")
        from_name = input("Enter the 'From Name' the recipient will see: ").strip()

        # Get recipient(s)
        if multiple:
            print("Enter recipient email addresses (one per line). Type 'END' when done:")
            to_emails = []
            while True:
                email = input().strip()
                if email.lower() == "end":
                    break
                to_emails.append(email)
        else:
            to_emails = [input("Enter recipient email address: ").strip()]

        # Choose message type
        print("\nSelect the message type:")
        print("1. Use a template")
        print("2. Enter custom message")
        message_choice = input("Enter your choice: ").strip()

        # Get message
        if message_choice == "1":
            templates = load_templates()
            if templates:
                message = select_template(templates)
            else:
                print("No templates found. Using custom message instead.")
                message = get_multiline_input("Enter the email message (type 'END' on a new line when done):")
        else:
            message = get_multiline_input("Enter the email message (type 'END' on a new line when done):")

        # Get subject
        subject = input("Enter the email subject: ").strip()

        # Send the email
        send_email(sender_email, sender_password, from_name, to_emails, subject, message)

    elif choice == "2":
        update_script()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main_menu()
