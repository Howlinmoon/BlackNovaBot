# BlackNovaBot

When finished, this will be a computer opponent for Black Nova Traders.
This opponent will follow all of the rules normal human players do,
and it will be using the web interface.

This Bot uses Python and Selenium Web Driver for autonomous automated operation.


2016/09/14 -
Bot can login to the game, creating an account for itself if necessary
Bot can scan the current sector, looking for possible desirable Ore or Goods ports

2016/09/15 - Port Searching
Search algorithm:
```
(Example starting from Sector 25, assume it is an Ore port)

Is the ship in a sector with an Ore or Goods port?
No:
	Move to the next sector in numerical order (26?)
	Back to Top

Yes:
	Scan neighboring sectors (example: 26, 40, 41, 55)
	Found an Ore or Goods port?
		Yes (41):
		 	Does the sector have a path back to this one?
		 	No:
		 		Continue scanning neighboring sectors

			Yes 41:
				travel to the sector (41)
				Is there a compatible port adjacent? (25, 42, 75, 91)
					Yes (75):
						setup a trade route!
					No:
						Return to the previous sector (25)

		No:
			Scan the next sector

Trade Route Found?
	Yes:
		Done!

	No:
		Travel to the next sector number in order. (example - from sector 25, travel to sector 26)
```
2016/09/16 - Implemented search algorithm - need to refactor for code efficiency and remove reuse

2016/09/20 - Refactored the trade route search routine, and fixed a logic bug where it would only
look for Goods ports if at an Ore port and not vice-versa.
Now keeps track of moves required to return to port zero for upgrades / end of session hiding / etc
In the process of creating a trade route support module

2016/09/21 - Created a new Trade Route module which will be used for the creation and maintenance
of trade routes.
Refactored the search routine into a function, and added a call to the create trade route
routine.  Have to add a check to see if the creation succeeded or not.

2015/09/22 - Updated Trade Route module to confirm creation of Trade Routes
Trade Route module can now retrieve currently created trade routes
In the process of creating a "get out of Dodge" feature where it will send the Bot X amount of moves away
from Zero using random warps prior to searching for a trade route.
This will keep all of the bots (hopefully) finding and establishing the same routes