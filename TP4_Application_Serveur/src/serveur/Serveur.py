#!/usr/bin/python   
# -*- coding: iso-8859-1 -*-
 
#import mysocket
import socket
import os
from xml.dom.minidom import parse, parseString
import base64
import shutil
import os.path
from time import mktime
import time
import datetime
import hashlib
import thread
import threading

 
class serveur:
    """
    Squelette du serveur
    """
 
    # Se donner un objet de la classe socket.
    aSocket = socket.socket()
    nomServeur = "Serveur Tp1"
    # Socket connexion au client.
    listActivities = ""
    MAX_RECV = 1024
    
    ###################################################################################################   
    def __init__(self, host, port):

        self.aSocket.bind((host, port))
        self.aSocket.listen(2)
        #LOISIR_LIBRE
    ###################################################################################################   
    def getData(self):
        #dom = parse('/donnees/' + nomBaseDonnees);
        dom = parse("LOISIR_LIBRE.XML");
        return dom
    ########################################################################################   
    def getListActivitiesForCurrentMonth(self):
        dom = self.getData()
        self.listActivities = "<ListActivities>"
        for node1 in dom.getElementsByTagName('LOISIR_LIBRE'):    
            valide = False
            for node2 in dom.getElementsByTagName('DATE_FIN'):
                if (node2.firstChild != None):
                    valide = self.verifyIfDatePassed(node2.firstChild.data)
                    valide = True
                    if valide:       
                            self.listActivities += node1.toxml() ##To verify. I'm not sure node1.toxml() will work. -Raphael
        self.listActivities += "</ListActivities>"    
        self.listActivities = parseString(self.listActivities).toxml()            
        return self.listActivities
    ###################################################################################################   
    def sendNewList(self, server, client, lock):
        lock.acquire()
        client.send(server.listActivities)
        lock.release()
        client.close()
    ########################################################################################   
    def verifyIfDatePassed(self, dateActivity):
        #dateActuelle = datetime.datetime.now()
        activityDateSplited = dateActivity.split('-')
        if int(activityDateSplited[0]) < 2013:
            return False
        else:
            dateActuelle = time.time()
            date = time.strptime(dateActivity, '%Y-%m-%d')
            dateFromData = time.mktime(date)
            if dateFromData > dateActuelle:
                dateActualMonth = datetime.date.month
                dateActivityMonth = datetime.datetime.strptime(dateActivity, '%Y-%m-%d')
                if (dateActualMonth == dateActivityMonth.month):
                    return True
                else:
                    return False
            else:
                return False

########################################################################################
### Main ###
########################################################################################
if __name__ == '__main__':
    serv = serveur('localhost', 50025)
    semaphoreDomUtilise = threading.Lock()
    while True:
        client, clientAdress = serv.aSocket.accept()
        thread = threading.Thread(target=serv.sendNewList)
        
    

    
            