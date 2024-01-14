# sms_manager.py

import vonage


class SMSManager:

    def __init__(self, logger , nexmo_key, nexmo_secret, nexmo_from, nexmo_to):
        self.nexmo_key = nexmo_key
        self.nexmo_secret = nexmo_secret
        self.nexmo_from = nexmo_from
        self.nexmo_to = nexmo_to
        self.logger = logger

    def send_sms(self, confidence , bol):
        client = vonage.Client(key=self.nexmo_key, secret=self.nexmo_secret)
        sms = vonage.Sms(client)

        if bol:
            message_text = f"Une detection avec une confiance superieure à {round(confidence, 2)} % a ete effectuee.\n"
        else:
            message_text = "La dérniere detection probablement erroné \n"

        responseData = sms.send_message(
            {
                "from": self.nexmo_from,
                "to": self.nexmo_to,
                "text": message_text,
            }
        )

        if responseData["messages"][0]["status"] == "0":
            print("Message sent successfully.")
            self.logger.info("Message SMS envoyé avec succès.")
        else:
            print(f"Message failed with error: {responseData['messages'][0]['error-text']}")
            self.logger.error(f"Message failed with error: {responseData['messages'][0]['error-text']}")
