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

 
class serveur:
    """
    Squelette du serveur
    """
 
    # Se donner un objet de la classe socket.
    un_socket = socket.socket()
    nomServeur = "Serveur Tp1"
    # Socket connexion au client.
    connexion = None
 
    MAX_RECV = 1024
    
    ###################################################################################################   
    def __init__(self, host, port):
        print "bob"
        self.listeActivites = []
        self.increment = 0;
        #LOISIR_LIBRE
    ###################################################################################################   
    def getListDonnees(self):
        #dom = parse('/donnees/' + nomBaseDonnees);
        dom = parse("LOISIR_LIBRE.XML");
        return dom
    ########################################################################################   
    def getNameActivities(self, nomBaseDonnees):
        dom = self.getListDonnees(nomBaseDonnees)
        for node1 in dom.getElementsByTagName('LOISIR_LIBRE'):    
            valide = False
            for node2 in dom.getElementsByTagName('DATE_FIN'):
                valide = self.verifyIfDatePassed(node2.firstChild.data)
                date = node2.firstChild.data
                if valide:
                    for node3 in dom.getElementsByTagName('DESCRIPTION'):
                        print node3.firstChild.data
                        print date
            if valide:
                self.listeActivites.append(node1)
                
          
    ###################################################################################################
    def getTenFirstActivities(self):
        domString = "<TenActivities>";
        for x in range(self.increment, self.increment + 10):
            domString += "<Activity>"
            domString += self.listeActivites[x]
            domString += "</Activity>"
        
        domString += "</TenActivities>"
        dom = parseString(domString)
        
                  
    ###################################################################################################
    def getStartDate(self):
        dom = self.getListDonnees()
        
        ###################################################################################################
    def getEndDate(self):
        dom = self.getListDonnees()
    
    def getAllPassedEvents(self):
        print "bob"
        print "bob2"
        
    ###################################################################################################       
    def verifyIfDatePassed(self, dateActivite):
        #dateActuelle = datetime.datetime.now()
        partiesDate = dateActivite.split('-')
        if int(partiesDate[0]) < 2013:
            return False
        else:
            dateActuelle = time.time()
            date = time.strptime(dateActivite, '%Y-%m-%d')
            dateDonnee = time.mktime(date)
            if dateDonnee > dateActuelle:
                return True
            else:
                return False

            
    
    ###################################################################################################   


########################################################################################
### Main ###
########################################################################################
if __name__ == '__main__':
    serv = serveur('', 50025)
    
    serv.getNameActivities()
   

    
            