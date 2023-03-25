#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g

from connexion_db import get_db

from controllers.client_liste_envies import client_historique_add

client_commentaire = Blueprint('client_commentaire', __name__,
                               template_folder='templates')


@client_commentaire.route('/client/article/details', methods=['GET'])
def client_article_details():
    mycursor = get_db().cursor()
    code_ski = request.args.get('code_ski', None)
    print(code_ski)
    id_client = session['id_user']

    sql = '''SELECT libelle_skis, image_skis, prix_skis, description , code_ski
          FROM skis 
          WHERE code_ski = %s;
          '''
    mycursor.execute(sql, (code_ski,))
    skis = mycursor.fetchone()
#AND commentaire.valider = 1
    sql = '''
    SELECT commentaire.Id_utilisateur ,commentaire.commentaire, commentaire.nom, commentaire.date_publication
    FROM commentaire
    INNER JOIN skis ON skis.code_ski = commentaire.Id_skis
    INNER JOIN utilisateur ON commentaire.Id_utilisateur = utilisateur.id_utilisateur
    WHERE skis.code_ski = %s AND commentaire.valider = 1;
    '''
    mycursor.execute(sql, (code_ski,))
    commentaire = mycursor.fetchall()

    sql = '''
        SELECT COUNT(*) as nb_commandes_article
        FROM skis
        INNER JOIN ligne_commande ON skis.code_ski = ligne_commande.code_ski
        INNER JOIN commande ON ligne_commande.id_commande = commande.id_commande
        INNER JOIN utilisateur ON commande.Id_utilisateur = utilisateur.id_utilisateur
        WHERE skis.code_ski = %s AND commande.id_utilisateur = %s;
    '''
    mycursor.execute(sql, (code_ski, id_client,))
    commandes_articles = mycursor.fetchone()

    sql = '''
    SELECT (SUM(note.note)/COUNT(note.note)) AS moy_notes, COUNT(note.note) AS nb_notes
    FROM note 
    INNER JOIN skis ON skis.code_ski = note.Id_skis
    WHERE skis.code_ski = %s;
    '''
    mycursor.execute(sql, (code_ski,))
    note = mycursor.fetchone()
    print('note', note)

    sql = "SELECT note FROM note WHERE Id_skis = %s AND Id_utilisateur = %s;"
    mycursor.execute(sql, (code_ski, id_client,))
    note_user = mycursor.fetchone()
    print('note_user', note_user)

    sql = '''
    SELECT COUNT(commentaire.commentaire) AS nb_commentaires_total
    FROM commentaire
    INNER JOIN skis ON skis.code_ski = commentaire.Id_skis
    WHERE skis.code_ski = %s
    ORDER BY commentaire.commentaire DESC;
    '''
    mycursor.execute(sql, (code_ski,))
    nb_commentaire = mycursor.fetchone()

    sql = '''
    SELECT COUNT(commentaire.commentaire) AS nb_commentaires_user
    FROM commentaire
    INNER JOIN skis ON skis.code_ski = commentaire.Id_skis
    WHERE commentaire.Id_utilisateur = %s AND skis.code_ski = %s
    ORDER BY commentaire.commentaire DESC;
    '''
    mycursor.execute(sql, (id_client, code_ski,))
    nb_commentaires_user = mycursor.fetchone()

    return render_template('client/article_info/article_details.html'
                           , skis=skis
                           , commentaire=commentaire
                           , commandes_articles=commandes_articles
                           , note=note
                           , note_user=note_user
                           , nb_commentaire=nb_commentaire
                           , nb_commentaires_user=nb_commentaires_user
                           )


@client_commentaire.route('/client/commentaire/add', methods=['POST'])
def client_comment_add():
    mycursor = get_db().cursor()
    commentaire = request.form.get('commentaire', None)
    print(commentaire)
    id_client = session['id_user']
    code_ski = request.form.get('code_ski', None)
    nom = session['login']
    print(nom)

    if commentaire == '':
        flash(u'Commentaire non prise en compte')
        return redirect('/client/article/details?id_article=' + code_ski)
    if commentaire != None and len(commentaire) > 0 and len(commentaire) < 3:
        flash(u'Commentaires en plus de 2 caractères', 'alert-warning')
        return redirect('/client/article/details?code_ski=' + code_ski)

    tuple_insert = (nom, id_client, code_ski, commentaire)
    print(tuple_insert)

    sql = '''INSERT INTO commentaire(nom, Id_utilisateur, Id_skis, commentaire, date_publication) 
         VALUES (%s,%s,%s,%s, NOW());'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?code_ski=' + code_ski)


@client_commentaire.route('/client/commentaire/delete', methods=['POST'])
def client_comment_delete():
    mycursor = get_db().cursor()
    id_skis_com = request.form.get('Id_skis', None)
    id_client = session['id_user']
    date_publication = request.form.get('date_publication', None)
    sql = '''DELETE FROM commentaire 
             WHERE commentaire.Id_skis = %s 
             AND commentaire.Id_utilisateur = %s AND commentaire.date_publication = %s;'''
    tuple_delete = (id_skis_com, id_client, date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?code_ski=' + id_skis_com)

@client_commentaire.route('/client/note/add', methods=['POST'])
def client_note_add():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    note = request.form.get('note', None)
    id_skis_note = request.form.get('code_ski', None)
    tuple_insert = (note, id_client, id_skis_note)
    print(tuple_insert)
    sql = '''INSERT INTO note(note, Id_utilisateur, Id_skis) VALUES (%s,%s,%s);'''
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    return redirect('/client/article/details?code_ski=' + id_skis_note)


@client_commentaire.route('/client/note/edit', methods=['POST'])
def client_note_edit():
    mycursor = get_db().cursor()
    note = request.form.get('note', None)
    id_client = session['id_user']
    id_ski_edit = request.form.get('code_ski', None)
    tuple_update = (note, id_client, id_ski_edit)
    print(tuple_update)
    sql = '''UPDATE note SET note = %s WHERE note.Id_utilisateur = %s AND note.Id_skis = %s;  '''
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    return redirect('/client/article/details?code_ski=' + id_ski_edit)


@client_commentaire.route('/client/note/delete', methods=['POST'])
def client_note_delete():
    mycursor = get_db().cursor()
    id_client = session['id_user']
    id_article = request.form.get('code_ski', None)
    tuple_delete = (id_client, id_article)
    print(tuple_delete)
    sql = '''DELETE FROM note WHERE note.Id_utilisateur =%s AND note.Id_skis = %s; '''
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/client/article/details?code_ski=' + id_article)
