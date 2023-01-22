import imaplib
import email
import time
from datetime import datetime
from bs4 import BeautifulSoup
import re
import smtplib


server = smtplib.SMTP('smtp.office365.com',587)
server.starttls()
from_email = "bobcryptbot3@hotmail.com"
from_password = "tcoDib01@"


subject1 = "Correct Password!"
body1 = "Send 'enc' to encrypt or 'dec' to decrypt:"

subject2 = "Wrong password"
body2 = "Try again!"

subject3 = "Invalid Command"
body3 = "Try again!"

subject4 = "Cypher Mode"
body4 = "Enter the message you want to Cypher"

subject5 = "Decypher Mode"
body5 = "Enter the message you want to Decypher"

subject6 = "Here's your message!"

texto1 = f"Subject: {subject1}\n\n{body1}"
texto2 = f"Subject: {subject2}\n\n{body2}"
texto3 = f"Subject: {subject3}\n\n{body3}"
texto4 = f"Subject: {subject4}\n\n{body4}"
texto5 = f"Subject: {subject5}\n\n{body5}"


email_pattern = r'([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)'

# Gerar a senha baseada na data atual

# Conectar ao servidor de e-mail
mail = imaplib.IMAP4_SSL("outlook.office365.com")



def extract_sender_email(msg):
    msg = email.message_from_string(msg)
    sender = email.utils.parseaddr(msg['From'])
    return sender[1]



def clear_inbox():
    mail.select("inbox")
    status, data = mail.search(None, 'ALL')
    mail.store("1:*", '+FLAGS', '\\Deleted')
    mail.expunge()

def encrypt(message):

    vowels = {"A": "#", "E": "@", "I": "!", "O": "%", "U": "&"}
    consonants = {}
    for i in range(2,27):
        if i<=24:
            consonants[chr(i + 64)] = chr((i+3) + 64)
        else:
            consonants[chr(i + 64)] = chr((i-24) + 64)
    new_message = ""
    for char in message.upper():
        if char in vowels:
            new_message += vowels[char]
        elif char in consonants:
            new_message += consonants[char]
        elif char == " ":
            new_message += "$"
        else:
            new_message += char
    return new_message

def decrypt(message):

    vowels = {"#": "A", "@": "E", "!": "I", "%": "O", "&": "U"}
    consonants = {}
    for i in range(2,27):
        if i<=24:
            consonants[chr((i+3) + 64)] = chr(i + 64)
        else:
            consonants[chr((i-24) + 64)] = chr(i + 64)
    new_message = ""
    i = 0
    while i < len(message):
        if message[i] in vowels:
            new_message += vowels[message[i]]
            i += 1
        elif message[i] in consonants:
            new_message += consonants[message[i]]
            i += 1
        elif message[i] == "$":
            new_message += " "
            i += 1
    return new_message


def extract_text_from_message(message, text):
    soup = BeautifulSoup(message, 'html.parser')
    for t in soup.stripped_strings:
        if t == text:
            return text
    return None


server.login(from_email, from_password)
mail.login("bobcryptbot3@hotmail.com", "tcoDib01@")


def main():
    try:
        while True:
            current_time = datetime.now()  # atualiza a data e hora
            password = str(current_time.day).zfill(2) + str(current_time.month).zfill(2)
            mail.select("inbox")
            status, messages = mail.search(None, 'ALL')
            if not messages[0]:
                time.sleep(1)
            else:
                messages = messages[0].split(b' ')
                last_message = messages[-1].decode('utf-8')
                if last_message:
                    status, data = mail.fetch(last_message, '(RFC822)')
                    for response in data:
                        if isinstance(response, tuple):
                            msg = response[1].decode()
                            soup = BeautifulSoup(msg, 'html.parser')
                            extracted_text = extract_text_from_message(msg, password)
                            if extracted_text == password:
                                sender_email = extract_sender_email(msg)
                                to_email = sender_email
                                server.sendmail(from_email, to_email, texto1)
                                clear_inbox()
                                while True:
                                    mail.select("inbox")
                                    status, messages = mail.search(None, 'ALL')
                                    if not messages[0]:
                                        time.sleep(1)
                                    else:
                                        messages = messages[0].split(b' ')
                                        last_message = messages[-1].decode('utf-8')
                                        if last_message:
                                            status, data = mail.fetch(last_message, '(RFC822)')
                                            for response in data:
                                                if isinstance(response, tuple):
                                                    msg = response[1].decode()
                                                    soup = BeautifulSoup(msg, 'html.parser')
                                                    extracted_text = extract_text_from_message(msg, "enc") or extract_text_from_message(msg, "dec")
                                                    if extracted_text == "enc":
                                                        sender_email = extract_sender_email(msg)
                                                        to_email = sender_email
                                                        server.sendmail(from_email, to_email, texto4)
                                                        clear_inbox()
                                                        while True:
                                                            mail.select("inbox")
                                                            status, messages = mail.search(None, 'ALL')
                                                            if not messages[0]:
                                                                time.sleep(1)
                                                            else:
                                                                messages = messages[0].split(b' ')
                                                                last_message = messages[-1].decode('utf-8')
                                                                if last_message:
                                                                    status, data = mail.fetch(last_message, '(RFC822)')
                                                                    for response in data:
                                                                        if isinstance(response, tuple):
                                                                            msg = email.message_from_bytes(response[1])
                                                                            for part in msg.walk():
                                                                                if part.get_content_type() == 'text/plain':
                                                                                    message_body = part.get_payload(decode=True)
                                                                                    message_body = message_body.decode()
                                                                                    match = re.search(r"\s{2,}",message_body)
                                                                                    if match:
                                                                                        first_message = message_body[:match.start()]
                                                                                        coded_message = encrypt(first_message)
                                                                                        body6 = coded_message
                                                                                        textocrypt = f"Subject: {subject6}\n\n{body6}"
                                                                                        server.sendmail(from_email,to_email, textocrypt)
                                                                                        clear_inbox()
                                                                                        main()
                                                    elif extracted_text == "dec":
                                                        sender_email = extract_sender_email(msg)
                                                        to_email = sender_email
                                                        server.sendmail(from_email, to_email, texto5)
                                                        clear_inbox()
                                                        while True:
                                                            mail.select("inbox")
                                                            status, messages = mail.search(None, 'ALL')
                                                            if not messages[0]:
                                                                time.sleep(1)
                                                            else:
                                                                messages = messages[0].split(b' ')
                                                                last_message = messages[-1].decode('utf-8')
                                                                if last_message:
                                                                    status, data = mail.fetch(last_message, '(RFC822)')
                                                                    for response in data:
                                                                        if isinstance(response, tuple):
                                                                            msg = email.message_from_bytes(response[1])
                                                                            for part in msg.walk():
                                                                                if part.get_content_type() == 'text/plain':
                                                                                    message_body = part.get_payload(decode=True)
                                                                                    message_body = message_body.decode()
                                                                                    match = re.search(r"\s{2,}",message_body)
                                                                                    if match:
                                                                                        first_message = message_body[:match.start()]
                                                                                        decoded_message = decrypt(first_message)
                                                                                        body7 = decoded_message
                                                                                        textodecrypt = f"Subject: {subject6}\n\n{body7}"
                                                                                        server.sendmail(from_email,to_email, textodecrypt)
                                                                                        clear_inbox()
                                                                                        main()
                                                    else:
                                                        sender_email = extract_sender_email(msg)
                                                        to_email = sender_email
                                                        server.sendmail(from_email, to_email, texto3)
                                                        clear_inbox()
                                                        continue
                            else:
                                sender_email = extract_sender_email(msg)
                                to_email = sender_email
                                server.sendmail(from_email, to_email, texto2)
                                clear_inbox()
                                continue
    except KeyboardInterrupt:
        mail.logout()
        server.quit()
if __name__ == '__main__':
    main()