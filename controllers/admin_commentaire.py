#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_commentaire = Blueprint('admin_commentaire', __name__,
                              template_folder='templates')


@admin_commentaire.route('/admin/article/commentaires', methods=['GET'])
def admin_article_details():
    mycursor = get_db().cursor()
    code_ski = request.args.get('code_ski', None)
    sql = '''    SELECT * FROM commentaire
                INNER JOIN skis ON skis.code_ski = commentaire.Id_skis
                INNER JOIN utilisateur ON commentaire.Id_utilisateur = utilisateur.id_utilisateur
                WHERE commentaire.Id_skis = {}
                ORDER BY commentaire.date_publication'''.format(code_ski)
    mycursor.execute(sql)
    commentaires = mycursor.fetchall()
    sql = '''   SELECT * FROM skis WHERE code_ski = {}'''.format(code_ski)
    mycursor.execute(sql)
    skis = mycursor.fetchone()
    return render_template('admin/article/show_article_commentaires.html'
                           , commentaires=commentaires
                           , skis=skis
                           )


@admin_commentaire.route('/admin/article/commentaires/delete', methods=['POST'])
def admin_comment_delete():
    mycursor = get_db().cursor()
    id_utilisateur = request.form.get('id_utilisateur', None)
    code_ski = request.form.get('code_ski', None)
    date_publication = request.form.get('date_publication', None)
    sql = '''DELETE FROM commentaire WHERE Id_utilisateur = %s AND Id_skis = %s AND date_publication = %s'''
    tuple_delete = (id_utilisateur, code_ski, date_publication)
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    return redirect('/admin/article/commentaires?code_ski=' + code_ski)


@admin_commentaire.route('/admin/article/commentaires/repondre', methods=['POST', 'GET'])
def admin_comment_add():
    if request.method == 'GET':
        id_utilisateur = request.args.get('id_utilisateur', None)
        code_ski = request.args.get('code_ski', None)
        date_publication = request.args.get('date_publication', None)
        return render_template('admin/article/add_commentaire.html', id_utilisateur=id_utilisateur, code_ski=code_ski,
                               date_publication=date_publication)

    mycursor = get_db().cursor()
    id_utilisateur = session['id_user']  # 1 admin
    code_ski = request.form.get('code_ski', None)
    print('XXXXXXXXXXXXXXXXXXXX', code_ski)
    date_publication = request.form.get('date_publication', None)
    commentaire = request.form.get('commentaire', None)
    sql = '''    INSERT INTO commentaire (Id_utilisateur, Id_skis, date_publication, commentaire, valider) 
    VALUES (%s, %s, NOW(), %s, 1) '''
    tuple_answer = (id_utilisateur, code_ski, commentaire)
    mycursor.execute(sql, tuple_answer)
    get_db().commit()
    return redirect('/admin/article/commentaires?code_ski=' + code_ski)


@admin_commentaire.route('/admin/article/commentaires/valider', methods=['POST', 'GET'])
def admin_comment_valider():
    code_ski = request.args.get('code_ski', None)
    mycursor = get_db().cursor()
    sql = '''   UPDATE commentaire SET valider = 1 WHERE Id_skis = %s'''
    mycursor.execute(sql, (code_ski,))
    get_db().commit()
    return redirect('/admin/article/commentaires?code_ski=' + code_ski)
