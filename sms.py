from twilio.rest import Client
from django.conf import settings

def send_sms(to_number, text, whatsapp=False):

    client = Client(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN
    )

    # ======== INTHA PART THAN NEE KETTA LINE ========

    if whatsapp:
        from_ = settings.WHATSAPP_FROM
        to_number = f'whatsapp:{to_number}'
    else:
        from_ = settings.TWILIO_PHONE

    # ===============================================

    message = client.messages.create(
        body=text,
        from_=from_,
        to=to_number
    )

    return message.sid