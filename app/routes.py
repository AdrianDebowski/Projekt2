from flask import Flask,Response,redirect,url_for,request,session,abort,render_template
from flask_login import LoginManager,UserMixin,login_required,login_user,logout_user
import sqlite3 as sql
from app import app

#-------------------------------------------------------------- config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'sekretny_klucz'
)
#-------------------------------------------------------------- 

#-------------------------------------------------------------- ustawienie flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
#-------------------------------------------------------------- 

#-------------------------------------------------------------- model uzytkownika
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
    
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name,self.password)
#-------------------------------------------------------------- 

#-------------------------------------------------------------- generacja uzytkownikow
users = [User(id) for id in range(1, 10)]
#-------------------------------------------------------------- 

#---------------------------------------------- index.html
@app.route("/")
@login_required #wymaga logowania
def main():
    return render_template('index.html')
#----------------------------------------------

#---------------------------------------------- omnie.html
@app.route("/about")
@login_required
def omnie():
    tytul = 'O mnie'
    return render_template('omnie.html', tytul=tytul)

#-------------------------------------------------------

#---------------------------------------------- informacja.html
@app.route("/info")
@login_required
def info():
    tytul = 'Pies domowy'
    return render_template('informacja.html', tytul=tytul)
#----------------------------------------------------------	

#-------------------------------------------------------------- formularz_logowania.html
@app.route("/login", methods=["GET", "POST"])
def login():
    tytul = 'Zaloguj się'
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            login_user(user)
            return redirect(url_for("main"))
        else:
            return abort(401)
    else:
        return render_template('formularz_logowania.html', tytul=tytul)
    
#-------------------------------------------------------------- 

#-------------------------------------------------------------- blad.html
@app.errorhandler(401)
def page_not_found(e):
    tytul="Coś poszło nie tak..."
    blad = "401"
    return render_template('blad.html', tytul=tytul, blad=blad)
#-------------------------------------------------------------- 


#-------------------------------------------------------------- logout.html
@app.route("/logout")
@login_required
def logout():
    logout_user()
    tytul="Wylogowanie"
    return render_template('logout.html', tytul=tytul)
#-------------------------------------------------------------- 

#-------------------------------------------------------------- przeladowanie uzytkownika
@login_manager.user_loader
def load_user(userid):
    return User(userid)
#-------------------------------------------------------------- 
	
if __name__ == "__main__":
    app.run()