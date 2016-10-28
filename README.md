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

2016/09/22 - Updated Trade Route module to confirm creation of Trade Routes
Trade Route module can now retrieve currently created trade routes
In the process of creating a "get out of Dodge" feature where it will send the Bot X amount of moves away
from Zero using random warps prior to searching for a trade route.
This will keep all of the bots (hopefully) from finding and establishing the same routes

2016/09/28 - Now retrieves existing trade routes to prevent re-creating existing ones
Implemented a simple path finding mechanism to find the most efficient route between sectors

2016/09/29 - Using proper tables in tinyDB instead of the default
Chasing a bug where on startup - the Bot is unable to find the shortest path to zero, even though
when it previously shut down - there was one...

2016/10/03 - Working on selecting an initial trade route to start trading. (if present)
Modified rsmove.php to ALWAYS ask the player if they want to real space move to a trade route sector -
regardless of the distance.

```
Original code for line 84:

elseif (($destination < $sector_max && empty($engage)) || ($destination < $sector_max && $triptime > 100 && $engage == 1))

Modified code for line 84:

elseif (($destination < $sector_max && empty($engage)) || ($destination < $sector_max && $triptime > 0 && $engage == 1))
```

2016/10/04 - Bot now will examine whether or not it has existing trade routes
If it does, it determines which one is the closest - and then jumps to it.

2016/10/05 - Fixed a bug in the text input routine where it was not properly clearing already filled in text<br>
Implemented executing a trade route the initial time, and optionally multiple times

Now need to investigate the skill level price thresholds.

2016/10/06 - In the process of creating a Ship Status extractor

2016/10/07 - Bot is now able to return to sector 0, and purchase a limited set of tech upgrades:<br>
Hull, Computer and Engines<br>

2016/10/13 - Issue with reading the upgrade costs when selecting a tech level.
The values are rendered via JS and appear as nulls when scanned.  Either going to calculate
the cost ourself, or implement a scripting work-around...

2016/10/14 - Unable to address the JS rendered cost, so implemented our own cost check prior to
attempting the purchase.

2016/10/20 - Refactored the Special Port tech purchase to efficiently select all available ship component
tech levels.  In the process of redoing the skeleton decision making process.

2016/10/28 - Slowly converting all scrape numbers from strings to ints/floats.  Fixed numerous issues with the trade route support lib

