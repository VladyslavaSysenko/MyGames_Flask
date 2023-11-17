# My Games
## Video Demo:  <https://youtu.be/1cfEG5iaJcY>
## Description:

My CS50 final progect is **My Games** for board games enthusiasts :)

It is a web-based application using JavaScript, Python, and SQL.

I love board games but I have bad memory, so with time I always forget my impression about played games. That is why i decided to make a website where all memories are being collected in one place!

 To begin, you need to register. After that, you will see the first where you can add board games in which you played with review, rating, belonging, price, picture and date. You can also sort them by name, rating, date, price and owning.

The next page is "random" where you can choose a first player or make a random order of players. To do so, you need to press the "start" button, type one letter/number for each person and then press "first player" or "random order". You can press again and change if you want.

Lastly, you can see a page "More games" with a list of websites where you can search for new interesting games. At first there will be default sites but you can delete them and add other ones.

---

## Files:
* *"app.py"* is the main file, in which all magic happens ;) It binds all files together and processes all information. It has such functions:
    * *login_required* decorates routes to require login.
    * *apology* shows funny picture with apology text if user did something wrong.
    * *register* checks all the register requirements and registers user.
    * *login* checks all login requirements and logins a user.
    * *mygames* shows user's games on the main page.
    * *add* adds a new game into the database.
    * *sort* sorts games as user wish.
    * *delete* deletes a game.
    * *random* renders "random" page.
    * *search* shows user's sites.
    * *add_site* adds a new site into the database.
    * *delete_site* deletes a site.
    * *logout* logs a user out.
* *"data.db"* is a database where all users, games, default sites and user's sites are stored.
    * "users" table contains id, username and hash.
    * "sites" table contains person id, site id, site name and url to website.
    * "games" table contains game id, person id, game name, review, rating, price, picture, owning and date.
    * "default_sites" table contains default sites that will be added to new user.
* folder *"static"*
    * *"dice.png"* is a site's icon.
    * *"styles.css"* is a file where all visual changes are collected.
* folder *"templates"*
    * *"apology.html"* contains a picture and is used when user did something wrong.
    * *"layout.html"* contains navigation bar for all pages.
    * *"login.html"* and *"register.html"* contain a login page and a register page respectively.
    * *"mygames.html"* contains main page (My games) where you will see all your games and add a new one.
    * *"random.html"* contains second page (Random) where you can choose a first player or random order of players.
    * *"searchgames.html"* contains third page (More games) where you can collect all sites where you look for new games. At first you will see default websites but feel free to delete them and add ones of your choice.

    ## To start the app:
    - From root folder run ***python app/app.py***