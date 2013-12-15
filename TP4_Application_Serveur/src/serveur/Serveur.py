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
import unicodedata

 
class serveur:
    """
    Squelette du serveur
    """
 
    # Se donner un objet de la classe socket.
    aSocket = socket.socket()
    nomServeur = "Serveur Tp1"
    # Socket connexion au client.
    listActivities = ""
    requeteXML = None
    MAX_RECV = 1024
    
    ###################################################################################################   
    def __init__(self, host, port):
        self.aSocket.bind((host, port))
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
        for node1 in dom.getElementsByTagName('ns1:LOISIRS_LIBRES'):
            for node2 in node1.getElementsByTagName('LOISIR_LIBRE'):    
                valide = False
                for node3 in node2.getElementsByTagName('DATE_FIN'):
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

        self.listActivities += "</ListActivities>"  
        print self.listActivities
        dom = parseString(self.listActivities)            
        return dom.toxml()

    def correctText(self, text):
        #unicodedata.normalize('NFD', text).encode('ascii', 'ignore')
        text = text.replace(u"\'", "").replace(u"è", "e").replace(u"É", "E").replace(u"é","e").replace(u"â","a").replace(u"î", "i").replace(u"«", "").replace(u"»",'').replace(u"À", "A").replace(u"ô","o")
        return text

    ###################################################################################################   
    def updateList(self, server, semaphore):
        while True:
            semaphore.acquire()
            semaphore.acquire()
            semaphore.acquire()
            semaphore.acquire()
        
            
            self.requeteXML = self.getListActivitiesForCurrentMonth()
        
            semaphore.release()
            semaphore.release()
            semaphore.release()
            semaphore.release()
            self.waitBeforeUpdate()
    ########################################################################################
    def waitBeforeUpdate(self):
        #La mise à jour se feront à 00h01 du matin
        heureActuelle = datetime.datetime.now()
        timeToSleep = ((24 - (heureActuelle.hour + 1))*3600)+((60 - heureActuelle.minute)*60)+(60 - heureActuelle.second) + 60
        time.sleep(timeToSleep)
        
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
    def getList(self, server, client, semaphoreDomUtilise):
        semaphoreDomUtilise.acquire()
        print "Send xml"
        client.send(self.requeteXML)
        semaphoreDomUtilise.release()
        client.close()
########################################################################################
### Main ###
########################################################################################
if __name__ == '__main__':
    serv = serveur('localhost', 50025)
    #4 clients au maximum pourront demander une requête en même temps
    semaphoreDomUtilise = threading.Semaphore(4)
    #On crée un Thread qui d'occupera de créer la requête XML correspondante à la journée et s'occupera ainsi
    #de mettre à jour la requête xml à tout les jours
    threadGenerationXML = threading.Thread(target=serv.updateList, args=(serv, semaphoreDomUtilise))
    threadGenerationXML.start()
    
    while True:
        serv.aSocket.listen(2)
        client, clientAdress = serv.aSocket.accept()
        thread = threading.Thread(target=serv.getList, args=(serv, client, semaphoreDomUtilise))
        thread.start()
        
        
