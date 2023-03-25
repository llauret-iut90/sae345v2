#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                          template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    sql = '''SET FOREIGN_KEY_CHECKS = 0;'''
    mycursor.execute(sql)

    sql = ''' SET GLOBAL sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));'''
    mycursor.execute(sql)

    sql = '''DROP TABLE IF EXISTS note,commentaire,ligne_panier,ligne_commande,declinaison,commande,skis,etat,utilisateur,couleur,type_skis;'''

    mycursor.execute(sql)
    sql = '''
CREATE TABLE type_skis
(
    id_type_skis INT AUTO_INCREMENT NOT NULL,
    libelle_ski  VARCHAR(50),
    PRIMARY KEY (id_type_skis)
);
    '''
    mycursor.execute(sql)
    sql = ''' 
CREATE TABLE couleur
(
    n_couleur   INT AUTO_INCREMENT NOT NULL,
    nom_couleur VARCHAR(50),
    PRIMARY KEY (n_couleur)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE utilisateur
(
    id_utilisateur INT AUTO_INCREMENT,
    login          VARCHAR(255),
    email          VARCHAR(255),
    nom            VARCHAR(255),
    password       VARCHAR(255),
    role           VARCHAR(255),
    PRIMARY KEY (id_utilisateur)
) ENGINE = InnoDB
  Default CHARSET utf8mb4;
    '''
    mycursor.execute(sql)
    sql = ''' 
CREATE TABLE etat
(
    id_etat INT AUTO_INCREMENT NOT NULL,
    libelle VARCHAR(50),
    PRIMARY KEY (id_etat)
);
    '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE skis
(
    code_ski     INT AUTO_INCREMENT NOT NULL,
    libelle_skis VARCHAR(50),
    image_skis   VARCHAR(50),
    type_skis_id INT                NOT NULL,
    prix_skis    VARCHAR(99),
    description VARCHAR(999),
    PRIMARY KEY (code_ski),
    FOREIGN KEY (type_skis_id) REFERENCES type_skis (id_type_skis)
);
    '''
    mycursor.execute(sql)
    sql = ''' 
CREATE TABLE commande
(
    id_commande    INT AUTO_INCREMENT NOT NULL,
    date_achat     DATE,
    id_utilisateur INT                NOT NULL,
    id_etat        INT                NOT NULL,
    PRIMARY KEY (id_commande),
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur (id_utilisateur),
    FOREIGN KEY (id_etat) REFERENCES etat (id_etat)
);
     '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE declinaison
(
    id_declinaison INT AUTO_INCREMENT NOT NULL,
    stock          INT(50),
    id_couleur     INT                NOT NULL,
    code_ski       INT                NOT NULL,
    PRIMARY KEY (id_declinaison),
    FOREIGN KEY (id_couleur) REFERENCES couleur (n_couleur),
    FOREIGN KEY (code_ski) REFERENCES skis (code_ski)
); 
     '''
    mycursor.execute(sql)
    sql = ''' 
CREATE TABLE ligne_commande
(
    id_commande             INT(50),
    code_ski                INT(50),
    prix                    VARCHAR(99),
    quantite_ligne_commande INT(50),
    n_declinaison INT DEFAULT 0,
    PRIMARY KEY (code_ski, id_commande, n_declinaison),
    FOREIGN KEY (code_ski) REFERENCES skis (code_ski),
    FOREIGN KEY (id_commande) REFERENCES commande (id_commande)
);
         '''
    mycursor.execute(sql)

    sql = ''' 
CREATE TABLE ligne_panier
(
    code_ski              INT AUTO_INCREMENT NOT NULL,
    utilisateur_id        INT(50),
    quantite_ligne_panier INT,
    date_ajout            DATE,
    n_declinaison INT DEFAULT 0,
    PRIMARY KEY (code_ski, utilisateur_id, n_declinaison),
    FOREIGN KEY (code_ski) REFERENCES skis (code_ski),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);
     '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE commentaire
(
    Id_utilisateur   INT,
    Id_skis          INT,
    date_publication DATE,
    commentaire      VARCHAR(99),
    valider          tinyint(1),
    PRIMARY KEY (Id_utilisateur, Id_skis, date_publication),
    FOREIGN KEY (Id_utilisateur) REFERENCES utilisateur (id_utilisateur),
    FOREIGN KEY (Id_skis) REFERENCES skis (code_ski)
);
         '''
    mycursor.execute(sql)

    sql = ''' 
    CREATE TABLE note
(
    Id_utilisateur INT,
    Id_skis        INT,
    note           INT(5),
    PRIMARY KEY (Id_utilisateur, Id_skis),
    FOREIGN KEY (Id_utilisateur) REFERENCES utilisateur (id_utilisateur),
    FOREIGN KEY (Id_skis) REFERENCES skis (code_ski)
);
         '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO utilisateur(id_utilisateur, login, email, password, role, nom)
VALUES (1, 'admin', 'admin@admin.fr',
        'sha256$dPL3oH9ug1wjJqva$2b341da75a4257607c841eb0dbbacb76e780f4015f0499bb1a164de2a893fdbf',
        'ROLE_admin', 'admin'),
       (2, 'client', 'client@client.fr',
        'sha256$1GAmexw1DkXqlTKK$31d359e9adeea1154f24491edaa55000ee248f290b49b7420ced542c1bf4cf7d',
        'ROLE_client', 'client'),
       (3, 'client2', 'client2@client2.fr',
        'sha256$MjhdGuDELhI82lKY$2161be4a68a9f236a27781a7f981a531d11fdc50e4112d912a7754de2dfa0422',
        'ROLE_client', 'client2');
                 '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO type_skis(libelle_ski)
VALUES ('Alpin'),('Nordique'),('Freeride'),('Freestyle');
         '''
    mycursor.execute(sql)
    sql = ''' 
INSERT INTO couleur(n_couleur, nom_couleur)
VALUES (1, 'Blanc'),(2, 'Noir'),(3, 'Rouge'),(4, 'Bleu');
         '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO etat(libelle)
VALUES ('En cours de traitement'),('expédié'),('validé');
         '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO skis(libelle_skis, type_skis_id, image_skis, prix_skis, description)
VALUES ('Ski Rossignol Experience 88', 1, 'ski_1.png', 500.12,
        'un ski de niveau intermédiaire à avancé qui offre une grande stabilité sur les pistes ainsi qu''une bonne accroche sur la neige dure. Il convient parfaitement pour les skieurs qui cherchent à améliorer leur technique.'),
       ('Ski Salomon QST Lumen Jr', 2, 'ski_2.png', 300.12,
        'un ski pour enfant/junior qui est facile à manier et qui offre une grande polyvalence sur tous les types de terrain. Il convient parfaitement pour les jeunes skieurs qui cherchent à progresser.'),
       ('Ski Mini Ranger Jr', 2, 'ski_3.png', 600.95,
        'un ski pour enfant/junior qui est très facile à manier et qui offre une bonne stabilité sur les pistes. Il convient parfaitement pour les jeunes skieurs qui cherchent à s''amuser sur les pistes.'),
       ('Ski Extreme Ranger 98 Ti', 4, 'ski_4.png', 100.36,
        'un ski pour les skieurs confirmés qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité et une excellente accroche sur la neige dure.'),
       ('Ski Night Rider 102 FR', 4, 'ski_5.png', 400.50,
        'un ski pour les skieurs confirmés qui cherchent à s''amuser dans la poudreuse. Il offre une bonne portance et une grande maniabilité dans la neige profonde.'),
       ('Ski Faller Snow 102', 4, 'ski_6.png', 700.58,
        'un ski pour les skieurs confirmés qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité et une excellente accroche sur la neige dure.'),
       ('XL Rode Poler 107', 4, 'ski_7.png', 452.12,
        'un ski pour les skieurs experts qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité à haute vitesse ainsi qu''une excellente portance en poudreuse.'),
       ('Ski Ignite ice 110 FR', 1, 'ski_8.png', 875.64,
        'un ski pour les skieurs experts qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité à haute vitesse ainsi qu''une excellente accroche sur la neige dure.'),
       ('Ski Fresh Forest 110', 3, 'ski_9.png', 696.42,
        'un ski pour les skieurs avancés qui cherchent à s''amuser sur les pistes. Il offre une grande maniabilité ainsi qu''une bonne accroche sur la neige dure.'),
       ('Ski Dominus Rango 130', 4, 'ski_10.png', 712.78,
        'un ski pour les skieurs experts qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité à haute vitesse ainsi qu''une excellente portance en poudreuse.'),
       ('Ski Octane White 110 FR', 3, 'ski_11.png', 300.00,
        'un ski pour les skieurs avancés qui cherchent à s''amuser sur les pistes. Il offre une grande maniabilité ainsi qu''une bonne accroche sur la neige dure.'),
       ('Ski Nord Ghost 110', 2, 'ski_12.png', 621.45,
        'un ski pour les skieurs intermédiaires à avancés qui cherchent à s''amuser sur les pistes. Il offre une grande maniabilité ainsi qu''une bonne accroche sur la neige dure.'),
       ('Ski Fischl Tiger 130', 3, 'ski_13.png', 278.23,
        'un ski pour les skieurs avancés qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité à haute vitesse ainsi qu''une excellente portance en poudreuse.'),
       ('Ski RAiden venti 110 FR', 4, 'ski_14.png', 587.15,
        'un ski pour les skieurs experts qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité à haute vitesse ainsi qu''une excellente portance en poudreuse.'),
       ('Ski Fischer Ranger 110', 4, 'ski_15.png', 675.45,
        'un ski pour les skieurs experts qui cherchent à explorer tous les types de terrain. Il offre une grande stabilité à haute vitesse ainsi qu''une excellente portance en poudreuse.');
         '''
    mycursor.execute(sql)

    sql = ''' 
INSERT INTO declinaison(stock, id_couleur, code_ski)
VALUES (23, 1, 1),(5, 2, 4),(15, 3, 2),(20, 4, 3),(17, 2, 15),(18, 1, 7),(10, 3, 8),(4, 4, 9),(3, 2, 10),(2, 1, 11),
(5, 1, 12),(24, 3, 13),(52, 3, 14),(36, 2, 5),(12, 4, 6),(15, 1, 6),(14, 3, 1);
         '''
    mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
