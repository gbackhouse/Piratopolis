# Piratopolis
Python pirate text-based adventure game

Piratopolis was created for a challenge as part of a university course and is currently in Beta.

---- DEPENDENCIES ----

Python 2.7.18
arcpy
time
os
numpy
random

Please note that this game requires ArcGIS

Please ensure that all files within Piratopolis.zip are downloaded and stored into the same folder.
These are:
- piratopolis.py
- Piratopolis.mxd
- shapefiles:
  -  moves
  -  points
  -  reference
- text files:
  - piratopolis
  - intro
  - gameover
  - rum
  - kraken
  - island
  - flag
  - gold

If your map PDF fails to update properly please open Piratopolis.mxd in ArcMAP and ensure the path to each
of the layers is correct

---- GAME DESCRITPION ----

The objective of the game is to find the treasure before you run out of rum.
You will start with a blank map, showing only your start location. As you
discover items in the map, they will become visible in subsequent maps.

Rum stockpiles are scattered throughout the map and may be revisited any number
of times to collect more rum if you are running low.

You have a maximum amount of rum you can carry before you are forced to drink
extra, resulting in you becoming drunk.
When you are drunk, you will see the direction of the closest treasure, however
some of the treasure has already been taken by pirates who have ventured before
you. When drunk you are not very good at walking straight, and may not go in
your desired direction.

Avast Ye! There are also kraken about. Running into one of these beasties will
result in you losing the game. You will be warned when one is nearby and offered
the option of drinking extra rum to gain sight. Remeber though, drinking extra
rum gets you drunk, and though you know where the kraken is, you may not move
in the desired direction.

There are also islands which will leave you marooned, and map fragments which
will print your course thus far when you hit them.

You will choose between 3 pirate characters with different start levels of rum,
rum capacity, and rum collection from stockpiles.

---- ACKNOWLEDGEMENTS ----

This game would be significantly less fun without my fun-tester Daryl D'Cruz
Pirate jokes are taken from boredpanda.com and kidadl.com
