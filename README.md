# Realms RPG

This was a little project I started a while back when I first thought about getting into programming. I knew a handful of Python and thought I woul be able to make a little text based RPG that used random selection to give environment descriptions and pick enemies to fight. Initially everything consistsed of lists and dictionaries, and although it worked, it was very crude and immature in its design. 

I have now rewritten the whole thing to make use of classes, and some tighter code. Unavoidably, a lot of things are still hardcoded, which I might rework in the future. The game is not very balanced as it is now, and the combat is not as sophisticated as I might like it to be. I might rework this in the future, but for now, it is what it is. 

Nevertheless, it was a fun project to get both my Python-brain going, and to get some creative writing done. Everything was made and written by me (yes even the cliche's, I was very inspired by 70's fantasy and dungeon delving games while making this) without the use of any AI. I might mess around with it some more occasionally, but it is in working shape now, and I hope it works for everyone else too.

Enjoy!

## Setting up the environment

First, you need to have python installed on your device.
Using the command line (terminal, or whatever) go to the root folder ```Realms_RPG``` and run the following command:
```Python
source .venv/bin/activate
```
to enter into the virtual environment that has the necessary packages installed. 

Alternatively you can install all the necessary packages locally by running the following command:
```Python
pip install -r requirements.txt
```
You can also use ```pipenv``` or some other environment management tool, but you're probably best off just using the virtual environment that's provided, as it will be updated on each commit if anything changes.

## Running the game

To run the game, simply type
```Bash
python3 main.py
```
or if you have python3 aliased as something else on your system or .bashrc (such as py, for example), the run
```Bash
[alias] main.py
```
## Gameplay

The game mostly runs by selecting from a range of choices. To select a choice simply input the number associated with that choice and press enter. 
Your characters are saved to a ```characters``` folder that will be generated when you make your first characters. To load them, simply type in their name when prompted to do so.
