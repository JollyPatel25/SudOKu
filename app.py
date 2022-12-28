from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from helpers import login_required
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import re

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#Connect the database
connection = sqlite3.connect("final.db", check_same_thread=False)
connection.row_factory = sqlite3.Row
db = connection.cursor()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/lvl1", methods=["GET", "POST"])
@login_required
def lvl1():

    #initialize basics
    count = 6
    db.execute("select * from users where id = ?", [session["user_id"]])
    record = db.fetchall()
    user = record[0]
    matrix = [[4,0,0,0,6,3],[0,0,0,0,0,0],[0,0,0,0,5,0],[0,6,0,0,4,0],[0,2,3,5,0,0],[0,1,0,2,0,0]]

    #if request method is post
    if request.method == "POST":

        #check if original game is not changed
        for i in range(count):
            for j in range(count):
                #check if exists
                if not request.form.get("i"+str(i)+str(j)) or request.form.get("i"+str(i)+str(j) == ''):
                    notify = "Specify Every Element To Submit!"
                    return render_template("lvl1.html", count=count, matrix=matrix, notify=notify)

                element = int(request.form.get("i"+str(i)+str(j)))

                #check for fix element position
                if matrix[i][j] != 0:

                    #check if fixed element is changed or not
                    if matrix[i][j] != element:
                        notify = "Good Try But Play Again!"
                        return render_template("lvl1.html", notify=notify, matrix=matrix, count=count)


        #check if existing every element is present
        #declare array for storing answers
        chkmatrix = [[0 for i in range(count)] for j in range(count)]

        #loop to store answers in array
        for i in range(count):
            for j in range(count):
                #check if exists
                if not request.form.get("i"+str(i)+str(j)) or request.form.get("i"+str(i)+str(j) == ''):
                    notify = "Specify Every Element To Submit!"
                    return render_template("lvl1.html", count=count, matrix=matrix, notify=notify)

                #get element in a variable
                element = int(request.form.get("i"+str(i)+str(j)))

                #if alright store answer
                chkmatrix[i][j] = element

        #check for correct answers
        #calulate number count in answers
        element_count = [0 for i in range(count)]
        othernumber = 0
        for i in range(count):
            for j in range(count):
                if chkmatrix[i][j] == 1:
                    element_count[0] += 1
                elif chkmatrix[i][j] == 2:
                    element_count[1] += 1
                elif chkmatrix[i][j] == 3:
                    element_count[2] += 1
                elif chkmatrix[i][j] == 4:
                    element_count[3] += 1
                elif chkmatrix[i][j] == 5:
                    element_count[4] += 1
                elif chkmatrix[i][j] == 6:
                    element_count[5] += 1
                else:
                    othernumber += 1

        #check for element count
        for i in range(count):
            if element_count[i] > count or othernumber != 0:
                notify = "Game Played Incorrectly!"
                return render_template("lvl1.html",notify=notify,matrix=matrix, count=count)

        #check for row correction
        #count element of row
        element_row_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if chkmatrix[i][j] == 1:
                    element_row_count[i][0] += 1
                elif chkmatrix[i][j] == 2:
                    element_row_count[i][1] += 1
                elif chkmatrix[i][j] == 3:
                    element_row_count[i][2] += 1
                elif chkmatrix[i][j] == 4:
                    element_row_count[i][3] += 1
                elif chkmatrix[i][j] == 5:
                    element_row_count[i][4] += 1
                elif chkmatrix[i][j] == 6:
                    element_row_count[i][5] += 1

        #check for element row count
        for i in range(count):
            for j in range(count):
                if element_row_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl1.html",notify=notify, count=count, matrix=matrix)


        #check for column correction
        #count element of column
        element_column_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if chkmatrix[j][i] == 1:
                    element_column_count[i][0] += 1
                elif chkmatrix[j][i] == 2:
                    element_column_count[i][1] += 1
                elif chkmatrix[j][i] == 3:
                    element_column_count[i][2] += 1
                elif chkmatrix[j][i] == 4:
                    element_column_count[i][3] += 1
                elif chkmatrix[j][i] == 5:
                    element_column_count[i][4] += 1
                elif chkmatrix[j][i] == 6:
                    element_column_count[i][5] += 1

        #check for element column count
        for i in range(count):
            for j in range(count):
                if element_column_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl1.html", notify=notify, count=count, matrix=matrix)

        #check for box correction
        #check for box element count
        element_box_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if i <= 1 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[0][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[0][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[0][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[0][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[0][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[0][5] += 1

                elif i <= 3 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[1][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[1][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[1][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[1][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[1][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[1][5] += 1
                elif i <= 5 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[2][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[2][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[2][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[2][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[2][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[2][5] += 1
                elif i <= 1 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[3][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[3][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[3][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[3][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[3][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[3][5] += 1
                elif i <= 3 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[4][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[4][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[4][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[4][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[4][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[4][5] += 1
                elif i <= 5 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[5][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[5][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[5][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[5][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[5][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[5][5] += 1

        #check for element box count
        for i in range(count):
            for j in range(count):
                if element_box_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl1.html", notify=notify, count=count, matrix=matrix)

        #if user has won the level
        notify = "Played Well!"
        sql = "update users set lvl1 = 'Yes' where username = '" + user["username"]+"'"
        db.execute(sql)
        connection.commit()
        notify=sql
        return redirect("/lvl2")
    else:
        #if method is get
        notify = "Start Playing Level 1!"
        return render_template("lvl1.html", matrix=matrix, notify=notify, count=count)





@app.route("/lvl2", methods=["GET", "POST"])
@login_required
def lvl2():

    #initialize basics
    count = 9
    matrix = [[0,0,4,7,1,0,0,0,0],[0,7,2,8,0,6,5,0,0],[0,0,0,0,0,5,0,0,7],
              [0,1,0,6,9,0,2,0,0],[3,9,0,0,5,0,0,0,0],[0,0,0,0,0,0,0,8,5],
              [0,0,1,2,3,0,8,0,4],[0,0,3,5,0,4,0,0,2],[2,4,0,9,0,0,0,0,0]]
    db.execute("select * from users where id = ?", [session["user_id"]])
    record = db.fetchall()
    user = record[0]

    #if method is post
    if request.method == "POST":

        #check if original game is not changed
        for i in range(count):
            for j in range(count):

                #check if exists
                if not request.form.get("i"+str(i)+str(j)) or request.form.get("i"+str(i)+str(j) == ''):
                    notify = "Specify Every Element To Submit!"
                    return render_template("lvl2.html", count=count, matrix=matrix, notify=notify)

                element = int(request.form.get("i"+str(i)+str(j)))

                #check for fix element position
                if matrix[i][j] != 0:

                    #check if fixed element is changed or not
                    if matrix[i][j] != element:
                        notify = "Good Try But Play Again!"
                        return render_template("lvl2.html", notify=notify, matrix=matrix, count=count)


        #check if existing every element is present
        #declare array for storing answers
        chkmatrix = [[0 for i in range(count)] for j in range(count)]

        #loop to store answers in array
        for i in range(count):
            for j in range(count):
                #check if exists
                if not request.form.get("i"+str(i)+str(j)) or request.form.get("i"+str(i)+str(j) == ''):
                    notify = "Specify Every Element To Submit!"
                    return render_template("lvl2.html", count=count, matrix=matrix, notify=notify)

                #get element in a variable
                element = int(request.form.get("i"+str(i)+str(j)))

                #if alright store answer
                chkmatrix[i][j] = element

        #check for correct answers
        #calulate number count in answers
        element_count = [0 for i in range(count)]
        othernumber = 0
        for i in range(count):
            for j in range(count):
                if chkmatrix[i][j] == 1:
                    element_count[0] += 1
                elif chkmatrix[i][j] == 2:
                    element_count[1] += 1
                elif chkmatrix[i][j] == 3:
                    element_count[2] += 1
                elif chkmatrix[i][j] == 4:
                    element_count[3] += 1
                elif chkmatrix[i][j] == 5:
                    element_count[4] += 1
                elif chkmatrix[i][j] == 6:
                    element_count[5] += 1
                elif chkmatrix[i][j] == 7:
                    element_count[6] += 1
                elif chkmatrix[i][j] == 8:
                    element_count[7] += 1
                elif chkmatrix[i][j] == 9:
                    element_count[8] += 1
                else:
                    othernumber += 1

        #check for element count
        for i in range(count):
            if element_count[i] > count or othernumber != 0:
                notify = "Game Played Incorrectly!"
                return render_template("lvl2.html",notify=notify,matrix=matrix, count=count)

        #check for row correction
        #count element of row
        element_row_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if chkmatrix[i][j] == 1:
                    element_row_count[i][0] += 1
                elif chkmatrix[i][j] == 2:
                    element_row_count[i][1] += 1
                elif chkmatrix[i][j] == 3:
                    element_row_count[i][2] += 1
                elif chkmatrix[i][j] == 4:
                    element_row_count[i][3] += 1
                elif chkmatrix[i][j] == 5:
                    element_row_count[i][4] += 1
                elif chkmatrix[i][j] == 6:
                    element_row_count[i][5] += 1
                elif chkmatrix[i][j] == 7:
                    element_row_count[i][6] += 1
                elif chkmatrix[i][j] == 8:
                    element_row_count[i][7] += 1
                elif chkmatrix[i][j] == 9:
                    element_row_count[i][8] += 1

        #check for element row count
        for i in range(count):
            for j in range(count):
                if element_row_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl2.html",notify=notify, count=count, matrix=matrix)


        #check for column correction
        #count element of column
        element_column_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if chkmatrix[j][i] == 1:
                    element_column_count[i][0] += 1
                elif chkmatrix[j][i] == 2:
                    element_column_count[i][1] += 1
                elif chkmatrix[j][i] == 3:
                    element_column_count[i][2] += 1
                elif chkmatrix[j][i] == 4:
                    element_column_count[i][3] += 1
                elif chkmatrix[j][i] == 5:
                    element_column_count[i][4] += 1
                elif chkmatrix[j][i] == 6:
                    element_column_count[i][5] += 1
                elif chkmatrix[j][i] == 7:
                    element_column_count[i][6] += 1
                elif chkmatrix[j][i] == 8:
                    element_column_count[i][7] += 1
                elif chkmatrix[j][i] == 9:
                    element_column_count[i][8] += 1


        #check for element column count
        for i in range(count):
            for j in range(count):
                if element_column_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl2.html", notify=notify, count=count, matrix=matrix)

        #check for box correction
        #check for box element count
        element_box_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if i <= 2 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[0][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[0][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[0][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[0][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[0][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[0][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[0][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[0][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[0][8] += 1

                elif i <= 5 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[1][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[1][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[1][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[1][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[1][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[1][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[1][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[1][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[1][8] += 1

                elif i <= 8 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[2][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[2][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[2][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[2][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[2][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[2][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[2][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[2][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[2][8] += 1


                elif i <= 2 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[3][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[3][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[3][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[3][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[3][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[3][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[3][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[3][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[3][8] += 1


                elif i <= 5 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[4][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[4][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[4][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[4][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[4][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[4][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[4][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[4][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[4][8] += 1


                elif i <= 8 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[5][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[5][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[5][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[5][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[5][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[5][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[5][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[5][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[5][8] += 1


                elif i <= 2 and j <= 8:
                    if chkmatrix[i][j] == 1:
                        element_box_count[6][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[6][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[6][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[6][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[6][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[6][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[6][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[6][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[6][8] += 1


                elif i <= 5 and j <= 8:
                    if chkmatrix[i][j] == 1:
                        element_box_count[7][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[7][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[7][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[7][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[7][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[7][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[7][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[7][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[7][8] += 1


                elif i <= 8 and j <= 8:
                    if chkmatrix[i][j] == 1:
                        element_box_count[8][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[8][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[8][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[8][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[8][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[8][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[8][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[8][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[8][8] += 1

        #check for element box count
        for i in range(count):
            for j in range(count):
                if element_box_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl2.html", notify=notify, count=count, matrix=matrix)

        #if user has won level2
        notify = "Played Well!"
        sql = "update users set lvl2 = 'Yes' where username = '" + user["username"]+"'"
        db.execute(sql)
        connection.commit()
        notify = sql
        return redirect("/lvl3")

    else:
        notify = "Start Playing Level2!"
        return render_template("lvl2.html", matrix=matrix, notify=notify, count=count)

@app.route("/lvl3", methods=["GET", "POST"])
@login_required
def lvl3():
        #initialize basics
    count = 9
    matrix = [[0,0,4,6,0,5,8,0,0],[6,0,0,0,0,0,0,0,0],[0,0,0,0,4,7,6,0,5],
              [2,8,0,3,0,0,0,0,0],[7,4,0,0,0,8,2,5,0],[0,0,0,0,0,0,9,0,0],
              [0,2,5,7,0,0,3,6,0],[4,3,0,0,2,0,0,8,0],[0,0,0,8,6,3,5,4,0]]
    db.execute("select * from users where id = ?", [session["user_id"]])
    record = db.fetchall()
    user = record[0]

    #if method is post
    if request.method == "POST":

        #check if original game is not changed
        for i in range(count):
            for j in range(count):

                #check if exists
                if not request.form.get("i"+str(i)+str(j)) or request.form.get("i"+str(i)+str(j) == ''):
                    notify = "Specify Every Element To Submit!"
                    return render_template("lvl3.html", count=count, matrix=matrix, notify=notify)

                element = int(request.form.get("i"+str(i)+str(j)))

                #check for fix element position
                if matrix[i][j] != 0:

                    #check if fixed element is changed or not
                    if matrix[i][j] != element:
                        notify = "Good Try But Play Again!"
                        return render_template("lvl3.html", notify=notify, matrix=matrix, count=count)


        #check if existing every element is present
        #declare array for storing answers
        chkmatrix = [[0 for i in range(count)] for j in range(count)]

        #loop to store answers in array
        for i in range(count):
            for j in range(count):
                #check if exists
                if not request.form.get("i"+str(i)+str(j)) or request.form.get("i"+str(i)+str(j) == ''):
                    notify = "Specify Every Element To Submit!"
                    return render_template("lvl3.html", count=count, matrix=matrix, notify=notify)

                #get element in a variable
                element = int(request.form.get("i"+str(i)+str(j)))

                #if alright store answer
                chkmatrix[i][j] = element

        #check for correct answers
        #calulate number count in answers
        element_count = [0 for i in range(count)]
        othernumber = 0
        for i in range(count):
            for j in range(count):
                if chkmatrix[i][j] == 1:
                    element_count[0] += 1
                elif chkmatrix[i][j] == 2:
                    element_count[1] += 1
                elif chkmatrix[i][j] == 3:
                    element_count[2] += 1
                elif chkmatrix[i][j] == 4:
                    element_count[3] += 1
                elif chkmatrix[i][j] == 5:
                    element_count[4] += 1
                elif chkmatrix[i][j] == 6:
                    element_count[5] += 1
                elif chkmatrix[i][j] == 7:
                    element_count[6] += 1
                elif chkmatrix[i][j] == 8:
                    element_count[7] += 1
                elif chkmatrix[i][j] == 9:
                    element_count[8] += 1
                else:
                    othernumber += 1

        #check for element count
        for i in range(count):
            if element_count[i] > count or othernumber != 0:
                notify = "Game Played Incorrectly!"
                return render_template("lvl3.html",notify=notify,matrix=matrix, count=count)

        #check for row correction
        #count element of row
        element_row_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if chkmatrix[i][j] == 1:
                    element_row_count[i][0] += 1
                elif chkmatrix[i][j] == 2:
                    element_row_count[i][1] += 1
                elif chkmatrix[i][j] == 3:
                    element_row_count[i][2] += 1
                elif chkmatrix[i][j] == 4:
                    element_row_count[i][3] += 1
                elif chkmatrix[i][j] == 5:
                    element_row_count[i][4] += 1
                elif chkmatrix[i][j] == 6:
                    element_row_count[i][5] += 1
                elif chkmatrix[i][j] == 7:
                    element_row_count[i][6] += 1
                elif chkmatrix[i][j] == 8:
                    element_row_count[i][7] += 1
                elif chkmatrix[i][j] == 9:
                    element_row_count[i][8] += 1

        #check for element row count
        for i in range(count):
            for j in range(count):
                if element_row_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl3.html",notify=notify, count=count, matrix=matrix)


        #check for column correction
        #count element of column
        element_column_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if chkmatrix[j][i] == 1:
                    element_column_count[i][0] += 1
                elif chkmatrix[j][i] == 2:
                    element_column_count[i][1] += 1
                elif chkmatrix[j][i] == 3:
                    element_column_count[i][2] += 1
                elif chkmatrix[j][i] == 4:
                    element_column_count[i][3] += 1
                elif chkmatrix[j][i] == 5:
                    element_column_count[i][4] += 1
                elif chkmatrix[j][i] == 6:
                    element_column_count[i][5] += 1
                elif chkmatrix[j][i] == 7:
                    element_column_count[i][6] += 1
                elif chkmatrix[j][i] == 8:
                    element_column_count[i][7] += 1
                elif chkmatrix[j][i] == 9:
                    element_column_count[i][8] += 1


        #check for element column count
        for i in range(count):
            for j in range(count):
                if element_column_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl3.html", notify=notify, count=count, matrix=matrix)

        #check for box correction
        #check for box element count
        element_box_count = [[0 for i in range(count)] for j in range(count)]
        for i in range(count):
            for j in range(count):
                if i <= 2 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[0][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[0][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[0][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[0][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[0][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[0][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[0][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[0][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[0][8] += 1

                elif i <= 5 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[1][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[1][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[1][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[1][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[1][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[1][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[1][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[1][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[1][8] += 1

                elif i <= 8 and j <= 2:
                    if chkmatrix[i][j] == 1:
                        element_box_count[2][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[2][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[2][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[2][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[2][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[2][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[2][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[2][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[2][8] += 1


                elif i <= 2 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[3][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[3][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[3][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[3][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[3][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[3][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[3][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[3][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[3][8] += 1


                elif i <= 5 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[4][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[4][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[4][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[4][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[4][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[4][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[4][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[4][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[4][8] += 1


                elif i <= 8 and j <= 5:
                    if chkmatrix[i][j] == 1:
                        element_box_count[5][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[5][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[5][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[5][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[5][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[5][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[5][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[5][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[5][8] += 1


                elif i <= 2 and j <= 8:
                    if chkmatrix[i][j] == 1:
                        element_box_count[6][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[6][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[6][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[6][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[6][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[6][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[6][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[6][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[6][8] += 1


                elif i <= 5 and j <= 8:
                    if chkmatrix[i][j] == 1:
                        element_box_count[7][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[7][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[7][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[7][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[7][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[7][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[7][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[7][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[7][8] += 1


                elif i <= 8 and j <= 8:
                    if chkmatrix[i][j] == 1:
                        element_box_count[8][0] += 1
                    elif chkmatrix[i][j] == 2:
                        element_box_count[8][1] += 1
                    elif chkmatrix[i][j] == 3:
                        element_box_count[8][2] += 1
                    elif chkmatrix[i][j] == 4:
                        element_box_count[8][3] += 1
                    elif chkmatrix[i][j] == 5:
                        element_box_count[8][4] += 1
                    elif chkmatrix[i][j] == 6:
                        element_box_count[8][5] += 1
                    elif chkmatrix[i][j] == 7:
                        element_box_count[8][6] += 1
                    elif chkmatrix[i][j] == 8:
                        element_box_count[8][7] += 1
                    elif chkmatrix[i][j] == 9:
                        element_box_count[8][8] += 1

        #check for element box count
        for i in range(count):
            for j in range(count):
                if element_box_count[i][j]  != 1:
                    notify = "Game Played Incorrectly!"
                    return render_template("lvl3.html", notify=notify, count=count, matrix=matrix)

        #if user has won level2
        notify = "Played Well!"
        sql = "update users set lvl3 = 'Yes' where username = '" + user["username"]+"'"
        db.execute(sql)
        connection.commit()
        notify = sql
        return redirect("/")

    else:
        notify = "Start Playing Level3!"
        return render_template("lvl3.html", matrix=matrix, notify=notify, count=count)


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    sql = "select lvl1,lvl2,lvl3 from users where id = " + str(session["user_id"])
    db.execute(sql)
    record = db.fetchall()
    user = record[0]

    #if user has played the levels before or not
    if user["lvl1"] == "Yes":
        lvl1 = "Play Again!"
    else:
        lvl1 = ""
    if user["lvl2"] == "Yes":
        lvl2 = "Play Again!"
    else:
        lvl2 = ""
    if user["lvl3"] == "Yes":
        lvl3 = "Play Again!"
    else:
        lvl3 = ""

    return render_template("index.html", lvl1=lvl1, lvl2=lvl2, lvl3=lvl3)


@app.route("/reset", methods=["GET"])
@login_required
def reset():
    sql = "select * from users where id = " + str(session["user_id"])
    db.execute(sql)
    record = db.fetchall()
    user = record[0]
    sql = "update users set lvl1 = 'No', lvl2 = 'No', lvl3 = 'No' where username = '" + user["username"] + "'"
    db.execute(sql)
    connection.commit()
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    #if method is get
    if request.method == "GET":
        return render_template("register.html")

    #if method is post
    if request.method == "POST":

        #if username is empty
        if not request.form.get("username"):
            notify = "Must Provide Username!"
            return render_template("register.html", notify=notify)

        #if username valid
        if not re.search("^[a-zA-Z_]+$", request.form.get("username")):
            notify = "Username Can Only Contain Letters and Underscore!"
            return render_template("register.html", notify=notify)

        #if username is not unique
        username = db.execute("select * from users where username = ?", [request.form.get("username").lower()])
        if username.fetchone():
            notify = "Must Provide Unique Username!"
            return render_template("register.html", notify=notify)

        #if phone number empty
        if not request.form.get("phone"):
            notify = "Must Provide Phone Number!"
            return render_template("register.html", notify=notify)

        #not a valid phone number
        if len(request.form.get("phone")) != 10 or not request.form.get("phone").isnumeric():
            notify = "Phone Number Not Valid! Please Re-enter The Details!"
            return render_template("register.html", notify=notify)

        #if password or confirmpassword  field not given
        if not request.form.get("password") or not request.form.get("confirmpassword"):
            notify = "Must Provide Both Passwords!"
            return render_template("register.html", notify=notify)

        #if length of both passwords do not match
        if not len(request.form.get("password")) == len(request.form.get("confirmpassword")):
            notify = "Both Passwords Must Match!"
            return render_template("register.html", notify=notify)

        #if password less than 5 characters
        if not len(request.form.get("password")) > 5:
            notify = "Password Must Be More Than 5 Characters"
            return render_template("register.html", notify=notify)

        #if passwords do not match
        if not request.form.get("password") == request.form.get("confirmpassword"):
            notify = "Both Passwords Must Match!"
            return render_template("register.html", notify=notify)

        #if all goes right
        db.execute("insert into users(username,hash,phone) values(?,?,?)", (
                  request.form.get("username").lower(), generate_password_hash(
                  request.form.get("password")), request.form.get("phone")))
        connection.commit()
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            notify = "Must Provide Username!"
            return render_template("login.html", notify=notify)

        # Ensure password was submitted
        elif not request.form.get("password"):
            notify = "Must Provide Password!"
            return render_template("login.html", notify=notify)

        # Ensure username exists
        db.execute("select * from users where username = ?", [request.form.get("username").lower()])

        #if username does not exist
        records = db.fetchall()
        row = records[0]
        if not row["username"]:
            notify = "Invalid Username or Password!"
            return render_template("login.html", notify=notify)

        #if password is wrong
        if not check_password_hash(row["hash"], request.form.get("password")):
            notify = "Invalid Username or Password"
            return render_template("login.html", notify=notify)

        # Remember which user has logged in
        session["user_id"] = row["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/rules", methods = ["POST", "GET"])
@login_required
def rules():
    if request.method == "GET":
        return render_template("rules.html")
    else:
        return redirect("/")