from Gemini_gpt import *
import smtplib
from email.mime.text import MIMEText
import imaplib
import email


GMAIL_ADDRESS_MAIN = os.getenv('GMAIL_ADDRESS_MAIN')

GMAIL_ADDRESS = os.getenv('GMAIL_ADDRESS')
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

def send_email(subject, message, to_addr):

    # Create MIMEText object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = GMAIL_ADDRESS
    msg['To'] = to_addr

    # Connect to Gmail's SMTP server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()  # Start TLS encryption
        server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
        server.sendmail(GMAIL_ADDRESS, to_addr, msg.as_string())


def read_emails(user = GMAIL_ADDRESS, app_password = GMAIL_APP_PASSWORD):
    
    imap_url = 'imap.gmail.com'

    # Connect to the server
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, app_password)

    # Select the mailbox
    status, messages = mail.select('inbox')
    if status != 'OK': return print("Error selecting inbox.")

    # Search for specific mails
    result, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    if not mail_ids: return print("No emails found.")

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    # Iterate through each email
    for i in range(latest_email_id, first_email_id - 1, -1):
        result, data = mail.fetch(str(i), '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                print('From : ' + email_from + '\n')
                print('Subject : ' + email_subject + '\n')

                if msg.is_multipart():
                    for part in msg.walk():
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        if "attachment" not in content_disposition and content_type == "text/html":
                            body = part.get_payload(decode=True).decode()
                            soup = BeautifulSoup(body, 'html.parser')
                            plain_text = soup.get_text(separator='\n')
                            # print("Body:\n", plain_text)
                            prompt = f"You are my email assistant. Please help me summarize this email concisely with bullet points: \n\nSubject: {email_subject}\n\nEmail body: \n{plain_text}"
                            try: send_email(email_subject, generate_text(prompt), GMAIL_ADDRESS_MAIN)
                            except: pass
                else:
                    content_type = msg.get_content_type()
                    if content_type == "text/html":
                        body = msg.get_payload(decode=True).decode()
                        soup = BeautifulSoup(body, 'html.parser')
                        plain_text = soup.get_text(separator='\n')
                        # print("Body:\n", plain_text)
                        prompt = f"You are my email assistant. Please help me summarize this email concisely with bullet points: \n\nSubject: {email_subject}\n\nEmail body: \n{plain_text}"
                        try: send_email(email_subject, generate_text(prompt), GMAIL_ADDRESS_MAIN)
                        except: pass



if __name__ == '__main__':
    print("Gmail_api.py is running directly")
    # send_email('Test Subject', 'This is the email content', GMAIL_ADDRESS_MAIN)
    while True:
        choice = input(f"Do you want to check your emails? (y/n): ")
        if choice == 'y': read_emails()
        else: break



