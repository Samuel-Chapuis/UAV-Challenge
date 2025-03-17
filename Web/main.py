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
# -------------------------------- #

if __name__ == '__main__':    
    app.run(debug=True, threaded=True)
