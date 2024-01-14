import cv2
from config_manager import ConfigManager
from sms_manager import SMSManager
from email_manager import EmailManager
from logging_manager import Logging
from frame_processor import FrameProcess
import numpy as np
import time

class Main:
    def __init__(self):

        self.config_manager = ConfigManager()
        self.alerte_active, self.nexmo_key, self.nexmo_secret, self.email_address, self.email_password, self.email_addressre, self.nexmo_from, self.nexmo_to, self.stream = self.config_manager.read_config()
        self.logger = Logging().logger
        self.sms_manager = SMSManager(self.logger,self.nexmo_key, self.nexmo_secret, self.nexmo_from, self.nexmo_to)
        self.email_manager = EmailManager(self.logger,self.email_address, self.email_password, self.email_addressre)
        self.frame_process = FrameProcess()


        # stream
        self.cap = cv2.VideoCapture(self.stream)

        # to calculate the number of frames
        self.frame_count = 0
        # to calculate the number of skipped frames
        self.skip = 1

        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        # Number of processed frames
        self.n_frame = 15 * self.fps

        # Number of skipped frames 
        self.frame_skipper = self.fps // 2

        self.dernier_envoi_temps = 0
        self.premier_envoi_temps = 0
        # To send an alert after 30 minutes for the first time
        self.time_skip_alert = 1800
        self.n = 0
        self.frames = []
        
        self.logger.info("Démarrage de l'application.")

    def run(self):
        while True:
            try:

                if self.skip % 6 == 0:
                    for _ in range(self.frame_skipper):
                        self.cap.grab()

                ret, frame = self.cap.retrieve()

                if not ret:
                    self.logger.warning(f"Reconnecting stream ....")
                    self.cap = cv2.VideoCapture(self.stream)
                    continue
                self.frames.append(frame)

                frame = cv2.resize(frame, (640, 480))
                processed_frame = self.frame_process.process_frame(frame)

                self.frame_count += 1
                self.skip += 1
                
                cv2.imshow('frame', processed_frame)
                cv2.waitKey(1)

                
                # Alert System
                if frame_count >= n_frame:

                    # If an alert was sent in the first minute and there is no detection after 30 minutes
                    if (n_frame >= (450 * self.fps) and len(self.frame_process.informations) == 0 ):
                        self.sms_manager.send_sms(mean_confidence , False)
                        self.logger.warning("la derniere detection est probablement fausse.")

                    # If there is at least a 20% detection
                    if len(self.frame_process.informations) >= (n_frame / 5):
                        # To store the frame associated with the max confidence
                        frameAlert = None
                        confs = []
                        for ite in self.frame_process.informations:
                            confs.append(ite[0])
                        
                        mean_confidence = np.mean(confs)

                        max_confidence = np.max(confs)

                        for item in self.frame_process.informations:
                            if item[0] == max_confidence:
                                frameAlert = item[1]
                                break

                        if time.time() - dernier_envoi_temps >= time_skip_alert:

                            if time.time() - premier_envoi_temps >= time_skip_alert:

                                frameAlert_index = self.frames.index(frameAlert)
                                # Copy a 10 second video
                                start_index = max(0, frameAlert_index - 10 * self.fps)  
                                end_index = min(len(self.frames), frameAlert_index + 10 * self.fps + 1)
                                selected_frames = self.frames[start_index:end_index]

                                video_writer = cv2.VideoWriter('video_captured.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 30, (self.frames[0].shape[1], self.frames[0].shape[0]))

                                for frame in selected_frames:
                                    video_writer.write(frame)
                                video_writer.release()

                                self.sms_manager.send_sms(mean_confidence , True)
                                alert_video_path = 'video_captured.mp4' 
                                self.email_manager.send_email(frameAlert, max_confidence, alert_video_path)
                                self.frames.clear()

                                dernier_envoi_temps = time.time()
                                
                                # If the first alert has not been sent yet
                                if premier_envoi_temps == 0:
                                    premier_envoi_temps = time.time()
                                
                                n_frame = 450 * self.fps
                                n+=1
                    else:
                        n_frame = 15 * self.fps
                        n = 0


                    self.frame_process.informations.clear()
                    premier_envoi_temps == 0
                    frame_count = 0

                if n == 3 :
                        time_skip_alert = 10800
                        n_frame = 2700 * self.fps
                        n = 0
                
            except Exception as e:
                self.logger.error(f"Une erreur s'est produite dans la boucle principale : {str(e)}")

        cap.release()

if __name__ == "__main__":
    app = Main()
    app.run()
