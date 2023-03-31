import sqlite3
import datetime




# Ajout d'éléments dans la BDD

#creation utilisateur
def creer_utilisateur(nom:str, email:str, mdp:str, jwt:str) -> int:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO utilisateur 
                        VALUES (NULL, ?, ?, 1, ?, ?)
                    """, (nom, email, mdp, jwt))
    id_user = curseur.lastrowid
    connexion.commit()

    connexion.close()
    return id_user

#creation action
def creer_action(titre:str, contenu:str, auteur_id:int) -> None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO actions 
                        VALUES (NULL, ?, ?, ?, ?)
                    """, (titre, contenu, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), auteur_id))
    # En savoir plus sur les dates : http://www.python-simple.com/python-modules-autres/date-et-temps.php
    connexion.commit()
    connexion.close()
    
# Auth utilisateur : 

def obtenir_jwt_depuis_email_mdp(email:str, mdp:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM utilisateur WHERE email=? AND mdp=?
                    """, (email, mdp))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

#obtenir l'id d'un utilisateur depuis son mail
def get_users_by_mail(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM utilisateur WHERE email=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

#obtenir l'id d'un utilisateur depuis son JWT
def get_users_by_JWT(JWT:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM utilisateur WHERE JWT=?
                    """, (JWT,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat



def get_id_user_by_email(email:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT id FROM utilisateur WHERE email=?
                    """, (email,))
    resultat = curseur.fetchone()
    connexion.close()
    return resultat

#séléctionner les actions disponibles
def select_actions_dispo(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM actions WHERE email=?
                    """, (mail,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

#changement de JWT
def update_token(id, token:str)->None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE utilisateur
                        SET jwt = ?
                        WHERE id=?
                    """,(token, id))
    connexion.commit()
    connexion.close()
    
# Obtenir actions d'un utilisateur : 
#voir les actions des personnes que l'on suit
def obtenir_action_user(id_user:int) -> list:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM actions WHERE utilisateur_id = ?
                    """, (id_user,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat


