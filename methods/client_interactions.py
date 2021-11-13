from utils.google_service import *
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders
import mimetypes
import base64

def parse_recipients(recipients=None):
    if recipients is None:
            recipients = []
    elif isinstance(recipients, str):
        recipients = str(recipients)
    elif isinstance(recipients, list) and len(recipients) == 1:
        recipients = str(recipients[0])
    elif isinstance(recipients, list) and isinstance(recipients[0], list):
        recipient_str = ''
        for recipient_group in recipients:
            group_str = ','.join(recipient_group)
            if len(recipient_str) == 0:
                recipient_str += group_str
            else:
                recipient_str = f'{recipient_str},{group_str}'
        recipients = recipient_str
    else: recipients = ','.join(recipients)
    return recipients

def create_email_string(client_name, content_link, content_name, additional_points=None):
    email_message = f"Hey {client_name}!\n\nYou can find the link for {content_name} below. \n\nLINK: {content_link}\n\nPlease note that these files are for listening only and are not considered ready for release until payment has been made.\n"
    addition_prefix = "\nAdditionally:\n"
    signoff = "\n\nMany thanks,\nJesse"
    if not additional_points: return email_message + signoff
    elif isinstance(additional_points, str):
        additional_points = f"{addition_prefix}- " + additional_points
        return email_message + additional_points + signoff
    elif isinstance(additional_points, list):
        additional_points_str = addition_prefix
        for point in additional_points: additional_points_str += f"\n- {point}"
        return email_message + additional_points_str + signoff
    else: raise TypeError("Additional points must be string, list or None.")

class Gmail_Service():
    def __init__(self, client_secret_file='secrets/keys.json', api_name='gmail', api_version='v1', scopes='https://mail.google.com/'):
        self.service = Create_Service(client_secret_file, api_name, api_version, scopes)
    
    def send_email(self, recipients=None, subject="No Subject", body=None, attachments=None):
        '''Basic function for sending emails'''
        recipients = parse_recipients(recipients)
        if body is None: body = ""
        else: body = str(body)
        if attachments is None: attachments = []
        elif isinstance(attachments, str): attachments = [attachments]
        subject = str(subject)
        ### Following code from this tutorial https://www.youtube.com/watch?v=44ERDGa9Dr4&ab_channel=JieJenn ###
        mime_message = MIMEMultipart()
        mime_message["to"] = recipients
        mime_message["subject"] = subject
        mime_message.attach(MIMEText(body, "plain"))
        if attachments:
            for attachment in attachments:
                content_type, encoding = mimetypes.guess_type(attachment)
                main_type, sub_type = content_type.split("/", 1)
                file_name = os.path.basename(attachment)
                my_file = MIMEBase(main_type, sub_type)
                with open(attachment, "rb") as f:
                    my_file.set_payload(f.read())
                my_file.add_header("Content-Disposition", "attachment", filename=file_name)
                encoders.encode_base64(my_file)
                mime_message.attach(my_file)
        raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
        message = (
            self.service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
        )
        print(message)