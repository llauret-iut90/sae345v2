#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import Blueprint
from flask import Flask, request, render_template, redirect, abort, flash, session

from connexion_db import get_db

admin_dataviz = Blueprint('admin_dataviz', __name__,
                          template_folder='templates')


@admin_dataviz.route('/admin/dataviz/etat1')
def show_type_article_stock():
    mycursor = get_db().cursor()
    sql = '''SELECT ts.libelle_ski as type_ski,
       ts.id_type_skis,
       s.libelle_skis AS nom_skis,
       GROUP_CONCAT(s.libelle_skis) as skis,
       IFNULL(ROUND(AVG(DISTINCT n.note),2), 0) AS moyenne_note, 
       COUNT(DISTINCT n.note) AS nb_notes, 
       COUNT(DISTINCT c.commentaire) AS nbr_commentaires
FROM skis s
INNER JOIN type_skis ts ON s.type_skis_id = ts.id_type_skis
LEFT JOIN note n ON s.code_ski = n.Id_skis
LEFT JOIN commentaire c ON s.code_ski = c.Id_skis
GROUP BY ts.libelle_ski, ts.id_type_skis, s.libelle_skis
ORDER BY ts.id_type_skis, moyenne_note DESC;
           '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['nom_skis']) for row in datas_show]
    values = [int(row['nbr_commentaires']) for row in datas_show]

    # sql = '''
    #         
    #        '''
    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)
