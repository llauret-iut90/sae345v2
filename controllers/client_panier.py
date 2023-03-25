#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import request, render_template, redirect, abort, flash, session
from datetime import datetime

from connexion_db import get_db

client_panier = Blueprint('client_panier', __name__,
                          template_folder='templates')


@client_panier.route('/client/panier/add', methods=['POST'])
def client_panier_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_skis = request.form.get('code_ski')
    quantite = request.form.get('quantite')
    date_ajout = datetime.now().strftime('%Y-%m-%d')
    # ---------
    # id_declinaison_article = 1
    # ajout dans le panier d'une déclinaison d'un article (si 1 declinaison : immédiat sinon => vu pour faire un choix
    sql = '''
    SELECT dl.id_declinaison,dl.stock,dl.id_couleur,sk.code_ski AS id_skis, cl.nom_couleur
FROM declinaison dl
INNER JOIN couleur cl ON dl.id_couleur=cl.n_couleur
INNER JOIN skis sk ON dl.code_ski=sk.code_ski
WHERE sk.code_ski = %s;
    '''
    mycursor.execute(sql, (id_skis,))
    declinaisons = mycursor.fetchall()

    if len(declinaisons) == 1:
        sql = ''' SELECT dl.id_declinaison FROM declinaison dl WHERE dl.code_ski=%s '''
        mycursor.execute(sql, (id_skis,))
        id_declinaison = mycursor.fetchone()
        id = id_declinaison['id_declinaison']
        sql = ''' SELECT * 
        FROM ligne_panier lp 
        WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
        mycursor.execute(sql, (id_client, id, id_skis,))
        verif_in_panier = mycursor.fetchall()

        if len(verif_in_panier) == 1:
            sql = ''' UPDATE ligne_panier lp 
            SET lp.quantite_ligne_panier=lp.quantite_ligne_panier+%s 
            WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
            mycursor.execute(sql, (quantite, id_client, id, id_skis,))
            sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock-%s WHERE id_declinaison=%s '''
            mycursor.execute(sql, (quantite, id,))
            get_db().commit()

        elif len(verif_in_panier) == 0:
            sql = ''' INSERT INTO ligne_panier(code_ski, utilisateur_id, quantite_ligne_panier, n_declinaison, date_ajout) VALUES (%s,%s,%s,%s,%s) '''
            mycursor.execute(sql, (id_skis, id_client, quantite, id, date_ajout,))
            sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock-%s WHERE id_declinaison=%s '''
            mycursor.execute(sql, (quantite, id,))
            get_db().commit()

        else:
            abort("probleme verif_in_panier resultat pas unique")
        # id_declinaison_article = declinaisons[0]['id_declinaison_article']

    elif len(declinaisons) == 0:
        abort("pb nb de declinaison")

    else:
        sql = ''' SELECT dl.id_declinaison,dl.stock,dl.id_couleur,dl.code_ski,sk.libelle_skis,sk.prix_skis,sk.image_skis
        FROM declinaison dl
        INNER JOIN skis sk ON sk.code_ski=dl.code_ski 
        WHERE dl.code_ski = %s  '''
        mycursor.execute(sql, (id_skis,))
        skis = mycursor.fetchone()
        return render_template('client/boutique/declinaison_article.html'
                               , declinaisons=declinaisons
                               , quantite=quantite
                               , skis=skis)

    # ajout dans le panier d'un article

    return redirect('/client/article/show')


@client_panier.route('/client/panier/add/decl', methods=['POST'])
def client_panier_add_decl():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_skis = request.form.get('code_ski')
    quantite = request.form.get('quantite')
    id_declinaison_article = request.form.get('id_declinaison_article', None)
    date_ajout = datetime.now().strftime('%Y-%m-%d')

    sql = "SELECT dl.id_declinaison,dl.stock,dl.id_couleur,cl.n_couleur,sk.code_ski AS id_skis, cl.nom_couleur " \
          "FROM declinaison dl " \
          "INNER JOIN couleur cl ON dl.id_couleur=cl.n_couleur " \
          "INNER JOIN skis sk ON dl.code_ski=sk.code_ski " \
          "WHERE sk.code_ski = %s AND dl.id_declinaison=%s;"
    mycursor.execute(sql, (id_skis, id_declinaison_article,))
    declinaisons = mycursor.fetchall()

    if len(declinaisons) == 1:
        sql = ''' SELECT * 
               FROM ligne_panier lp 
               WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
        mycursor.execute(sql, (id_client, id_declinaison_article, id_skis,))
        verif_in_panier = mycursor.fetchall()

        if len(verif_in_panier) == 1:
            sql = ''' UPDATE ligne_panier lp 
                   SET lp.quantite_ligne_panier=lp.quantite_ligne_panier+%s 
                   WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
            mycursor.execute(sql, (quantite, id_client, id_declinaison_article, id_skis,))
            sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock-%s WHERE id_declinaison=%s '''
            mycursor.execute(sql, (quantite, id_declinaison_article,))
            get_db().commit()
        elif len(verif_in_panier) == 0:
            sql = ''' INSERT INTO ligne_panier(code_ski, utilisateur_id, quantite_ligne_panier, n_declinaison, date_ajout) VALUES (%s,%s,%s,%s,%s) '''
            mycursor.execute(sql, (id_skis, id_client, quantite, id_declinaison_article, date_ajout,))
            sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock-%s WHERE id_declinaison=%s '''
            mycursor.execute(sql, (quantite, id_declinaison_article,))
            get_db().commit()
        else:
            abort("probleme verif_in_panier resultat pas unique")

    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete', methods=['POST'])
def client_panier_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_skis = request.form.get('code_ski')
    quantite = request.form.get('quantite')
    quantite_ligne_panier = request.form.get('quantite_ligne_panier')
    id_declinaison_article = request.form.get('id_declinaison_article')
    # ---------
    # partie 2 : on supprime une déclinaison de l'article

    sql = ''' SELECT * FROM ligne_panier lp WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
    mycursor.execute(sql, (id_client, id_declinaison_article, id_skis,))
    skis_panier = mycursor.fetchone()

    if not (skis_panier is None) and int(quantite_ligne_panier) > 1:
        sql = ''' UPDATE ligne_panier lp 
        SET lp.quantite_ligne_panier=lp.quantite_ligne_panier-%s 
        WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
        mycursor.execute(sql, (quantite, id_client, id_declinaison_article, id_skis,))
        sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock+%s WHERE id_declinaison=%s '''
        mycursor.execute(sql, (quantite, id_declinaison_article,))
        get_db().commit()
    else:
        sql = ''' DELETE FROM ligne_panier WHERE ligne_panier.utilisateur_id=%s AND ligne_panier.n_declinaison=%s AND ligne_panier.code_ski=%s '''
        mycursor.execute(sql, (id_client, id_declinaison_article, id_skis,))
        sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock+1 WHERE id_declinaison=%s '''
        mycursor.execute(sql, (id_declinaison_article,))
        get_db().commit()
    # mise à jour du stock de l'article disponible
    return redirect('/client/article/show')


@client_panier.route('/client/panier/vider', methods=['POST'])
def client_panier_vider():
    mycursor = get_db().cursor()
    client_id = session['id_user']
    sql = ''' SELECT * FROM ligne_panier lp WHERE lp.utilisateur_id=%s'''
    mycursor.execute(sql, (client_id,))
    skis_panier = mycursor.fetchall()
    for item in skis_panier:
        declinaison = item['n_declinaison']
        skis = item['code_ski']
        quantite = item['quantite_ligne_panier']
        sql = ''' DELETE FROM ligne_panier WHERE ligne_panier.utilisateur_id=%s AND ligne_panier.n_declinaison=%s AND ligne_panier.code_ski=%s '''
        mycursor.execute(sql, (client_id, declinaison, skis,))
        sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock+%s WHERE id_declinaison=%s '''
        mycursor.execute(sql, (quantite, declinaison,))
        get_db().commit()

        # sql2=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''
    return redirect('/client/article/show')


@client_panier.route('/client/panier/delete/line', methods=['POST'])
def client_panier_delete_line():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_declinaison_article = request.form.get('id_declinaison_article')
    id_skis = request.form.get('code_ski')

    sql = ''' SELECT * FROM ligne_panier lp WHERE lp.utilisateur_id=%s AND lp.n_declinaison=%s AND lp.code_ski=%s '''
    mycursor.execute(sql, (id_client, id_declinaison_article, id_skis,))
    declinaison = mycursor.fetchone()
    sql2 = ''' DELETE FROM ligne_panier WHERE ligne_panier.utilisateur_id=%s AND ligne_panier.n_declinaison=%s AND ligne_panier.code_ski=%s '''
    mycursor.execute(sql2, (id_client, id_declinaison_article, id_skis,))
    quantite = declinaison['quantite_ligne_panier']
    sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock+%s WHERE id_declinaison=%s '''
    mycursor.execute(sql, (quantite, id_declinaison_article,))
    get_db().commit()
    # sql3=''' mise à jour du stock de l'article : stock = stock + qté de la ligne pour l'article'''

    return redirect('/client/article/show')


@client_panier.route('/client/panier/filtre', methods=['POST'])
def client_panier_filtre():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    print("id_client =", id_client)

    filter_word = request.form.get('filter_word', None)
    filter_prix_min = request.form.get('filter_prix_min', None)
    filter_prix_max = request.form.get('filter_prix_max', None)
    filter_types = request.form.getlist('filter_types', None)

    # pour le filtre
    sql = "SELECT * FROM type_skis"
    mycursor.execute(sql)
    types_skis = mycursor.fetchall()

    # vérif que c'est bien écrit
    if filter_word and filter_word != "":
        message = u'Filtre sur le mot: ' + filter_word
        flash(message, 'alert-success')

    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                message = u'Filtre sur le prix avec un numérique entre : ' + filter_prix_min + " et " + filter_prix_max
                flash(message, 'alert-success')
            else:
                message = u'min < max'
                flash(message, 'alert-warning')
        else:
            message = u'min et max doivent être des numérique'
            flash(message, 'alert-warning')
    if filter_types and filter_types != []:
        message = u'Case à cocher selectionnées: '
        for case in filter_types:
            message += 'id: ' + case + ' '
        flash(message, 'alert-success')

    # mise en session
    if filter_word or filter_word == "":
        if len(filter_word) > 1:
            if filter_word.isalpha():
                session['filter_word'] = filter_word
            else:
                flash(u'Votre mot recherché doit uniquement être composé de lettres')
        else:
            if len(filter_word) == 1:
                flash(u'Votre mot recherché doit être composé de au moins 2 lettres')
            else:
                session.pop(filter_word, None)
    if filter_prix_min or filter_prix_max:
        if filter_prix_min.isdecimal() and filter_prix_max.isdecimal():
            if int(filter_prix_min) < int(filter_prix_max):
                session['filter_prix_min'] = filter_prix_min
                session['filter_prix_max'] = filter_prix_max
            else:
                flash(u'min < max')
        else:
            flash(u'min et max doivent être des numériques')
    print("filter_types:", filter_types)
    print("ss:", filter_word)
    if filter_types and filter_types != []:
        session['filter_types'] = []
        for number_type in filter_types:
            session['filter_types'].append(number_type)

    # # Ajouter une pause de 1 seconde pour permettre aux valeurs de session d'être enregistrées avant la redirection
    # time.sleep(1)
    skis_panier = []
    sqlTemp = "SELECT declinaison.id_declinaison, COUNT(declinaison.id_declinaison) AS nb_declinaison, SUM(declinaison.stock) AS stock,declinaison.id_couleur,declinaison.code_ski, skis.libelle_skis,skis.image_skis,skis.type_skis_id,skis.prix_skis FROM skis INNER JOIN declinaison ON declinaison.code_ski = skis.code_ski INNER JOIN type_skis ON type_skis.id_type_skis = skis.type_skis_id"
    list_param = []
    condition_and = ""

    if "filter_word" in session or "filter_prix_min" in session or "filter_prix_max" in session or "filter_types" in session:
        sqlTemp = sqlTemp + " WHERE "
    if "filter_word" in session:
        sqlTemp = sqlTemp + " skis.libelle_skis LIKE %s"
        recherche = "%" + session["filter_word"] + "%"
        list_param.append(recherche)
        condition_and = " AND "
    if "filter_prix_min" in session or "filter_prix_max" in session:
        sqlTemp = sqlTemp + condition_and + " skis.prix_skis BETWEEN %s AND %s "
        list_param.append(session["filter_prix_min"])
        list_param.append(session["filter_prix_max"])
        condition_and = " AND "
    if "filter_types" in session:
        sqlTemp = sqlTemp + condition_and + "("
        last_item = session['filter_types'][-1]
        for item in session['filter_types']:
            sqlTemp = sqlTemp + " type_skis_id = %s "
            if item != last_item:
                sqlTemp = sqlTemp + " or "
            list_param.append(item)
        sqlTemp = sqlTemp + ")"
    sqlTemp = sqlTemp + " GROUP BY skis.code_ski"

    tuple_sql = tuple(list_param)
    cursor_skis = get_db().cursor()
    print(sqlTemp)
    cursor_skis.execute(sqlTemp, tuple_sql)
    ski = cursor_skis.fetchall()
    # pour le panier
    sql = "SELECT skis.libelle_skis AS nom, skis.prix_skis AS prix, ligne_panier.quantite_ligne_panier AS quantite, ROUND((skis.prix_skis * ligne_panier.quantite_ligne_panier),2) AS sous_total, declinaison.stock, skis.code_ski, ligne_panier.n_declinaison AS id_declinaison_article FROM ligne_panier INNER JOIN skis ON ligne_panier.code_ski = skis.code_ski INNER JOIN declinaison ON skis.code_ski = declinaison.code_ski WHERE utilisateur_id=%s GROUP BY id_declinaison_article"
    mycursor.execute(sql, (id_client,))
    skis_panier = mycursor.fetchall()

    if len(skis_panier) >= 1:
        prix_total = 0
        for panier in skis_panier:
            prix_total = prix_total + panier['sous_total']
    else:
        prix_total = None

    return render_template('client/boutique/panier_article.html', skis=ski, items_filtre=types_skis,
                           skis_panier=skis_panier, prix_total=prix_total)


@client_panier.route('/client/panier/filtre/suppr', methods=['POST'])
def client_panier_filtre_suppr():
    # suppression  des variables en session
    session.pop('filter_word', None)
    session.pop('filter_prix_min', None)
    session.pop('filter_prix_max', None)
    session.pop('filter_types', None)

    print("suppr filtre")
    return redirect('/client/article/show')
