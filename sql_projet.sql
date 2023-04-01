DROP TABLE IF EXISTS note;
DROP TABLE IF EXISTS commentaire;
DROP TABLE IF EXISTS ligne_panier;
DROP TABLE IF EXISTS ligne_commande;
DROP TABLE IF EXISTS declinaison;
DROP TABLE IF EXISTS commande;
DROP TABLE IF EXISTS skis;
DROP TABLE IF EXISTS etat;
DROP TABLE IF EXISTS utilisateur;
DROP TABLE IF EXISTS couleur;
DROP TABLE IF EXISTS type_skis;

CREATE TABLE type_skis
(
    id_type_skis INT AUTO_INCREMENT NOT NULL,
    libelle_ski  VARCHAR(50),
    PRIMARY KEY (id_type_skis)
);

CREATE TABLE couleur
(
    n_couleur   INT AUTO_INCREMENT NOT NULL,
    nom_couleur VARCHAR(50),
    PRIMARY KEY (n_couleur)
);

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

CREATE TABLE etat
(
    id_etat INT AUTO_INCREMENT NOT NULL,
    libelle VARCHAR(50),
    PRIMARY KEY (id_etat)
);

CREATE TABLE skis
(
    code_ski     INT AUTO_INCREMENT NOT NULL,
    libelle_skis VARCHAR(50),
    image_skis   VARCHAR(50),
    type_skis_id INT                NOT NULL,
    prix_skis    VARCHAR(255),
    description  VARCHAR(255),
    PRIMARY KEY (code_ski),
    FOREIGN KEY (type_skis_id) REFERENCES type_skis (id_type_skis)
);

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

CREATE TABLE ligne_commande
(
    id_commande             INT(50),
    code_ski                INT(50),
    prix                    VARCHAR(255),
    quantite_ligne_commande INT(50),
    n_declinaison           INT,
    PRIMARY KEY (code_ski, id_commande, n_declinaison),
    FOREIGN KEY (code_ski) REFERENCES skis (code_ski),
    FOREIGN KEY (id_commande) REFERENCES commande (id_commande)
);

CREATE TABLE ligne_panier
(
    code_ski              INT AUTO_INCREMENT NOT NULL,
    utilisateur_id        INT(50),
    quantite_ligne_panier INT,
    date_ajout            DATE,
    n_declinaison         INT,
    PRIMARY KEY (code_ski, utilisateur_id, n_declinaison),
    FOREIGN KEY (code_ski) REFERENCES skis (code_ski),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur (id_utilisateur)
);

CREATE TABLE commentaire
(
    Id_utilisateur   INT,
    Id_skis          INT NOT NULL DEFAULT 0,
    nom              VARCHAR(255),
    date_publication DATETIME,
    commentaire      VARCHAR(255),
    valider          tinyint(1),
    PRIMARY KEY (Id_utilisateur, Id_skis, date_publication),
    FOREIGN KEY (Id_utilisateur) REFERENCES utilisateur (id_utilisateur),
    FOREIGN KEY (Id_skis) REFERENCES skis (code_ski)
);
CREATE TABLE note
(
    Id_utilisateur INT,
    Id_skis        INT,
    note           INT,
    PRIMARY KEY (Id_utilisateur, Id_skis),
    FOREIGN KEY (Id_utilisateur) REFERENCES utilisateur (id_utilisateur),
    FOREIGN KEY (Id_skis) REFERENCES skis (code_ski)
);

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

INSERT INTO type_skis(libelle_ski)
VALUES ('Alpin');
INSERT INTO type_skis(libelle_ski)
VALUES ('Nordique');
INSERT INTO type_skis(libelle_ski)
VALUES ('Freeride');
INSERT INTO type_skis(libelle_ski)
VALUES ('Freestyle');

INSERT INTO couleur(n_couleur, nom_couleur)
VALUES (1, 'Blanc');
INSERT INTO couleur(n_couleur, nom_couleur)
VALUES (2, 'Noir');
INSERT INTO couleur(n_couleur, nom_couleur)
VALUES (3, 'Rouge');
INSERT INTO couleur(n_couleur, nom_couleur)
VALUES (4, 'Bleu');

INSERT INTO etat(libelle)
VALUES ('En cours de traitement');
INSERT INTO etat(libelle)
VALUES ('expédié');
INSERT INTO etat(libelle)
VALUES ('validé');
INSERT INTO etat(libelle)
VALUES ('refusé');

INSERT
INTO commande(date_achat, id_utilisateur, id_etat)
VALUES ('2022-01-01', 1, 1);
INSERT
INTO commande(date_achat, id_utilisateur, id_etat)
VALUES ('2022-02-01', 2, 2);
INSERT
INTO commande(date_achat, id_utilisateur, id_etat)
VALUES ('2022-03-01', 3, 3);
INSERT
INTO commande(date_achat, id_utilisateur, id_etat)
VALUES ('2022-04-01', 2, 4);

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

INSERT INTO declinaison(stock, id_couleur, code_ski)
VALUES (23, 1, 1),
       (5, 2, 4),
       (15, 3, 2),
       (20, 4, 3),
       (17, 2, 15),
       (18, 1, 7),
       (10, 3, 8),
       (4, 4, 9),
       (3, 2, 10),
       (2, 1, 11),
       (5, 1, 12),
       (24, 3, 13),
       (52, 3, 14),
       (36, 2, 5),
       (12, 4, 6),
       (15, 1, 6),
       (14, 3, 1);
ALTER TABLE commentaire
ALTER COLUMN valider SET DEFAULT 0;
# SELECT *
# from commentaire;
# # INSERT INTO note(Id_utilisateur, note, Id_skis) VALUES (1,4,2);
# SELECT * from note;
# SELECT ROUND(SUM(note.note)/COUNT(note.note),2) AS moy_notes, COUNT(note.note) AS nb_notes
#     FROM note
#     INNER JOIN skis ON skis.code_ski = note.Id_skis
#     WHERE skis.code_ski = 1;
#
# SELECT skis.libelle_skis,skis.code_ski,skis.type_skis_id,type_skis.libelle_ski,
#           skis.prix_skis,SUM(declinaison.stock) AS stock,
#           COUNT(declinaison.id_declinaison) AS nb_declinaisons,
#           skis.image_skis,
#           (SELECT COUNT(commentaire.commentaire) FROM commentaire
#           WHERE Id_skis = skis.code_ski AND valider = 1) AS nb_commentaires_nouveaux
#            FROM declinaison
#           INNER JOIN skis ON declinaison.code_ski=skis.code_ski
#           INNER JOIN type_skis ON skis.type_skis_id=type_skis.id_type_skis
#           LEFT JOIN commentaire ON skis.code_ski = commentaire.Id_skis AND commentaire.valider = 0
#           GROUP BY skis.code_ski;
#
# SELECT skis.libelle_skis,
#        skis.code_ski,
#        skis.type_skis_id,
#        type_skis.libelle_ski,
#        skis.prix_skis,
#        SUM(declinaison.stock) AS stock,
#        COUNT(declinaison.id_declinaison) AS nb_declinaisons,
#        skis.image_skis,
#        SUM(CASE WHEN commentaire.valider = 0 THEN 1 ELSE 0 END) AS nb_commentaires_nouveaux
# FROM declinaison
# INNER JOIN skis ON declinaison.code_ski=skis.code_ski
# INNER JOIN type_skis ON skis.type_skis_id=type_skis.id_type_skis
# LEFT JOIN commentaire ON skis.code_ski = commentaire.Id_skis
# GROUP BY skis.code_ski;

# INSERT
# INTO ligne_commande(code_ski, id_commande, prix, quantite_ligne_commande)
# VALUES (1, 1, 500, 2);
# INSERT
# INTO ligne_commande(code_ski, id_commande, prix, quantite_ligne_commande)
# VALUES (2, 1, 700, 1);
# INSERT
# INTO ligne_commande(code_ski, id_commande, prix, quantite_ligne_commande)
# VALUES (3, 2, 600, 3);
# INSERT
# INTO ligne_commande(code_ski, id_commande, prix, quantite_ligne_commande)
# VALUES (4, 3, 200, 4);

# INSERT INTO ligne_panier(code_ski, utilisateur_id, quantite_ligne_panier, date_ajout, n_declinaison)
# VALUES (1, 2, 2, '2022-01-01', 1);
#
# INSERT INTO ligne_panier(code_ski, utilisateur_id, quantite_ligne_panier, date_ajout, n_declinaison)
# VALUES (2, 3, 2, '2022-02-01', 3);
#
# INSERT INTO ligne_panier(code_ski, utilisateur_id, quantite_ligne_panier, date_ajout, n_declinaison)
# VALUES (3, 2, 3, '2022-03-01', 4);

# SELECT sk.libelle_skis,
#        sk.code_ski,
#        sk.type_skis_id,
#        tp.libelle_ski,
#        sk.prix_skis,
#        SUM(dl.stock)            AS stock,
#        COUNT(dl.id_declinaison) AS nb_declinaisons,
#        sk.image_skis
# FROM skis sk
#          INNER JOIN declinaison dl ON dl.code_ski = sk.code_ski
#          INNER JOIN type_skis tp ON sk.type_skis_id = tp.id_type_skis
# GROUP BY sk.code_ski;
#
# SELECT *, tp.libelle_ski, SUM(dl.stock) AS stock
# FROM skis sk
#          INNER JOIN type_skis tp ON sk.type_skis_id = tp.id_type_skis
#          INNER JOIN declinaison dl ON dl.code_ski = sk.code_ski
# GROUP BY sk.code_ski
# ORDER BY sk.code_ski;
#
# SELECT sk.libelle_skis, sk.code_ski, sk.type_skis_id, tp.libelle_ski, sk.prix_skis, sk.image_skis
# FROM skis sk
#          INNER JOIN type_skis tp ON sk.type_skis_id = tp.id_type_skis
# GROUP BY sk.code_ski;
#
# SELECT *
# FROM skis
# WHERE skis.code_ski NOT IN (SELECT code_ski
#                             FROM declinaison);
#
# SELECT sk.libelle_skis, sk.code_ski, sk.type_skis_id, tp.libelle_ski, sk.prix_skis, sk.image_skis
# FROM skis sk
#          INNER JOIN type_skis tp ON sk.type_skis_id = tp.id_type_skis
# WHERE sk.code_ski NOT IN (SELECT code_ski
#                           FROM declinaison);
#
# SELECT SUM(dl.stock) AS stock, ts.libelle_ski
# FROM declinaison dl
#          INNER JOIN skis s on dl.code_ski = s.code_ski
#          INNER JOIN type_skis ts on s.type_skis_id = ts.id_type_skis
# GROUP BY ts.libelle_ski;
#
# SELECT dl.id_declinaison,dl.stock,dl.id_couleur,cl.n_couleur,sk.code_ski AS id_skis, cl.nom_couleur
#           FROM declinaison dl
#           INNER JOIN couleur cl ON dl.id_couleur=cl.n_couleur
#           INNER JOIN skis sk ON dl.code_ski=sk.code_ski
#           WHERE sk.code_ski = 1;

# SELECT COUNT(commande.date_achat) as commandes_articles FROM commande
#         INNER JOIN utilisateur ON utilisateur.id_utilisateur = commande.id_utilisateur
#         INNER JOIN ligne_commande ON ligne_commande.id_commande = commande.id_commande
#         INNER JOIN skis on ligne_commande.code_ski = skis.code_ski
#         WHERE skis.code_ski = 1 AND ligne_commande.id_commande = 1;

# SELECT COUNT(commande.id_commande) as commandes_articles
# FROM commande
#          INNER JOIN utilisateur ON utilisateur.id_utilisateur = commande.id_utilisateur
#          INNER JOIN ligne_commande ON ligne_commande.id_commande = commande.id_commande
#          INNER JOIN skis ON ligne_commande.code_ski = skis.code_ski
# WHERE skis.code_ski = 4
#   AND ligne_commande.id_commande = 1;
#
# SELECT *
# from ligne_commande;