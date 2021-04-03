__author__ = 'Nopnithi Khaokaew'

import imaplib
import email
from email.header import decode_header
from bs4 import BeautifulSoup
from time import sleep
from notifications import send_alert
from pprint import pprint
from re import sub

EMAIL = '<your-email>'
PASSWORD = '<your-email-password>'
SERVER = '<your-imap-server>'
FILTER_FROM = '<filter-all-emails-from-X>'
FILTER_SUBJECT = '<filter-the-subject-that-contains-X>'


def extract_html(html):
    soup = BeautifulSoup(html, features='html.parser')
    for script in soup(['script', 'style']):
        script.decompose()
    strips = list(soup.stripped_strings)
    if len(strips) == 18 and strips[1] == 'Ticket ID:':
        return {
            'ticket_id': strips[2],
            'customer': strips[4],
            'requestor': strips[6],
            'classification': strips[8],
            'type': strips[10],
            'category': strips[12],
            'reason': strips[14],
            'description': strips[16],
        }
    return None


def pull_tickets(n: int):
    try:
        imap = imaplib.IMAP4_SSL(SERVER)
        imap.login(EMAIL, PASSWORD)
        status, messages = imap.select('INBOX')
    except:
        status = None
    if status == 'OK':
        tickets = []
        messages = int(messages[0])
        for i in range(messages, messages - n, -1):
            res, msg = imap.fetch(str(i), '(RFC822)')
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    sent_from, encoding = decode_header(msg.get('From'))[0]
                    if isinstance(sent_from, bytes):
                        sent_from = sent_from.decode(encoding)
                    sent_from = sub('[< >]', '', sent_from)
                    if sent_from == FILTER_FROM:
                        subject, encoding = decode_header(msg['Subject'])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding)
                        if FILTER_SUBJECT in subject:
                            content_type = msg.get_content_type()
                            if content_type == 'text/html':
                                body = msg.get_payload(decode=True).decode()
                                ticket = extract_html(body)
                                tickets.append(ticket)
        imap.close()
        imap.logout()
        return tickets
    return None


def main():
    existing_id = None
    while True:
        tickets = pull_tickets(10)
        if tickets:
            lastest_ticket = tickets[0]
            new_id = lastest_ticket['ticket_id']
            if existing_id == new_id:
                print('No new ticket...')
            else:
                existing_id = new_id
                print('A new customer ticket has been found! --> Sent LINE notification')
                pprint(lastest_ticket)
                send_alert(f'Found a new customer ticket!\n'
                           '------------------------------\n'
                           f'Ticket ID: {lastest_ticket["ticket_id"]}\n'
                           f'Customer: {lastest_ticket["customer"]}\n'
                           f'Requestor: {lastest_ticket["requestor"]}\n'
                           f'Classification: {lastest_ticket["classification"]}\n'
                           f'Type: {lastest_ticket["type"]}\n'
                           f'Category: {lastest_ticket["category"]}\n'
                           f'Reason: {lastest_ticket["reason"]}\n'
                           f'Description: {lastest_ticket["description"]}\n'
                           '------------------------------\n'
                           f'URL: https://<your-domain>.com')
            print('-' * 50)
        sleep(10)


if __name__ == '__main__':
    main()
