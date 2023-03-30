import sqlite3 

con = sqlite3.connect("bdd.db")
curseur = con.cursor()

"""
https://sql.sh/
"""

curseur.execute("""
                CREATE TABLE IF NOT EXISTS utilisateur (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nom TEXT NOT NULL,
                    email TEXT NOT NULL,
                    mdp TEXT NOT NULL,
                    JWT INTEGER NOT NULL,
                
)
""")
con.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS actions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    entreprise TEXT NOT NULL,
                    prix INTEGER NOT NULL,
                    utilisateur_id INTEGER,
                    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
)
""")
con.commit()


curseur.execute("""
                CREATE TABLE IF NOT EXISTS portefeuille_actions(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                id_action INTEGER,
                id_user INTEGER,
                prix_achat INTEGER,
                prix_vente INTEGER,
                data_achat DATETIME,
                date_vente DATETIME,
                FOREIGN KEY (id_action) REFERENCES actions(id),
                FOREIGN KEY (id_user) REFERENCES utilisateur(id)

)
""")
con.commit()

curseur.execute("""
                CREATE TABLE IF NOT EXISTS asso_suivant(
                id_suiveur INTEGER,
                id_suivi INTEGER,
                FOREIGN KEY (id_suiveur) REFERENCES utilisateur(id),
                FOREIGN KEY (id_suivi) REFERENCES utilisateur(id)
)
""")
con.commit()



con.close()
