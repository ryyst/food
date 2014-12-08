Food
====

Python script for printing the menus of student restaurants in Turku. Intended for all the local command-line junkies. :)


### Prerequisites

This script requires the following:
*  Python 3.3
*  beautifulsoup4
*  GNU/Linux

Notes:
*  Any version of Python3.X might do, 3.0 worked on quick tests.
*  Not tested on Windows, could work with minimal fixes


### Installation

On a newer Debian/Ubuntu system installing the required packages should be as easy as this:

    sudo apt-get update && sudo apt-get install git python3 python3-bs4
    
After you have the prerequisites installed, just run this:

    git clone https://github.com/Rippentrop/food && cd food && chmod +x food.py

Then just symlink food.py to your $PATH or put an alias on it. Whatever you like the most. A singleliner for aliasing:

    echo 'alias food="python3 ~/food/food.py"' >> ~/.bashrc && source ~/.bashrc

Now you can run it with just `food`!

### Usage

This script supports most Unica and Sodexo restaurants.

Default user configuration in config.py, just remember to follow Python syntax while editing it.

Proper configuration is recommended, because the script will then cache the data for whole week when using config values. When using arguments the script will redownload the data every time.

For quickly checking other restaurants/prices/etc. you can use arguments.

#### Example

_Check Sodexo restaurants **ict** and **eurocity**, print only **today** in **english** with **other** pricelevel_

    > food -s ict eurocity -t -p other -l en
    
    Today's menu (08.12.14)
     Eurocity (Sodexo)
      [ 7,70 ] Fried frankfurter {G VL}
      [ 8,60 ] Beef stir fry, chili sauce {G M}
      [ 7,70 ] Ham and tomato pizza {VL}
      [ 5,10 ] Carrot and tarragon soup {G VL}
      [ 6,60 ] Salad buffe 
      [ 1,10 ] Berry kissel {G}
      
     Ict (Sodexo)
      [ 4,90 ] Meatballs in tomato sauce 
      [ 4,90 ] Mozzarella and tomato casserole {G VL}
      [ 7,40 ] Fish ala wallenberg {VL}
      [ 3,70 ] Wild mushroom soup {L}
      [ 4,45 ] Chicken salad {G M}
