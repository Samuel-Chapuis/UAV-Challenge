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
import cv2
import threading
import numpy as np
import time
import torch
from ultralytics import YOLO
# -------------------------------- #

from model import model


if __name__ == '__main__':    
    app.run(debug=True, threaded=True)
