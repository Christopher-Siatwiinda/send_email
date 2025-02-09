# send_email
Email Sender Script
A Python script to send emails via Gmail's SMTP server. The script allows you to send emails to one or multiple recipients, with support for multi-line messages, custom "From Name," and interactive input.

Features
Send emails to one recipient or multiple recipients.

Interactive input for:

Sender's Gmail address.

Sender's Gmail app password (hidden input).

Custom "From Name."

Email subject and multi-line message.

Displays a "Wait, sending your email..." message while sending.

Supports multi-line messages (type END to finish).

Easy-to-use command-line interface.

Prerequisites
Python 3.x installed on your system.

A Gmail account with App Password enabled (if 2-Step Verification is turned on).

Setup
Clone the Repository (if applicable):

git clone https://github.com/Christopher-Siatwiinda/send_email.git
cd email-sender-script
Make the Script Executable:

chmod +x send_email.py
Install Required Libraries:

This script uses Python's built-in libraries (smtplib, argparse, email, getpass), so no additional installation is required.

Usage
Send to One Recipient
Run the script without any flags:

./send_email.py
Follow the prompts to enter:

Your Gmail address.

Your Gmail app password (hidden input).

The "From Name."

The recipient's email address.

The email subject.

The email message (type END on a new line to finish).

Send to Multiple Recipients
Use the -m or --multiple flag:

./send_email.py --multiple
Follow the prompts to enter:

Your Gmail address.

Your Gmail app password (hidden input).

The "From Name."

Recipient email addresses (one per line, type END when done).

The email subject.

The email message (type END on a new line to finish).

Example
Input:
./send_email.py --multiple
Enter your Gmail address: your_email@gmail.com
Enter your Gmail app password: **\*\*\*\***
Enter the 'From Name' the recipient will see: John Doe
Enter recipient email addresses (one per line). Type 'END' when done:
recipient1@example.com
recipient2@example.com
END
Enter the email subject: Test Email
Enter the email message (type 'END' on a new line when done):
Hello,

This is a test email.
Please confirm receipt.

END
Output:
Copy
Wait, sending your email...
Email sent successfully!
Notes
App Password: If you have 2-Step Verification enabled on your Gmail account, you must generate an App Password to use this script. Follow Google's guide to create one.

Error Handling: The script includes basic error handling for common issues (e.g., incorrect password, SMTP errors).

Multi-Line Messages: To write a multi-line message, type your message line by line. When finished, type END on a new line.

License
This project is licensed under the MIT License. See the LICENSE file for details.
