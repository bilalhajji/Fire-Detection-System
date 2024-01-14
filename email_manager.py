import smtplib
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication



class EmailManager:
    def __init__(self, logger , email_address, email_password, email_addressre):
        self.email_address = email_address
        self.email_password = email_password
        self.email_addressre = email_addressre
        self.logger = logger

    def send_email(self, frame, confidence,video_path):
        subject = f'Alerte - Confiance supérieure à{round(confidence, 2)}%'

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.email_address
        msg['To'] = self.email_addressre

        # Add text to the message
        msg.attach(MIMEText(f'Une détection avec une confiance supérieure à {round(confidence, 2)} a été effectuée.'))

        # Convert the image to jpg format
        _, buffer = cv2.imencode('.jpg', frame)

        # Create an image attachment
        msg.attach(MIMEImage(buffer.tobytes(), name="detection.jpg"))

        with open(video_path, 'rb') as video_file:
            video_data = video_file.read()

        video_attachment = MIMEApplication(video_data, _subtype='mp4')
        video_attachment.add_header('content-disposition', 'attachment', filename='video_captured.mp4')
        msg.attach(video_attachment)


        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            print('E-mail envoyé avec succès.')
            self.logger.info("E-mail envoyé avec succès.")
        except Exception as e:
            print('Erreur lors de l\'envoi de l\'e-mail:', str(e))
            self.logger.error(f"Erreur lors de l\'envoi de l\'e-mail: {str(e)}")
