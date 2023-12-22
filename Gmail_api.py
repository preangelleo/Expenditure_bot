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


def send_to_gmail_main(message, subject = 'From Python Bot'):
    send_email(subject, message, GMAIL_ADDRESS_MAIN)
    send_msg(f"Message sent to {GMAIL_ADDRESS_MAIN} successfully.")
    return


def read_emails(user=GMAIL_ADDRESS, app_password=GMAIL_APP_PASSWORD):
    imap_url = 'imap.gmail.com'

    # Connect to the server
    mail = imaplib.IMAP4_SSL(imap_url)
    mail.login(user, app_password)

    # Select the mailbox
    status, messages = mail.select('inbox')
    if status != 'OK':
        print("Error selecting inbox.")
        return

    # Search for specific mails
    result, uids = mail.uid('search', None, 'ALL')
    if result != 'OK':
        print("No emails found.")
        return

    for uid in uids[0].split():
        uid = uid.decode('utf-8')  # Ensure UID is a string
        result, data = mail.uid('fetch', uid, '(RFC822)')
        if result != 'OK':
            continue

        msg = email.message_from_bytes(data[0][1])
        email_subject = msg['subject']
        email_from = msg['from']
        print('From : ' + email_from + '\n')
        print('Subject : ' + email_subject + '\n')

        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition and content_type == "text/html":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            content_type = msg.get_content_type()
            if content_type == "text/html":
                body = msg.get_payload(decode=True).decode()

        soup = BeautifulSoup(body, 'html.parser')
        plain_text = soup.get_text(separator='\n')
        prompt = f"You are my email assistant. Please help me summarize this email concisely with bullet points. If you think it's an commercial or spam, please reply restrictly with only the word: no_need_to_summarize in lowercase. Then your reply will be passed to python code, if my python code finds 'no_need_to_summarize' in your reply, this email will be ignored. \n\nSubject: {email_subject}\n\nFrom: {email_from}\n\nContent:\n{plain_text}"

        if 'no_need_to_summarize' in plain_text.lower(): continue

        try: 
            summary = generate_text(prompt)  # Assuming generate_text is a function you've defined
            send_email(email_subject, summary, GMAIL_ADDRESS_MAIN)
        except Exception as e:
            print(f"Error during email processing: {e}")

        # Archive the email
        result, copy_response = mail.uid('COPY', uid, '"[Gmail]/All Mail"')
        if result == 'OK':
            mail.uid('store', uid, '+FLAGS', '(\Deleted)')
            mail.expunge()
        else:
            print(f"Error archiving email UID {uid}: {copy_response}")


if __name__ == '__main__':
    print("Gmail_api.py is running directly")
    # send_email('Test Subject', 'This is the email content', GMAIL_ADDRESS_MAIN)
    while True:
        choice = input(f"Do you want to check your emails? (y/n): ")
        if choice == 'y': read_emails()
        else: break



