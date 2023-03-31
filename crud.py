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
                    """, (nom, email, mdp,datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), jwt))
    id_user = curseur.lastrowid
    connexion.commit()

    connexion.close()
    return id_user

#permettre à un utilisateur d'en suivre un autre

def user_suivi_user(id_suiveur:int, id_suivi:int) -> None:
    
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO asso_suivi
                        VALUES (?,?     
                        )
                    """, (id_suiveur,id_suivi))
    
    connexion.commit()

    connexion.close()


#creer une action dans la table action
def creer_action(id_user:int) -> None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO actions 
                        VALUES (?, ?)
                    """, (id_user, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
    # En savoir plus sur les dates : http://www.python-simple.com/python-modules-autres/date-et-temps.php
    connexion.commit()
    connexion.close()
    
#creer une ligne en remplissant les champs dans la table portefeuilleactions

def creer_ligne_action(id_user:int,id_action: int,prix_achat:int,prix_vente:int,date_achat,date_vente) -> list :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    INSERT INTO portefeuilleactions 
                        VALUES (?, ?, NULL, NULL, NULL, NULL)
                    """, (id_user,id_action,prix_achat,prix_vente, datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"),datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")))
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

#obtenir le JWT avec l'auth id/mdp
def get_JWT_by_mail(JWT:str, mail:str, mdp:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT jwt FROM utilisateur 
                    WHERE mail=? AND mdp=?
                    """, (JWT,mail, mdp))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat


#séléctionner les actions disponibles
def select_actions_dispo(mail:str):
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM actions WHERE id=?
                    """, (id,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

#changement de JWT
def update_token(id, jwt:str)->None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE utilisateur
                        SET jwt = ?
                        WHERE id=?
                    """,(jwt, id))
    connexion.commit()
    connexion.close()
    
#changement de mail
def update_email(id, mail:str) -> None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE utilisateur
                        SET mail = ?
                        WHERE id=?
                    """,(mail, id))
    connexion.commit()
    connexion.close()
    
#changement de mdp
def update_email(mdp:str, mail:str) -> None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE utilisateur
                        SET mdp = ?
                        WHERE mail=?
                    """,(mdp,mail))
    connexion.commit()
    connexion.close()
    
#changement de valeur action
def update_action(entreprise:str, prix:int) -> None:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE action
                        SET prix = ?
                        WHERE entreprise =?
                    """,(entreprise,prix))
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


#obtenir les actions d'une personne suivi


def obtenir_action_suivi(id_user:int) -> list:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM actions WHERE utilisateur_id = ?
                    """, (id_user,))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

#vendre une action
def vendre_action(id_action:int,id_user:int,prix_vente:int, email:str) -> list:
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    UPDATE portefeuille_actions
                        SET id_user = ? 
                        SET prix_vente = ?
                        SET date_vente = ?
                        WHERE id_action = ?
                    """, (id_user,prix_vente,datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"), id_action))

# vérifié la validité du JWT
def verifier_JWT(jwt) -> None :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    SELECT * FROM utilisateur 
                    WHERE jwt = ?
                    """, (jwt))
    resultat = curseur.fetchall()
    if len(resultat) <1 :
        return False
    return True
    connexion.close()
    return resultat


#suppimer un utilisateur
def supprimer_user(id) -> None :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM utilisateur
                    WHERE id =?
                    """, (id))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

#supprimer suivi
def supprimer_suivi(id_suiveur, id_suivi) -> None :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM asso_suivi
                    WHERE id_suivi =? OR id_suiveur=?
                    """, (id_suiveur, id_suivi))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat

#supprimer une action

def supprimer_action(id_action) -> None :
    connexion = sqlite3.connect("bdd.db")
    curseur = connexion.cursor()
    curseur.execute("""
                    DELETE FROM action
                    WHERE id_action = ?
                    """, (id_action))
    resultat = curseur.fetchall()
    connexion.close()
    return resultat