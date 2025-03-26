'''
Projet ...... : Application Web de control d'un drone

Auteurs ..... : Samuel Chapuis
............. :

Langage ..... : Python 3.11.11           
Version ..... : 2.1.0
'''

# -------------------------------- #
# Import Locaux
from webb import app
from video import Video
import globalVar
import cv2
# -------------------------------- #

if __name__ == '__main__':
    # Load the local image
    # globalVar.video_image = cv2.imread('Web/root_image.png')

    video_thread = Video(cam_index=0)
    video_thread.start()

    app.run(debug=True, threaded=True)
    
    # count = 0
    # while True:
    #     count += 1
    #     print(f"Count: {count}")
    
    
        
 
