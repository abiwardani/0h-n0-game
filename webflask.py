import os
from flask import Flask, render_template, flash, request, url_for, redirect
from werkzeug.utils import secure_filename
import Oh_nO as on

UPLOAD_FOLDER = '/uploadFiles'
ALLOWED_EXTENSIONS = {'txt','pdf'}
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['TEMPLATES_AUTO_RELOAD'] = True

game = 0
board = [[]]
n = 0
win = False

@app.route('/', methods = ['GET', 'POST'])
def mainPage():
    if request.method == "POST":
        n = request.form.get("size")
    
    return render_template('mainpage.html')

@app.route('/Start', methods = ['GET', 'POST'])
def startGame():
    if request.method == "POST":
        global game
        global board
        global n
        global win
        win = False
        n = int(request.form.get("size"))
        game = on.Game(n)
        board = [[game.Puzzle[i][j] for j in range(1,n+1)] for i in range(1,n+1)]
    
    return playPage()
    
@app.route('/Incr/<nstr>')
def increment(nstr):
    (i, j) = nstr.split("_")
    i = int(i)
    j = int(j)
    global board
    if board[i][j] == None:
        board[i][j] = 1
    elif board[i][j] == "X":
        board[i][j] = None
    else:
        board[i][j] = "X"
    return playPage()

@app.route('/Check/', methods = ['GET', 'POST'])
def checkPage():
    global board
    global game
    global win
    
    win = True
    
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == "X":
                win = win and (game.Board[i+1][j+1] == "X")
            elif board[i][j] != None:
                win = win and (game.Board[i+1][j+1] != "X")
            else:
                win = False
            if win == False:
                return playPage()
    
    return playPage()
        
    
@app.route('/Play', methods = ['GET', 'POST'])
def playPage():
    global board
    global game
    global n
    global win
    
    html = "<!DOCTYPE html>"
    html += "<html>\n"
    html += "   <head>\n"
    html += "       <title>Oh_nO!</title>\n"
    html += "       <style>\n"
    html += "           .board table { border: 1px solid black; }\n"
    html += "           .board tr, td { border: 1px solid black; height: 60px; }\n"
    html += "       </style>\n"
    html += "   </head>\n"
    html += "   <body>\n"
    html += "       <a style=\"text-decoration: none\" href=\"http://127.0.0.1:5000\"><h2>Oh_nO!<span class=\"Searchy\">NxN</span></h2></a>\n"
    html += "       <form action=\"http://127.0.0.1:5000/Start\" method=POST>\n"
    html += "           <div class=\"searchbar\">\n"
    html += "               <label>Board size: </label>\n"
    html += "               <input type=\"text\" name=\"size\" id=\"size\" placeholder=\"Input Length\">\n"
    html += "               <input type=\"submit\" name=\"playButton\" value=\"Play\">\n"
    html += "           </div>\n"
    html += "       </form>\n"
    html += "       <form action=\"http://127.0.0.1:5000/Check\" method=POST>\n"
    html += "           <div class=\"check\">\n"
    if win:
        html += "               <label>Correct!</label>\n"
    html += "               <input type=\"submit\" name=\"checkButton\" value=\"Check\">\n"
    html += "           </div>\n"
    html += "       </form>\n"
    
    html += "       <div class=\"board\">\n"
    html += "           <table style=\"width:"+str(n*60)+"px;\">\n"
    for i in range(n):
        html += "               <tr>\n"
        for j in range(n):
            html += "               <th width=60px"
            if board[i][j] == None:
                html += " style=\"background-color:white; color:white;\""
            elif board[i][j] == "X":
                html += " style=\"background-color:red; color:red;\""
            else:
                html += " style=\"background-color:blue; color:white;\""
                
            if win:
                html += ">"+str(game.Board[i+1][j+1])
            else:
                if game.Puzzle[i+1][j+1] == None:
                    html += " onclick=\"window.location=\'http://127.0.0.1:5000/Incr/"+str(i)+"_"+str(j)+"\'\">"
                    html += "<a style=\"color:LightGray;\" href=\"http://127.0.0.1:5000/Incr/"+str(i)+"_"+str(j)+"\">X</a>"
                else:
                    if board[i][j] != "X":
                        html += ">"+str(board[i][j])
                    else:
                        html += ">X"
            
            html += "</th>\n"
            
        html += "               </tr>\n"
    
    html += "           </table>\n"
    html += "       </div>\n"
    html += "   </body>\n"
    html += "</html>"
    
    with open("templates/play.html", "w", encoding="utf8") as file:
        file.write(html)
    
    return html #render_template('play.html')


if __name__ == '__main__':
    app.run()
