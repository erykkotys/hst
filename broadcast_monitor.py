from twilio.rest import Client


def send_sms(sms_message):
    client = Client("AC51dd8fc9acf639d9046b518eee89d13e", "b3ad5ffb3bdd4e6754ee0bef3a3c0a01")
    client.messages.create(to="+48604505025", from_="+18125754923", body=sms_message)