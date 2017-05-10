#file with all the maps in it
#functions:
#levels.getlevel(levelnumber)
#levels.playerpos(levelnumber)
#levels.ghostpos(levelnumber)

from tilegamelib import Vector

#example level
example= """####################
####################
####################
#bs#################
#y##################
#pgbry5#############
#o##g###############
#br#os##############
#igyp###############
####################"""
ghostposex=[Vector(1, 3)]
playerposex=[Vector(1, 8)]
ghostspeedex=2

#level 1, Tutorial
#player must press every combination of colors to learn
#no ghosts
level1="""####################
####################
####################
####################
####################
####################
####################
########5###########
#ipgbryos###########
####################"""
playerpos1=Vector(1, 8)
ghostpos1=[Vector(1, 8)]
ghostspeed1=1
#TODO: TAKE OUT GHOST. GAME WONT INITIALIZE WITHOUT ONE IN THE LEVEL

#level 2, GHOST!
#player must press every combination of colors to learn but now there's a ghost chasing him...
level2="""
##########
##########
##########
##########
##########
########5#
########o#
########s#
#wwipgbry#
##########"""
playerpos2=Vector(5, 8)
ghostpos2=[Vector(1, 8)]
ghostspeed2=1

#level 2, Track and Field
level3="""
##########
#roypgbwi#
#b######p#
#g######p#
#p######g#
#y######r#
#5######o#
########s#
#wwipgbry#
##########"""
playerpos3=Vector(5, 8)
ghostpos3=[Vector(1, 8)]
ghostspeed3=1

#level 4, Cage Match
level4="""
##########
#wwwwwwws#
#wggggggw#
#woooooow#
#wyyy5yyw#
#wbbbbbbw#
#wrrrrrrw#
#wppppppw#
#swwwwwws#
##########"""
playerpos4=Vector(1, 1)
ghostpos4=[Vector(5,4), Vector(5,5), Vector(5,6)]
ghostspeed4=2

#level 5, Trapped On An Island
level5="""
##########
####so####
###rbow###
##gysrws##
#ysoory5w#
#wpryppww#
##wgsrwo##
###oypw###
####wg####
##########"""
playerpos5=Vector(4, 8)
ghostpos5=[Vector(5,5), Vector(5,6)]
ghostspeed5=2

#level 6, The Maze Runner
level6="""
##########
###wpgb#5#
#ps#s#w#w#
#p####w#o#
#rgbywbgy#
####b#####
#wwprygy##
#s##b##s##
##pio#####
##########"""
playerpos6=Vector(3, 8)
ghostpos6=[Vector(1, 8), Vector(1, 2)]
ghostspeed6=1

#level 7, Outnumbered...
level7="""
##########
#wwwwwwws#
#wggggggw#
#woooooow#
#wyyy5yyw#
#wbbbbbbw#
#wrrrrrrw#
#wppppppw#
#swwwwwws#
##########"""
playerpos7=Vector(1, 1)
ghostpos7=[Vector(5,2), Vector(5,3), Vector(5,4), Vector(5,5), Vector(5,6), Vector(5,7), Vector(5,8)]
ghostspeed7=2

def getlevel(levelnumber):
	if levelnumber == 1:
		return level1
	if levelnumber == 2:
		return level2
	if levelnumber == 3:
		return level3
	if levelnumber == 4:
		return level4
	if levelnumber == 5:
		return level5
	if levelnumber == 6:
		return level6
	if levelnumber == 7:
		return level7

def getghostpos(levelnumber):
	if levelnumber == 1:
		return ghostpos1
	if levelnumber == 2:
		return ghostpos2
	if levelnumber == 3:
		return ghostpos3
	if levelnumber == 4:
		return ghostpos4
	if levelnumber == 5:
		return ghostpos5
	if levelnumber == 6:
		return ghostpos6
	if levelnumber == 7:
		return ghostpos7


def getplayerpos(levelnumber):
	if levelnumber == 1:
		return playerpos1
	if levelnumber == 2:
		return playerpos2
	if levelnumber == 3:
		return playerpos3
	if levelnumber == 4:
		return playerpos4
	if levelnumber == 5:
		return playerpos5
	if levelnumber == 6:
		return playerpos6
	if levelnumber == 7:
		return playerpos7

def getGhostSpeed(levelnumber):
	if levelnumber == 1:
		return ghostspeed1
	if levelnumber == 2:
		return ghostspeed2
	if levelnumber == 3:
		return ghostspeed3
	if levelnumber == 4:
		return ghostspeed4
	if levelnumber == 5:
		return ghostspeed5
	if levelnumber == 6:
		return ghostspeed6
	if levelnumber == 7:
		return ghostspeed7