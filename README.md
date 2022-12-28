# SudOKu
A puzzle in which player enters the number into a grid in specific pattern.
## Video Demo: https://youtu.be/lTJU5zP4U5g
## Description:

+ SudOKu is a **flask application**. It is a game that is made with the registration facility.<br/><br/>
+ A User can register him/her in SudOKu.<br/><br/>
+ They are registered with validation of their username and password. After that they are allowed to log in into the app.<br/><br/>
+ This app contains a navigation bar which is displayed after the user logs in which contains **menu, rules,reset and logout** links.<br/><br/>
+ After logging in they can view a menu page which has bascially three levels. User can play any of the levels anytime without clearing the previous one.<br/><br/>
+ Level 1 is of **6 * 6**. Level 2 and Level 3 are of **9 * 9**.<br/><br/>
+ SudOKu also provides a user, knowledge about how to play this game if he/she is unaware about the game rules.<br/><br/>
+ If the user has **won** the level their menu page will be updated to **play again** in front of that specific level, to **reset** this click the **reset** button in **navigation bar**.<br/><br/>
+ It also allows logout facility along with the needy validation during registration and logging.<br/><br/>
+ sqlite3 is used for varoius database operations.<br/><br/>

## Information about project files<br/>
## flask_app.py
+ It contains main code through which the application runs.<br/>

## helpers.py
+ It contains function to define login_required function.<br/>

## final.db
+ This file defines the database needed by the flask application.

## Templates Directory
### It contains following .html files:
+ layout.html: It specifies layout which is common for all pages.
+ lvl1.html: It specifies level 1 layout.
+ lvl2.html: It specifies level 2 layout.
+ lvl3.html: It specifies level 3 layout.
+ register.html: It specifies registration page layout.
+ login.html: It specifies login page layout.
+ index.html: It specifies home page layout.
+ rules.html: It specifies rules page layout.<br/><br/>

## static Directory
### It contains following files:
+ style.css: It defines css for layout file.
+ s2.png: It is the image that is put in the navigation bar.
+ favicon.jpg: It is the icon image used in title bar.<br/>

## Structure of the Project
+ project/
    + flask_app.py
    + helpers.py
    + templates/
        + layout.html
        + lvl1.html
        + lvl2.html
        + lvl3.html
        + register.html
        + login.html
        + index.html.
        + rules.html
    + static/
        + styles.css
        + s2.png
        + favicon.jpg
    + final.db