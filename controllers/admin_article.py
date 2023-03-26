#! /usr/bin/python
# -*- coding:utf-8 -*-
import math
import os.path
from random import random

from flask import Blueprint
from flask import request, render_template, redirect, flash
# from werkzeug.utils import secure_filename

from connexion_db import get_db

admin_article = Blueprint('admin_article', __name__,
                          template_folder='templates')


@admin_article.route('/admin/article/show')
def show_article():
    mycursor = get_db().cursor()

    sql = '''
    SELECT skis.libelle_skis,skis.code_ski,skis.type_skis_id,type_skis.libelle_ski,
          skis.prix_skis,SUM(declinaison.stock) AS stock,
          COUNT(declinaison.id_declinaison) AS nb_declinaisons,
          skis.image_skis,
          (SELECT COUNT(commentaire.commentaire) FROM commentaire
          WHERE Id_skis = skis.code_ski AND valider = 0) AS nb_commentaires_nouveaux
           FROM declinaison
          INNER JOIN skis ON declinaison.code_ski=skis.code_ski
          INNER JOIN type_skis ON skis.type_skis_id=type_skis.id_type_skis
          LEFT JOIN commentaire ON skis.code_ski = commentaire.Id_skis AND commentaire.valider = 1
          GROUP BY skis.code_ski;
          '''
    mycursor.execute(sql)
    skis = mycursor.fetchall()
    sql = ''' 
SELECT skis.libelle_skis,skis.code_ski,
skis.type_skis_id,type_skis.libelle_ski,skis.prix_skis,skis.image_skis,
(SELECT COUNT(commentaire.commentaire) FROM commentaire 
WHERE Id_skis = skis.code_ski AND valider = 0) AS nb_commentaires_nouveaux
FROM skis
INNER JOIN type_skis ON skis.type_skis_id=type_skis.id_type_skis
WHERE skis.code_ski NOT IN (
SELECT code_ski
FROM declinaison);
'''
    mycursor.execute(sql)
    skis_sans_decl = mycursor.fetchall()
    return render_template('admin/article/show_article.html', skis=skis, skis_sans_decl=skis_sans_decl)


@admin_article.route('/admin/article/add', methods=['GET'])
def add_article():
    mycursor = get_db().cursor()
    mycursor_bis = get_db().cursor()
    sql = "SELECT * from skis;"
    sql_bis = "SELECT * FROM type_skis;"
    mycursor.execute(sql)
    mycursor_bis.execute(sql_bis)
    skis = mycursor.fetchall()
    type_skis = mycursor_bis.fetchall()
    return render_template('admin/article/add_article.html', skis=skis, type_skis=type_skis)


@admin_article.route('/admin/article/add', methods=['POST'])
def valid_add_article():
    mycursor = get_db().cursor()
    libelle_skis = request.form.get('libelle_skis', '')
    prix_skis = request.form.get('prix_skis', '')
    type_skis_id = request.form.get('type_skis_id', '')
    image_skis = request.form.get('image_skis', '')
    tuple_insert = (libelle_skis, prix_skis, type_skis_id, image_skis)
    sql = "INSERT INTO skis (libelle_skis, prix_skis, type_skis_id, image_skis) VALUES (%s, %s, %s, %s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'Ski ajouté, Nom : ', libelle_skis, ' | Prix :', prix_skis, ' | ID Type de ski :', type_skis_id,
          ' | Image : ', image_skis)
    message = u'Ski ajouté, Nom : ' + libelle_skis + ' | Prix : ' + prix_skis + ' | ID Type de ski : ' + type_skis_id + ' | Image : ' \
              + image_skis
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/delete', methods=['GET'])
def delete_article():
    mycursor = get_db().cursor()
    mycursor_2 = get_db().cursor()
    mycursor_3 = get_db().cursor()
    mycursor_4 = get_db().cursor()
    code_ski = request.args.get('code_ski', '')
    tuple_delete = (code_ski,)
    sql = "DELETE FROM ligne_panier WHERE code_ski =%s;"
    sql_2 = "DELETE FROM ligne_commande WHERE code_ski = %s;"
    sql_3 = "DELETE FROM declinaison WHERE code_ski =%s;"
    sql_4 = "DELETE FROM skis WHERE code_ski =%s;"
    mycursor.execute(sql, tuple_delete)
    mycursor_2.execute(sql_2, tuple_delete)
    mycursor_3.execute(sql_3, tuple_delete)
    mycursor_4.execute(sql_4, tuple_delete)

    get_db().commit()
    print(u'Ski Supprimé , ID : ', code_ski)
    message = u'Ski Supprimé, ID : ' + code_ski
    flash(message, 'alert-warning')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/edit', methods=['GET'])
def edit_article():
    mycursor = get_db().cursor()
    mycursor_bis = get_db().cursor()
    mycursor_3 = get_db().cursor()
    code_ski = request.args.get('code_ski', '')
    decl = request.args.get('decl', None)

    if decl is None:
        sql = "SELECT *,SUM(dl.stock) AS total_stock from skis sk INNER JOIN declinaison dl ON dl.code_ski=sk.code_ski where sk.code_ski=%s GROUP BY dl.code_ski;"
    else:
        sql = "SELECT * FROM skis WHERE skis.code_ski=%s"

    sql_bis = "SELECT * FROM type_skis;"
    mycursor.execute(sql, code_ski)
    skis = mycursor.fetchone()
    mycursor_bis.execute(sql_bis)

    type_skis = mycursor_bis.fetchall()
    sql = ''' 
    SELECT c.nom_couleur,dl.stock,dl.code_ski,dl.id_declinaison AS id_declinaison_skis
    FROM declinaison dl 
    INNER JOIN couleur c ON c.n_couleur=dl.id_couleur 
    WHERE dl.code_ski=%s '''
    mycursor.execute(sql, (code_ski,))
    declinaison = mycursor.fetchall()
    return render_template('admin/article/edit_article.html', skis=skis, type_skis=type_skis, declinaison=declinaison,
                           decl=decl)


@admin_article.route('/admin/article/edit', methods=['POST'])
def valid_edit_article():
    mycursor = get_db().cursor()
    mycursor_2 = get_db().cursor()
    libelle_skis = request.form.get('libelle_skis', '')
    prix_skis = request.form.get('prix_skis', '')
    type_skis_id = request.form.get('type_skis_id', '')
    image_skis = request.form.get('image_skis', '')
    code_ski = request.form.get('code_ski', '')
    stock = request.form.get('stock', '')
    tuple_update = (libelle_skis, prix_skis, type_skis_id, image_skis, code_ski)
    print(image_skis)
    sql = "UPDATE skis SET libelle_skis=%s, prix_skis=%s, type_skis_id=%s, image_skis=%s WHERE code_ski=%s;"

    mycursor.execute(sql, tuple_update)
    get_db().commit()
    # sql = "UPDATE declinaison SET stock=%s WHERE code_ski=%s;"
    # tuple_update = (stock, code_ski)
    # mycursor.execute(sql, tuple_update)
    # get_db().commit()
    print(u'Ski modifié, Nom : ', libelle_skis, ' | Prix :', prix_skis, ' | ID Type de ski :', type_skis_id,
          ' | Image : ', image_skis, ' | Stock : ', stock)
    message = u'Ski modifié, Nom : ' + libelle_skis + ' | Prix : ' + prix_skis + ' | ID Type de ski : ' + type_skis_id + ' | Image : ' \
              + image_skis
    flash(message, 'alert-success')
    return redirect('/admin/article/show')


@admin_article.route('/admin/article/avis/<int:id>', methods=['GET'])
def admin_avis(id):
    mycursor = get_db().cursor()
    sql = ''' SELECT *, type_skis.libelle_skis, couleur.nom_couleur 
    FROM skis
    INNER JOIN type_skis ON type_skis.id_type_skis=skis.type_skis_id
    WHERE skis.code_ski=%s'''
    mycursor.execute(sql, (id,))
    skis = mycursor.fetchone()

    sql = '''
    SELECT * FROM avis WHERE code_ski=%s;
    '''
    mycursor.execute(sql, (id,))
    commentaires = mycursor.fetchall()
    return render_template('admin/article/show_avis.html'
                           , skis=skis
                           , commentaires=commentaires
                           )


@admin_article.route('/admin/comment/delete', methods=['POST'])
def admin_avis_delete():
    mycursor = get_db().cursor()
    article_id = request.form.get('idArticle', None)
    userId = request.form.get('idUser', None)

    return admin_avis(article_id)
