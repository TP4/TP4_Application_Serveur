#!/usr/bin/python   
# -*- coding: iso-8859-1 -*-
 
#import mysocket
import socket
import os
from xml.dom.minidom import parse, parseString
import base64
import shutil
import os.path, time
import datetime
import hashlib
 
class serveur:
    """
    Squelette du serveur
    """
 
    # Se donner un objet de la classe socket.
    un_socket = socket.socket()
    nomServeur = "Serveur Tp4"
    # Socket connexion au client.
    connexion = None
 
    MAX_RECV = 1024
    
    ###################################################################################################   
    def __init__(self, host, port):
        print "bob"
        #LOISIR_LIBRE
    ###################################################################################################   
   

    def getListActivities(self, nomBaseDonnees):
        dom = parse('/donnees/' + nomBaseDonnees);
    
    ###################################################################################################   
    def getNameActivity(self):
        print "bob"
    ###################################################################################################
    def getDateActivity(self):
        print "bob"
        
    ###################################################################################################       
    def verifyIfDatePassed(self):
        print "bob"
    
    ###################################################################################################   


########################################################################################
### Main ###
########################################################################################
if __name__ == '__main__':
    serv = serveur('162.209.100.18', 50025)
   

    
            