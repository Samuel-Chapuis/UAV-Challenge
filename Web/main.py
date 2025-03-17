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
from globalVar import mother_drone, second_drone
# -------------------------------- #

if __name__ == '__main__':
    video_thread = Video(cam_index=0)
    video_thread.start()
    
    count = 0
    while True:
        count += 1
        print(f"Count: {count}")
    
    
        
    # app.run(debug=True, threaded=True)
