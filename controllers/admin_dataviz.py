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
    sql = '''
SELECT SUM(dl.stock) AS nbr_skis, ts.libelle_ski AS libelle, ts.id_type_skis
FROM declinaison dl
INNER JOIN skis s on dl.code_ski = s.code_ski
INNER JOIN type_skis ts on s.type_skis_id = ts.id_type_skis
GROUP BY ts.libelle_ski
           '''
    mycursor.execute(sql)
    datas_show = mycursor.fetchall()
    labels = [str(row['libelle']) for row in datas_show]
    values = [int(row['nbr_skis']) for row in datas_show]

    # sql = '''
    #         
    #        '''
    return render_template('admin/dataviz/dataviz_etat_1.html'
                           , datas_show=datas_show
                           , labels=labels
                           , values=values)

