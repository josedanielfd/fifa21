import email
import imaplib
import sys
import utils as utils


def get_access_code():
    M = imaplib.IMAP4_SSL("imap.gmail.com")
    config_yaml = utils.read_yaml_configs()
    try:
        M.login(config_yaml["EMAIL_CREDENTIALS"]["email"], config_yaml["EMAIL_CREDENTIALS"]["password"])
    except imaplib.IMAP4.error:
        print("Login to email failed")
        sys.exit(1)

    print("Waiting for access code...")

    message_numbers_list = []
    message_numbers = []

    while not message_numbers_list:
        M.select()
        status, message_numbers = M.search(None, f'FROM "{config_yaml["EA_EMAIL"]}" UNSEEN')
        message_numbers_list = message_numbers[0].split()

    message_number = message_numbers[0].split()[0]
    _, msg = M.fetch(message_number, '(RFC822)')
    raw_email = msg[0][1].decode('utf-8')

    email_message = email.message_from_string(raw_email)

    print(email_message['Subject'])

    access_code = ''.join(filter(str.isdigit, email_message['Subject']))

    return access_code
