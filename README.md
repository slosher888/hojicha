# hojicha
Sloshers bot for funsies

Features, says hello

* !hojicha [,hi,hello]
* !hojicha speak
	* Tells you a "fortune"
* !hojicha q <yes/no question>
	*Answers a yes/no question
* !hojica pick <comma separated list>
	* picks element from list
* !hojica draw card
	* Single card tarot reading
* !hojica roll ndm (+/-x)
	* Roll m-sided die, n times (with optional modifier)
* !hojicha help
	* Displays every command it knows


	Dependencies
	* fortune python library
	* Fortune database:
		https://github.com/bmc/fortunes.git

Make sure to set `FORTUNE_DB_PATH` in `.env` or you'll make Hojicha sad. T_T
And we can't have that...

## License
You may use any code in this repo but you must:
* Give credit to SlosherDeluxe (that's me)
* Tell me (because I'm nosy)
* Not use any code for commercial purposes
* Make the source code for your project available
