#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_type_article = Blueprint('admin_type_article', __name__,
                        template_folder='templates')

@admin_type_article.route('/admin/type-article/show')
def show_type_article():
    mycursor = get_db().cursor()

    sql = "SELECT * from type_skis;"

    mycursor.execute(sql)

    type_skis = mycursor.fetchall()

    return render_template('admin/type_article/show_type_article.html', type_skis=type_skis)

@admin_type_article.route('/admin/type-article/add', methods=['GET'])
def add_type_article():
    mycursor = get_db().cursor()
    sql = "SELECT * FROM type_skis;"
    mycursor.execute(sql)
    type_skis = mycursor.fetchall()
    return render_template('admin/type_article/add_type_article.html', type_skis=type_skis)

@admin_type_article.route('/admin/type-article/add', methods=['POST'])
def valid_add_type_article():
    mycursor = get_db().cursor()
    libelle_ski = request.form.get('libelle_ski', '')
    tuple_insert = (libelle_ski,)
    sql = "INSERT INTO type_skis (libelle_ski) VALUES (%s);"
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    print(u'Ski ajouté, Nom : ', libelle_ski)
    message = u'Ski ajouté, Nom : ' + libelle_ski
    flash(message, 'alert-success')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/delete', methods=['GET'])
def delete_type_article():
    mycursor = get_db().cursor()
    code_ski = request.args.get('code_ski', '')
    id_type_skis = request.args.get('id_type_skis', '')
    type_skis_id = request.args.get('type_skis_id', '')

    mycursor.execute("SET foreign_key_checks = 0")

    sql = "DELETE FROM skis WHERE type_skis_id = %s"
    mycursor.execute(sql, (type_skis_id,))

    sql_2 = "DELETE FROM type_skis WHERE id_type_skis = %s"
    mycursor.execute(sql_2, (id_type_skis,))

    get_db().commit()
    mycursor.execute("SET foreign_key_checks = 1")

    print(f"Type de ski supprimé, ID : {id_type_skis}")
    message = f"Type de ski supprimé, ID : {id_type_skis}"
    flash(message, 'alert-warning')
    return redirect('/admin/type-article/show')

@admin_type_article.route('/admin/type-article/edit', methods=['GET'])
def edit_type_article():
    mycursor = get_db().cursor()
    libelle_ski = request.args.get('libelle_ski', '')
    sql = "SELECT * from type_skis WHERE libelle_ski =%s;"

    mycursor.execute(sql, libelle_ski)
    type_skis = mycursor.fetchone()
    return render_template('admin/type_article/edit_type_article.html', type_skis=type_skis)

@admin_type_article.route('/admin/type-article/edit', methods=['POST'])
def valid_edit_type_article():
    mycursor = get_db().cursor()
    libelle_ski = request.form.get('libelle_ski', '')
    id_type_skis = request.form.get('id_type_skis', '')
    tuple_update = (libelle_ski, id_type_skis)

    sql = "UPDATE type_skis SET libelle_ski=%s WHERE id_type_skis=%s;"
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    print(u'Type de ski modifié, Nom : ', libelle_ski, ' | Id du type de ski :', id_type_skis)
    message = u'Type de ski modifié, Nom : ' + libelle_ski + ' | Id du type de ski : ' + id_type_skis
    flash(message, 'alert-success')
    return redirect('/admin/type-article/show')







