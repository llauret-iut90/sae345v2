#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint, url_for
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

app = Flask(__name__)
app.secret_key = 'une cle(token) : grain de sel(any random string) je sais pas quoi mettre'

client_article = Blueprint('client_article', __name__,
                           template_folder='templates')


# @client_article.route('/client/index')
# def client_index():
#     return redirect(url_for('client_article_show'))


@client_article.route('/client/article/show')
def client_article_show():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    print("id_client =", id_client)

    # Affichage des cartes
    sql3 = ''' SELECT DISTINCT skis.code_ski, skis.image_skis, skis.libelle_skis, skis.prix_skis,skis.type_skis_id,
                COUNT(d.code_ski) AS nb_declinaison,SUM(d.stock) AS stock
FROM skis
INNER JOIN declinaison d on skis.code_ski = d.code_ski
GROUP BY skis.code_ski, skis.image_skis, skis.libelle_skis, skis.prix_skis,skis.type_skis_id; '''
    mycursor.execute(sql3)
    skis0 = mycursor.fetchall()

    # pour le filtre
    sql = "SELECT * FROM type_skis"
    mycursor.execute(sql)
    types_skis = mycursor.fetchall()

    # pour le panier
    sql = ''' 
SELECT skis.libelle_skis AS nom, skis.prix_skis AS prix, ligne_panier.quantite_ligne_panier AS quantite,
ROUND((skis.prix_skis * ligne_panier.quantite_ligne_panier),2) AS sous_total, declinaison.stock,
skis.code_ski, ligne_panier.n_declinaison AS id_declinaison_article,cl.nom_couleur AS libelle_couleur,
declinaison.id_couleur
FROM ligne_panier
INNER JOIN skis ON ligne_panier.code_ski = skis.code_ski
INNER JOIN declinaison ON ligne_panier.n_declinaison = declinaison.id_declinaison
INNER JOIN couleur cl ON cl.n_couleur=declinaison.id_couleur
WHERE utilisateur_id=%s;
    '''
    mycursor.execute(sql, (id_client,))
    skis_panier = mycursor.fetchall()

    if len(skis_panier) >= 1:
        prix_total = 0
        for panier in skis_panier:
            prix_total = prix_total + panier['sous_total']
    else:
        prix_total = None
    return render_template('client/boutique/panier_article.html',skis=skis0, skis_panier=skis_panier,items_filtre=types_skis,
                            prix_total=prix_total)
