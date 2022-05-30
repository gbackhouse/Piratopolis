'''
This script contains the functions and program for the game
----------------------------------------------------------
   ____  _           _                         _ _     _ 
  |  _ \(_)_ __ __ _| |_ ___  ___  _ __   ___ | (_)___| |
  | |_) | | '__/ _` | __/ _ \/ _ \| '_ \ / _ \| | / __| |
  |  __/| | | | (_| | ||  __/ (_) | |_) | (_) | | \__ \_|
  |_|   |_|_|  \__,_|\__\___|\___/| .__/ \___/|_|_|___(_)
                                |_|                    
----------------------------------------------------------
For detailed explanation and dependencies, please see the
read me file
----------------------------------------------------------
Created by Gillian Backhouse
Created on 05 May 2022
Updated on 27 May 2022
'''

import time, os, numpy, random, arcpy


Play = 1

# dictionaries storing character information
CAPN = {"name":"Captain Lobster Legs", "rum": 20, "tolerance": 20, "rumadd": 3}
MADMAN = {"name":"Mad Rodger Sea Wolf", "rum": 15, "tolerance": 15, "rumadd": 4}
LADY = {"name":"Lady Ailith of Dark Water", "rum": 12, "tolerance": 12, "rumadd": 5}
TYPES = {1: CAPN, 2: MADMAN, 3: LADY}


Jokes = {}
# Pirate jokes
Jokes[1] = "What do you call 3.14 men out at sea?\n'Pi'-rates!" #BoredPanda
Jokes[2] = "What did the ocean say to the pirate?\nNothing, it just waved." #BoredPanda
Jokes[3] = "How do pirates know that they are pirates?\nThey think, therefore they ARRRR!!!!!" #BoredPanda
Jokes[4] = "What lies at the bottom of the ocean and twitches?\nA nervous wreck." #BoredPanda
Jokes[5] = "What do you call a pirate who likes to skip school?\nCaptain Hooky!" #BoredPanda
Jokes[6] = "What did the pirate say when he left his wooden leg in the freezer?\nShiver me timbers!" #BoredPanda
Jokes[7] = "What would you call a pirate with 4 eyes?\nAn iiiirate." #BoredPanda
Jokes[8] = "What's the difference between a hungry pirate and a drunken pirate?\nOne has a rumbling tummy, and the other's a tumbling rummy." #BoredPanda
Jokes[9] = "Why does it take pirates so long to learn the alphabet?\nBecause they can spend years at C." #BoredPanda
Jokes[10] = "What do you call a pirate with two eyes, two hands, and two legs?\nA beginner." #BoredPanda
Jokes[11] = "What did the pirate say when his wooden leg got stuck in the freezer?\nShiver me timbers!" #JuicyQuotes.com
Jokes[12] = "What did the sea say to the pirate?\nNothing, it just waved!" #kidadl.com
Jokes[13] = "How much did the pirate pay for his hook and his peg?\nAn arm and a leg!" #kidadl.com
Jokes[14] = "What did the pirate say on his 80th birthday?\nAye matey!" #kidadl.com
Jokes[15] = "Why couldn't the pirates play cards?\nBecause they were standing on the deck!" #kidadl.com
Jokes[16] = "Where do pirates buy their hooks?\nThe second hand store!" #kidadl.com
Jokes[17] = "How do you make a pirate furious?\nYou take away the 'p'!" #kidadl.com
Jokes[18] = "Why was the pirate ship so cheap?\nIt was on sail!" #kidadl.com
Jokes[19] = "What's a pirate's favourite type of exercise?\nThe plank!" #kidadl.com
Jokes[20] = "What's the difference between a pirate and a raspberry farmer?\nThe pirate buries his treasures, but the farmer treasures his berries" #kidadl.com
Jokes[21] = "Why are maths teachers secretly pirates?\nBecause they're always trying to find X!" #kidadl.com
Jokes[22] = "Why is being a pirate so addictive?\nBecause once you lose your first hand, you get hooked!" #kidadl.com
Jokes[23] = "How much did the pirate pay to get his ears pierced?\nA buck an ear." #kidadl.com
Jokes[24] = "What does pirate Santa say?\nRow row row!" #kidadl.com
Jokes[25] = "How much did the pirate pay to get his ears pierced?\nA buck an ear!" #kidadl.com


# Character class
class Pirate():

    def __init__(self, type, Loc):
        self.type = type
        self.xLoc = Loc[0]
        self.yLoc = Loc[1]
        self.drunk = "no"
        self.movesCount = 0
        self.outcome = "lost"
        #self.trigger = "null"
        # Call function attributes
        self.attributes()

    def attributes(self):
        types_dict = TYPES[self.type]
        self.name = types_dict["name"]
        self.rum = types_dict["rum"]
        self.tolerance = types_dict["tolerance"]
        self.rumadd = types_dict["rumadd"]


    def Directions(self, Arrrrrrray):
        self.moves = {}
        self.events = {}
        # if location is not on the north edge, add north to moves
        if self.yLoc != 0:
            self.moves["North"] = [self.xLoc, self.yLoc-1]
            self.events["North"] = Arrrrrrray[self.yLoc-1, self.xLoc]
        # if location is not on the south edge, add south to moves
        if self.yLoc != 15:
            self.moves["South"] = [self.xLoc, self.yLoc+1]
            self.events["south"] = Arrrrrrray[self.yLoc+1, self.xLoc]
        # if location is not on the east edge, add east to moves
        if self.xLoc != 15:
            self.moves["East"] = [self.xLoc+1, self.yLoc]
            self.events["East"] = Arrrrrrray[self.yLoc, self.xLoc+1]
        # if location is not on the west edge, add west to moves
        if self.xLoc != 0:
            self.moves["West"] = [self.xLoc-1, self.yLoc]
            self.events["West"] = Arrrrrrray[self.yLoc, self.xLoc-1]
        # returns a dictionary containing possible moves as the key, and the updated location as the value
        return self.moves, self.events

    def SetUp(self, eventsList, Arrrrrrray):
        # Set game grid by shuffling
        self.Directions(Arrrrrrray)
        while 5 in self.events.values():
            random.shuffle(eventsList)
            # get new start position
            index = eventsList.index(10)
            self.xLoc = index % 16
            self.yLoc = index / 16
            # get new array
            Arrrrrrray = numpy.array(eventsList).reshape(16,16)
            # get new directions
            self.Directions(Arrrrrrray)

        # Set Map
        n = 0
        # Update points feature class with current location
        with arcpy.da.UpdateCursor("pointsLayer", ["Events", "Visible"]) as cursor:
            for row in cursor:
                row[0] = eventsList[n]
                if eventsList[n] == 10:
                    row[1] = eventsList[n]
                else:
                    row[1] = "0"
                cursor.updateRow(row)
                n +=1
        # Clear moves from previous game
        self.MapUpdate("Moves", 0, "all")


        # Print map at start showing only start location
        mxd = arcpy.mapping.MapDocument("Piratopolis.mxd")
        arcpy.mapping.ExportToPDF(mxd, "map.PDF")
        # Open map
        os.startfile("map.PDF")

        # Find treasure locations
        # Get x and y coordinates for treasure and flags
        treasurey, treasurex = numpy.where((Arrrrrrray == 4)|(Arrrrrrray == 5))
        # Create an empty dictionary of treasure locations
        self.treasure = {}
        # Get number of treasures
        number = len(treasurex)
        # fill dictionary with treasure locations
        for n in range(number):
            self.treasure[n] = [treasurex[n], treasurey[n]]

        return eventsList, Arrrrrrray

    def Move(self,answer):
        Loc = self.moves[answer]
        # update location
        self.xLoc = Loc[0]
        self.yLoc = Loc[1]
        # Drink 1 rum
        self.rum -= 1
        # Update moves count
        self.movesCount += 1
        print "{}ward we go!\n".format(answer)
        return self.xLoc, self.yLoc, self.rum

    def Drunk(self, answer):
        # drink an extra rum - now you're drunk!
        self.rum -= 1
        directions = [answer]
        # add possible moves to randomly choose from
        for key in self.moves:
            directions.append(key)
        # choose a random direction
        newDirection = random.choice(directions)
        if newDirection != answer:
            print "Woa! Watch that drink. Looks like you're going " + newDirection + " instead.\n"
        else:
            print "You're swaying a bit but you've managed to stay on course.\n"

        self.Move(newDirection)
        

    def Events(self, Arrrrrrray):
        event = Arrrrrrray[self.yLoc, self.xLoc]
        if event == 1: # You've hit rum, add rum
            print "Drink up me hearty, yo-ho!"
            time.sleep(1)
            with open("rum.txt", 'r') as f:
                print f.read()
            time.sleep(1)
            # add rum but stop infinite collection of rum as revisits are unlimited
            if self.rum <= self.tolerance + 10:
                self.rum += self.rumadd
            else:
                print "Sink me! You can't keep taking rum like that!\nNo more rum has been added to your stock."

        elif event == 2: # You've hit an island, lose 3 rum, get drunk, point to treasure
            print "You've hit and island and are marooned."
            time.sleep(1)
            with open("island.txt", 'r') as f:
                print f.read()
            time.sleep(1)
            self.rum -= 3
            self.drunk = "yes"
            self.trigger = "island"
            self.Point()
        
        elif event == 3: # You've hit the kraken - end
            print "You've been eaten by the kraken."
            time.sleep(1)
            with open("kraken.txt", 'r') as f:
                print f.read()
            self.rum = 0
            time.sleep(1)

        elif event == 4: # Someone's been here before, lose 3 rum, get drunk, point to treasure
            print "Too bad, this treasure has already been taken!"
            time.sleep(1)
            with open("flag.txt", 'r') as f:
                print f.read()
            time.sleep(1)
            self.rum -= 3
            self.drunk = "yes"
            self.trigger = "flag"
            print self.treasure
            treasure = [k for k, v in self.treasure.items() if v == [self.xLoc, self.yLoc]]
            del self.treasure[treasure[0]]
            print self.treasure
            self.Point()
        
        elif event == 5: # You've struck treasure - win!
            print "Treasure! You win!"
            time.sleep(1)
            with open("gold.txt", 'r') as f:
                print f.read()
            self.outcome = "won"
            self.rum = 0
            time.sleep(1)

        elif event == 6:
            print "You have discovered a map fragment!\nPlease wait while your map loads.\n"
            
            #Update moves layer with current location
            self.MapUpdate("Moves", 2, "current")

            # name map
            mapBase = os.path.splitext("map.PDF")
            mapName = "{0}{1}{2}".format(mapBase[0], str(self.movesCount), mapBase[1])
            # print map
            mxd = arcpy.mapping.MapDocument("Piratopolis.mxd")
            arcpy.mapping.ExportToPDF(mxd, mapName)
            os.startfile(mapName)

        else:
            x = random.randint(0,1)
            if x == 0:
                print "No treasure here but no beasties either.\nYou're safe for now, best keep moving.\n"
            else:
                print "Ahoy matey! It's a silly parrot!\n"
                z = random.randint(1,len(Jokes))
                print Jokes[z]
                print ""
            time.sleep(1)

    def MapUpdate(self, layer, value, type):
        # if updating moves layer
        if layer == "Moves":
            fid = str(16*self.xLoc + self.yLoc)
            if type == "current":
                # Select FID = list index
                query = '"FID" = {}'.format(fid)
            else:
                query = ""

            # update current location
            with arcpy.da.UpdateCursor("movesLayer", "Moves", query) as cursor:
                for row in cursor:
                    row[0] = value
                    cursor.updateRow(row)
        
        # If updating points layer
        elif layer == "Points":
            fid = str(16*self.yLoc + self.xLoc)
            if type == "current":
                # Select FID = list index
                query = '"FID" = {}'.format(fid)
            else:
                query = ""
            # add current location to visible
            with arcpy.da.UpdateCursor("pointsLayer", ["Events", "Visible"], query) as cursor2:
                for row2 in cursor2:
                    # if value is zero, update visible with events
                    if value == 0:
                        row2[1] = row2[0]
                    # else update visible with value (pointer)
                    else:
                        row2[1] = value
                    cursor2.updateRow(row2)
        


    def Warning(self):
        kraken = []
        # if the cracken is in one of your possible moves
        for key in self.events:
            if self.events[key] ==3:
                kraken.append(key)

        if len(kraken) > 0:
            print "Watch out! There's something lurking in the depths nearby.\nRumour has it that drink gives you special sight.\n"
            answer = raw_input("Would you like to drink some extra rum?\n>>>").lower().strip()
            if answer == "yes":
                print "\nBest avoid heading {}\n".format(kraken[0])
                self.rum -= 3
                self.drunk = "yes"
                self.trigger = "kraken"
                self.Point()
                return self.rum, self.drunk
            else:
                print "\nTake your chances then! Good luck!\n"
        time.sleep(1)

    
    def Point(self):

        # Calculate distance between each treasure and current location
        distance = {}
        for key in self.treasure:
            xdiff = abs(self.xLoc - self.treasure[key][0])
            ydiff = abs(self.yLoc - self.treasure[key][1])
            distance[key] = xdiff + ydiff

        # get the key for the closest treasure/flag
        closest = min(distance, key=distance.get)

        # get the difference between the x and y locations of the closest treasure/flag and character
        xclose = self.xLoc - self.treasure[closest][0]
        yclose = self.yLoc - self.treasure[closest][1]

        # if y is further than x
        if abs(xclose) < abs(yclose):
            # and y is positive - north
            if yclose > 0:
                point = "North"
                pointVal = 11
            # y is negative - south
            else:
                point = "South"
                pointVal = 12
        # if x is further than y
        else:
            # and x is positive - east
            if xclose < 0:
                point = "East"
                pointVal = 13
            # x is negative - west
            else:
                point = "West"
                pointVal = 14

        self.MapUpdate("Points", pointVal, "current")
        
        if self.trigger == "island":
            print "What better to do than drink rum?\nYo Ho! Is that treasure to the {}?\n".format(point)
        elif self.trigger == "flag":
            print "While drinking your sorrows away you have sensed some more pieces of eight to the {}.\n".format(point)
        elif self.trigger == "kraken":
            print "But blimey! Is that treasure to the {}?\n".format(point)
        #if self.trigger == "drunk":
        else:
            print "Yaaaarrr! All this grog is making you hallucinate!\nYou think you may have spotted some dubloons to the {}\n".format(point)

    def GameOver(self, Play):
        with open("gameover.txt", 'r') as f:
            print f.read() + "\n"
        print "Thanks for playing! Your final map is printing."
        
        #Update moves layer with current location
        self.MapUpdate("Moves",2, "current")

        # add all events to visible
        self.MapUpdate("Points",0, "all")


        # Print map at start showing only start location
        mxd = arcpy.mapping.MapDocument("Piratopolis.mxd")
        arcpy.mapping.ExportToPDF(mxd, "mapFinal.PDF")
        os.startfile("mapFinal.PDF")
        answer = raw_input("Would you like to exit now?\n>>>").lower().strip()
        if answer == "yes":
            Play = 0
        else:
            print "Yo Ho! Let's play again!\nPlease close your maps to allow overwrite.\n"
            time.sleep(2)
        return Play
            
        
# ----------------------------------------------------------------------------------------------#
#                                     START MAIN SCRIPT                                         #
#-----------------------------------------------------------------------------------------------#


#--- GAME SET-UP ---#

# Allow overwrite
arcpy.env.overwriteOutput = True

# Get the folder where the Python scrip resides to allow easy navigation
Folder = os.path.dirname(__file__)

# set workspace
arcpy.env.workspace = Folder

#points feature class showing events on map
points = "points.shp"
arcpy.management.MakeFeatureLayer(points, "pointsLayer")
# moves feature class showing moves on map
positions = "moves.shp"
arcpy.management.MakeFeatureLayer(positions, "movesLayer")

# Print intro text
with open("piratopolis.txt", 'r') as f:
    print f.read() + "\n"

answer = raw_input("Fellow pirate, arr ye game? (Y\N):\n>>>").lower().strip()

if answer == 'y':
    print "Arrrrr\n"

else:
    print "Ye lose"
    quit()

with open("intro.txt", 'r') as f2:
    print f2.read()

#--- BEGIN GAME LOOP ---#

while Play:

    # --- Create game array and map --- #

    # Create an empty list to be appended with events
    eventsList = []
    line = "-"*80
    # Add events to list
    for n in range(256):
        if n == 0:
            eventsList.append(10) # Start x1
        elif n < 2:
            eventsList.append(5) # Treasure x1
        elif n < 4:
            eventsList.append(4) # Flags x2
        elif n < 14:
            eventsList.append(3) # Krakens x10
        elif n < 29:
            eventsList.append(2) # Islands x15
        elif n < 104:
            eventsList.append(1) # Rum x 75
        elif n < 119:
            eventsList.append(6) # Map fragments x 15
        else:
            eventsList.append(0)

    # create game grid
    Arrrrrrray = numpy.array(eventsList).reshape(16,16)

    # start location before shuffling
    start = [0,0]

    # --- Choose character --- #

    # Choose pyrate
    while True:
        char = input("Please choose a pirate!\nFor Captain Lobster Legs type 1\nFor Mad Rodger Sea Wolf type 2\nFor Lady Ailith of Dark Water type 3:\n>>>")
        if char == 1 or 2 or 3:
            # initiate Pirate
            pyrate = Pirate(char, start)
            print "Wise choice! You have chosen to play {}.\nYou have {} bottles of rum in your inventory, and a rum capacity of {}\n".format(pyrate.name, pyrate.rum, pyrate.tolerance)
            break
        else:
            print "invalid choice\n"
            continue

    # start position
    eventsList, Arrrrrrray = pyrate.SetUp(eventsList, Arrrrrrray)

    # Output start position
    print "Your start position is: {}, {}".format(pyrate.xLoc, pyrate.yLoc)
    print "Ahoy! Hold your horses, piratopolis is loading!\n"

    #--- GAME LOOP TO NAVIGATE THROUGH THE MAP TO FIND TREASURE ---#

    # Continue until you run out of rum
    while pyrate.rum > 0:

        # Update location to 1 to indicate location has been visited
        pyrate.MapUpdate("Moves", 1, "current")      

        # Get possible moves
        moves, events = pyrate.Directions(Arrrrrrray)
        # Check for kraken
        if 3 in events.values():
            # warn + give option to see but get drunk
            pyrate.Warning()
        # ask which direction you would like to go
        while True:
            answer = raw_input("Which way would you like to go? {}\n>>>".format(moves.keys())).capitalize().strip()
            if answer in moves.keys():
                # Check if drunk and move accordingly
                if pyrate.drunk == "yes":
                    pyrate.Drunk(answer) # move randomly
                else:
                    pyrate.Move(answer) # move straight
                break
            elif answer == "Exit":
                Play = 0
            else:
                continue


        # Update map
        # add current location to visible
        pyrate.MapUpdate("Points", 0, "current")


        # Check for events!
        pyrate.Events(Arrrrrrray)

        print "Location: {}, {}\nRum: {}\n".format(pyrate.xLoc, pyrate.yLoc, pyrate.rum)
        time.sleep(1)
        # update drunkenness
        if pyrate.rum <= pyrate.tolerance:
            pyrate.drunk = "no"
        else:
            pyrate.drunk = "yes"
            pyrate.trigger = "drunk"
            print "Arrrr!\nLooks like you've been an bit greedy with that rum.\nDrink up but watch you don't trip!\n"
            pyrate.Point()

    Play = pyrate.GameOver(Play)
   










