import cv2
import time
import numpy as np

class Video():
    def __init__(self, cam_index=0):
        super().__init__()
        self.cap = cv2.VideoCapture(cam_index)
        self.running = self.cap.isOpened()  
        self.frame = None
        self.detected = False  # instance variable for detection state
        self.detection_start_time = 0  # instance variable for detection timer

    def stop(self):
        self.running = False
        self.cap.release()  

    def update_frame(self):
        success, frame = self.cap.read()
        if success:
            self.frame = frame

    def get_jpg(self):
        if self.frame is not None:
            success, buffer = cv2.imencode('.jpg', self.frame)
            if success:
                return buffer.tobytes()
        return None
    
    def detect(self):
        hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        
        lower_red = np.array([0, 100, 70])
        upper_red = np.array([10, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([170, 110, 70])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        
        mask = mask1 + mask2
        res = cv2.bitwise_and(self.frame, self.frame, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        valid_contours = [contour for contour in contours if cv2.contourArea(contour) >= min_area]
        
        if valid_contours:
            if not self.detected:
                self.detection_start_time = time.time()  # start timer
                self.detected = True
            else:
                if time.time() - self.detection_start_time >= 0.5:
                    for contour in valid_contours:
                        x, y, w, h = cv2.boundingRect(contour)
                        cv2.rectangle(self.frame, (x, y), (x + w, y + h), (255, 255, 255), 2)
                    print("Tache rouge détectée pendant 1 seconde")
        else:
            self.detected = False

        cv2.imshow('Webcam', self.frame)

if __name__ == '__main__':
    video = Video()
    min_area = 500  # Aire minimale pour considérer un contour comme valide

    while video.running:
        video.update_frame()
        video.detect()
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    video.stop()
    cv2.destroyAllWindows()
