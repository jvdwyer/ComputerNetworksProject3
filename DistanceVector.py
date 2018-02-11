# Project 3 for CS 6250: Computer Networks
#
# This defines a DistanceVector (specialization of the Node class)
# that can run the Bellman-Ford algorithm. The TODOs are all related 
# to implementing BF. Students should modify this file as necessary,
# guided by the TODO comments and the assignment instructions. This 
# is the only file that needs to be modified to complete the project.
#
# Student code should NOT access the following members, otherwise they may violate
# the spirit of the project:
#
# topolink (parameter passed to initialization function)
# self.topology (link to the greater topology structure used for message passing)
#
# Copyright 2017 Michael D. Brown
# Based on prior work by Dave Lillethun, Sean Donovan, and Jeffrey Randow.
        											
from Node import *
from helpers import *

class DistanceVector(Node):
    
    def __init__(self, name, topolink, outgoing_links, incoming_links):
        ''' Constructor. This is run once when the DistanceVector object is
        created at the beginning of the simulation. Initializing data structure(s)
        specific to a DV node is done here.'''

        super(DistanceVector, self).__init__(name, topolink, outgoing_links, incoming_links)
        
        #TODO: Create any necessary data structure(s) to contain the Node's internal state / distance vector data
        
        
        #only knows about itself and cost to itself
        self.vector = {name: 0}
        

    def send_initial_messages(self):
        ''' This is run once at the beginning of the simulation, after all
        DistanceVector objects are created and their links to each other are
        established, but before any of the rest of the simulation begins. You
        can have nodes send out their initial DV advertisements here. 

        Remember that links points to a list of Neighbor data structure.  Access
        the elements with .name or .weight '''

        # TODO - Each node needs to build a message and send it to each of its neighbors
        # HINT: Take a look at the skeleton methods provided for you in Node.py


        #send messages to incoming/upstream links only
        for x in self.incoming_links:
             myMessage = {"OriginNode": self.name, "DistanceVector": self.vector, "destination": x.name}
             #print('initial message:')
             #print(myMessage)
             self.send_msg(myMessage, x.name)


    def process_BF(self):
        ''' This is run continuously (repeatedly) during the simulation. DV
        messages from other nodes are received here, processed, and any new DV
        messages that need to be sent to other nodes as a result are sent. '''

        # Implement the Bellman-Ford algorithm here.  It must accomplish two tasks below:
        # TODO 1. Process queued messages


        wasUpdated = False
        for msg in self.messages: #this came with the skeleton
             for x in msg["DistanceVector"].keys():
                  if x != self.name and x not in self.vector: #ignore self, check if node is in vector, add to vector
                       for y in self.outgoing_links:
                            if x != y.name:
                                 xWeight = int(self.get_outgoing_neighbor_weight(msg["OriginNode"])) + int(msg["DistanceVector"][x])
                            else:
                                 xWeight = int(self.get_outgoing_neighbor_weight(x))
                       self.vector[x] = xWeight
                       wasUpdated = True
                  elif x != self.name and x in self.vector: #update costs for nodes/ASes already in vecotr
                       myCost = int(msg["DistanceVector"][x]) + int(self.get_outgoing_neighbor_weight(msg["OriginNode"]))
                       if self.vector[x] != -99 and int(msg["DistanceVector"][x]) <= -99 or int(self.get_outgoing_neighbor_weight(msg["OriginNode"])) <= -99: #stop iterating if cost makes it to 99
                           self.vector[x] = -99
                           wasUpdated = True
                       else:
                            if myCost < self.vector[x]  and myCost > -99:
                                 self.vector[x] = myCost
                                 wasUpdated = True
                            elif self.vector[x] != -99 and myCost <= -99:
                                 self.vector[x] = -99
                                 wasUpdated = True
        #print('Vector:')
        #print(self.vector)

        
        # Empty queue -> this came in the skeleton
        self.messages = []



        # TODO 2. Send neighbors updated distances


        if wasUpdated == True:               
             for x in self.incoming_links: #send to incoming/upstream links only
                  copyVector = self.vector.copy()
                  myMessage = {"OriginNode": self.name, "DistanceVector": copyVector, "destination": x.name}
                  #print('updated message:')
                  #print(myMessage)
                  self.send_msg(myMessage, x.name)

    def log_distances(self):
        ''' This function is called immedately after process_BF each round.  It 
        prints distances to the console and the log file in the following format (no whitespace either end):
        
        A:A0,B1,C2
        
        Where:
        A is the node currently doing the logging (self),
        B and C are neighbors, with vector weights 1 and 2 respectively
        NOTE: A0 shows that the distance to self is 0 '''
        
        # TODO: Use the provided helper function add_entry() to accomplish this task (see helpers.py).
        # An example call that which prints the format example text above (hardcoded) is provided.        
        #add_entry("A", "A0,B1,C2") 
        
        logString = ''
        for x in sorted(self.vector):
             logString = logString + x + str(self.vector[x]) + ','
             #print(logString)
        logString = logString.rstrip(',') #drop last comma
        add_entry(self.name, logString)
