#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, flash, session

from connexion_db import get_db

admin_commande = Blueprint('admin_commande', __name__,
                        template_folder='templates')

@admin_commande.route('/admin')
@admin_commande.route('/admin/commande/index')
def admin_index():
    return render_template('admin/layout_admin.html')


@admin_commande.route('/admin/commande/show', methods=['get','post'])
def admin_commande_show():
    mycursor = get_db().cursor()
    admin_id = session['id_user']
    sql = ''' 
     SELECT c.date_achat,SUM(lc.quantite_ligne_commande) AS nbr_skis,c.id_commande,
ROUND(SUM(lc.prix * lc.quantite_ligne_commande),2) AS prix_total,e.libelle,c.id_etat AS etat_id
FROM commande c
INNER JOIN ligne_commande lc on c.id_commande = lc.id_commande
INNER JOIN etat e on c.id_etat = e.id_etat
GROUP BY c.id_commande;
     '''
    mycursor.execute(sql)
    commandes = mycursor.fetchall()

    skis_commande = None
    commande_adresses = None
    id_commande = request.args.get('id_commande', None)
    print(id_commande)
    if id_commande != None:
        sql = ''' 
SELECT sk.libelle_skis AS nom, lc.quantite_ligne_commande AS quantite, lc.prix, 
ROUND((lc.quantite_ligne_commande*lc.prix), 2) AS prix_ligne
FROM ligne_commande lc
INNER JOIN skis sk on lc.code_ski = sk.code_ski
WHERE id_commande=%s; '''
        mycursor.execute(sql, (id_commande, ))
        skis_commande = mycursor.fetchall()
        commande_adresses = []
    return render_template('admin/commandes/show.html'
                           , commandes=commandes
                           , skis_commande=skis_commande
                           , commande_adresses=commande_adresses
                           )


@admin_commande.route('/admin/commande/valider', methods=['get','post'])
def admin_commande_valider():
    mycursor = get_db().cursor()
    commande_id = request.form.get('id_commande', None)
    sql = ''' SELECT * FROM commande WHERE id_commande=%s '''
    mycursor.execute(sql, (commande_id, ))
    commande = mycursor.fetchone()
    if commande['id_etat'] is not 3:
        if commande_id != None:
            print(commande_id)
            sql = ''' UPDATE commande SET id_etat=id_etat+1 WHERE id_commande=%s '''
            mycursor.execute(sql, commande_id)
            get_db().commit()
    return redirect('/admin/commande/show')