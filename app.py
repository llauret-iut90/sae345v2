#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
from flask import Blueprint


from controllers.auth_security import *
from controllers.fixtures_load import *

from controllers.client_article import *
from controllers.client_panier import *
from controllers.client_commande import *
from controllers.client_commentaire import *
from controllers.client_coordonnee import *

from controllers.admin_article import *
from controllers.admin_declinaison_article import *
from controllers.admin_commande import *
from controllers.admin_type_article import *
from controllers.admin_dataviz import *
from controllers.admin_commentaire import *
from controllers.client_liste_envies import *

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string)'


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def show_accueil():
    return render_template('auth/layout.html')

##################
# Authentification
##################

# Middleware de sécurité

@app.before_request
def before_request():
     if request.path.startswith('/admin') or request.path.startswith('/client'):
        if 'role' not in session:
            return redirect('/login')
        else:
            if (request.path.startswith('/client') and session['role'] != 'ROLE_client') or (request.path.startswith('/admin') and session['role'] != 'ROLE_admin'):
                print('pb de route : ', session['role'], request.path.title(), ' => deconnexion')
                session.pop('login', None)
                session.pop('role', None)
                return redirect('/login')
     # if session['role'] == 'ROLE_client':
     #    if not request.path.startswith('/client'):
     #        return redirect('/client/article/show')
     # if session['role'] == 'ROLE_admin':
     #    if not request.path.startswith('/admin'):
     #        return redirect('/admin')



app.register_blueprint(auth_security)
app.register_blueprint(fixtures_load)

app.register_blueprint(client_article)
app.register_blueprint(client_commande)
app.register_blueprint(client_commentaire)
app.register_blueprint(client_panier)
app.register_blueprint(client_coordonnee)
app.register_blueprint(client_liste_envies)

app.register_blueprint(admin_article)
app.register_blueprint(admin_declinaison_article)
app.register_blueprint(admin_commande)
app.register_blueprint(admin_type_article)
app.register_blueprint(admin_dataviz)
app.register_blueprint(admin_commentaire)


if __name__ == '__main__':
    app.run()
