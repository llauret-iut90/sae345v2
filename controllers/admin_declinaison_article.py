#! /usr/bin/python
# -*- coding:utf-8 -*-

from flask import Blueprint
from flask import request, render_template, redirect, flash
from connexion_db import get_db

admin_declinaison_article = Blueprint('admin_declinaison_article', __name__,
                         template_folder='templates')


@admin_declinaison_article.route('/admin/declinaison_article/add')
def add_declinaison_article():
    id_skis=request.args.get('code_ski')
    id_type_skis=request.args.get('id_type_skis')
    mycursor = get_db().cursor()
    decl = request.args.get('decl', '')
    sql= ''' SELECT * FROM skis WHERE code_ski=%s '''
    mycursor.execute(sql, (id_skis,))
    skis = mycursor.fetchone()
    sql = ''' SELECT * FROM couleur '''
    mycursor.execute(sql)
    couleurs=mycursor.fetchall()
    return render_template('admin/article/add_declinaison_article.html'
                           , skis=skis
                           , couleurs=couleurs, decl=decl, type_skis=id_type_skis
                           )


@admin_declinaison_article.route('/admin/declinaison_article/add', methods=['POST'])
def valid_add_declinaison_article():
    mycursor = get_db().cursor()
    id_skis = request.form.get('code_ski')
    stock = request.form.get('stock')
    couleur = request.form.get('couleur')
    type_skis = request.form.get('type_skis')
    sql = ''' SELECT id_couleur FROM declinaison WHERE code_ski=%s '''
    mycursor.execute(sql, (id_skis,))
    declinaison = mycursor.fetchall()
    here = None

    if len(declinaison) != 0:
        for dl in declinaison:
            if dl['id_couleur'] == int(couleur):
                here = 1

        if here is not None:
            sql = ''' UPDATE declinaison dl SET dl.stock=dl.stock+%s WHERE dl.id_couleur=%s AND dl.code_ski=%s '''
            mycursor.execute(sql, (stock,couleur,id_skis,))
            print(100)
        else:
            sql = ''' INSERT INTO declinaison(stock,id_couleur,code_ski) VALUES (%s,%s,%s) '''
            mycursor.execute(sql, (stock, couleur, id_skis,))
            print(200)

    else:
        sql = ''' INSERT INTO declinaison(stock,id_couleur,code_ski) VALUES (%s,%s,%s) '''
        mycursor.execute(sql, (stock,couleur,id_skis,))
        print(300)

    # attention au doublon
    get_db().commit()
    return redirect('/admin/article/edit?code_ski='+id_skis+'&amp;id_type_skis='+type_skis)



@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['GET'])
def edit_declinaison_article():
    id_declinaison = request.args.get('id_declinaison_skis')
    mycursor = get_db().cursor()
    sql = ''' SELECT sk.libelle_skis AS nom,sk.image_skis,dl.stock,cl.n_couleur,cl.nom_couleur, dl.code_ski, dl.id_declinaison
    FROM declinaison dl
    INNER JOIN skis sk ON sk.code_ski = dl.code_ski
    INNER JOIN couleur cl ON cl.n_couleur = dl.id_couleur
    WHERE dl.id_declinaison=%s '''
    mycursor.execute(sql, (id_declinaison, ))
    declinaison_skis = mycursor.fetchone()
    sql = ''' SELECT * FROM couleur '''
    mycursor.execute(sql)
    couleurs = mycursor.fetchall()
    return render_template('admin/article/edit_declinaison_article.html'
                           , couleurs=couleurs
                           , declinaison_article=declinaison_skis
                           )


@admin_declinaison_article.route('/admin/declinaison_article/edit', methods=['POST'])
def valid_edit_declinaison_article():
    id_declinaison_skis = request.form.get('id_declinaison_skis')
    id_skis = request.form.get('code_ski')
    stock = request.form.get('stock')
    couleur_id = request.form.get('id_couleur')
    mycursor = get_db().cursor()
    sql = ''' UPDATE declinaison dl SET dl.stock=%s,dl.id_couleur=%s WHERE dl.id_declinaison=%s  '''
    mycursor.execute(sql, (stock, couleur_id, id_declinaison_skis, ))
    get_db().commit()
    #print(stock+", "+couleur_id+", "+id_declinaison_skis)
    message = u'declinaison_article modifié , id:' + str(id_declinaison_skis) + '- stock :' + str(stock) + ' - couleur_id:' + str(couleur_id)
    flash(message, 'alert-success')
    return redirect('/admin/article/edit?code_ski='+id_skis)


@admin_declinaison_article.route('/admin/declinaison_article/delete', methods=['GET'])
def admin_delete_declinaison_article():
    id_declinaison_skis = request.args.get('id_declinaison_skis')
    id_skis = request.args.get('code_ski')
    mycursor = get_db().cursor()
    sql = ''' DELETE FROM declinaison WHERE declinaison.id_declinaison=%s '''
    mycursor.execute(sql, (id_declinaison_skis, ))
    get_db().commit()
    #print(id_declinaison_skis+", "+id_skis)
    sql =''' SELECT * FROM declinaison dl WHERE code_ski=%s '''
    mycursor.execute(sql, (id_skis, ))
    declinaison_skis = mycursor.fetchall()
    #print(len(declinaison_skis))
    flash(u'declinaison supprimée, id_declinaison_article : ' + str(id_declinaison_skis),  'alert-success')
    if len(declinaison_skis) == 0:
        return redirect('/admin/article/show')
    else:
        return redirect('/admin/article/edit?code_ski=' + id_skis)
