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
import re

 
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
        print "niaaaa1"
        self.aSocket.bind((host, port))
        self.aSocket.listen(2)
        print "niaaaaa2"
        #LOISIR_LIBRE
    ###################################################################################################   
    def getData(self):
        #dom = parse('/donnees/' + nomBaseDonnees);
        print "sa commence !"
        dom = parse("LOISIR_LIBRE.XML");
        print "caliss"
        return dom
    ########################################################################################   
    def getListActivitiesForCurrentMonth(self):
        dom = self.getData()
        self.listActivities = "<ListActivities>"
        print 'A'
        for node1 in dom.getElementsByTagName('ns1:LOISIRS_LIBRES'):
            for node2 in node1.getElementsByTagName('LOISIR_LIBRE'):    
                valide = False
                print 'B'
                for node3 in node2.getElementsByTagName('DATE_FIN'):
                    print 'C'
                    if (node3.firstChild != None):
                        valide = self.verifyIfDatePassed(node3.firstChild.data)
                        if valide:
                            self.listActivities += "<Activite>"
                            self.listActivities += "<DATE_FIN>" + node3.firstChild.data + "</DATE_FIN>"
                            #------------------------------------------------------------------------------------
                            for node4 in node2.getElementsByTagName('DATE_DEB'):
                                if node4.firstChild != None:
                                    text = self.correctText(node4.firstChild.data)
                                    self.listActivities += "<DATE_DEB>" + text + "</DATE_DEB>"
                            #------------------------------------------------------------------------------------
                            for node4 in node2.getElementsByTagName('DESCRIPTION'):
                                if node4.firstChild != None:
                                     text = self.correctText(node4.firstChild.data)
                                     self.listActivities += "<DESCRIPTION>" + text + "</DESCRIPTION>"
                            #------------------------------------------------------------------------------------
                            for node4 in node2.getElementsByTagName('NOM_COUR'):
                                if node4.firstChild != None:
                                     text = self.correctText(node4.firstChild.data)
                                     self.listActivities += "<NOM_COUR>" + text + "</NOM_COUR>"
                            #------------------------------------------------------------------------------------
                            for node4 in node2.getElementsByTagName('LIEU_1'):
                                if node4.firstChild != None:
                                     text = self.correctText(node4.firstChild.data)
                                     self.listActivities += "<LIEU_1>" + text + "</LIEU_1>"
                            #------------------------------------------------------------------------------------
                            for node4 in node2.getElementsByTagName('ADRESSE'):
                                if node4.firstChild != None:
                                     text = self.correctText(node4.firstChild.data)
                                     self.listActivities += "<ADRESSE>" + text + "</ADRESSE>"
                            #------------------------------------------------------------------------------------
                            for node4 in node2.getElementsByTagName('HEURE_FIN'):
                                if node4.firstChild != None:
                                     text = self.correctText(node4.firstChild.data)
                                     self.listActivities += "<HEURE_FIN>" + text + "</HEURE_FIN>"
                            #------------------------------------------------------------------------------------
                            for node4 in node2.getElementsByTagName('HEURE_DEBUT'):
                                if node4.firstChild != None:
                                     text = self.correctText(node4.firstChild.data)
                                     self.listActivities += "<HEURE_DEBUT>" + text + "</HEURE_DEBUT>"
                            #------------------------------------------------------------------------------------
                            self.listActivities += "</Activite>"
                            print self.listActivities + '\n'

        self.listActivities += "</ListActivities>"  
        print self.listActivities
        dom = parseString(self.listActivities)            
        return dom.toxml()
    
    def correctText(self, text):
        text = text.replace('\'', '').replace('è', '').replace('É', '').replace('é','')
        return text
    ###################################################################################################   
    def sendNewList(self, server, client, lock):
        entree = client.recv(1024)
        print entree
        print "magiiie"
        lock.acquire()
        server.getListActivitiesForCurrentMonth()
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
                dateActual = (datetime.date.today())
                dateActivity = datetime.datetime.strptime(dateActivity, '%Y-%m-%d')
                if (dateActual.month == dateActivity.month):
                    return True
                else:
                    return False
            else:
                return False

########################################################################################
### Main ###
########################################################################################
if __name__ == '__main__':
    serv = serveur('localhost', 50000)
    semaphoreDomUtilise = threading.Lock()
    while True:
       xml = serv.getListActivitiesForCurrentMonth()
        #print "1"
       # client, clientAdress = serv.aSocket.accept()
       # print "2"
       # thread = threading.Thread(target=serv.sendNewList, args=(serv, client, semaphoreDomUtilise))
       # thread.start()
       # print "3"
        
    

    
            