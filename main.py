from fastapi import FastAPI, HTTPException, Request, Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import crud
import hashlib

# pip install "python-jose[cryptography]"
# pip install "passlib[bcrypt]"

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

# Fonctions utiles :
def hasher_mdp(mdp:str) -> str:
    return hashlib.sha256(mdp.encode()).hexdigest()

def decoder_token(token:str)->dict:
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

def verifier_token(req: Request):
    token = req.headers["Authorization"]
    

# Classes contenu
class UserRegister(BaseModel):
    nom:str
    email:str
    mdp:str

class UserLogin(BaseModel):
    email:str
    mdp:str

class Usersuivi(BaseModel):
    id_suiveur:int
    id_suivi:int
    
class Follow(BaseModel):
    email_suivi: str
    

    
    
app = FastAPI()



# Début des endpoints

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/api/auth/inscription")
async def inscription(user:UserRegister):
    if len(crud.get_users_by_mail(user.email)) > 0:
        raise HTTPException(status_code=403, detail="L'email fourni possède déjà un compte")
    else:
        id_user = crud.creer_utilisateur(user.nom, user.email, hasher_mdp(user.mdp), None)
        token = jwt.encode({
            "email" : user.email,
            "mdp" : user.mdp,
            "id" : id_user
        }, SECRET_KEY, algorithm=ALGORITHM)
        crud.update_token(id_user, token)
        return {"token" : token}
    

    
    
@app.post("/api/users/follow/")
async def follow(user:Usersuivi):
    crud.user_suivi_user(user.id_suiveur, user.id_suivi)
    return {"message": "L'utilisateur avec l'ID " + str(user.id_suiveur) + " suit désormais l'utilisateur avec l'ID " + str(user.id_suivi)}


@app.post("/api/creeactions/")
async def creer_action_table_action(id_user:int, id_action:int):
    crud.creer_action(id_user, id_action)
    return {"message": "L'action a été créée avec succès."}



# @app.delete("/utilisateur/arreter_de_suivre_utilisateur")
# async def arreter_de_suivre_utilisateur(req: Request, follow: follow):
#     try:
#         decode = decoder_token(req.headers["Authorization"])
#         crud.arreter_de_suivre_utilisateur(decode["id"], follow.email_suivi)
#         return {"message": "L'utilisateur n'est plus suivi."}
#     except:
#         raise HTTPException(status_code=401, detail="Vous devez être identifié pour accéder à cet endpoint.")
    

# @app.put("/utilisateur/mettre_a_jour_utilisateur/{id}")
# async def modifier_utilisateur_route(id: int, utilisateur: User) -> None:
#     crud.modifier_utilisateur(id, utilisateur.pseudo, utilisateur.email, utilisateur.mdp)
#     return {"detail": "Utilisateur mis à jour avec succès"}


# @app.get("/utilisateur/portefeuille/{user_id}")
# async def portefeuille_route(user_id: int) -> dict:
#     portefeuille_data = crud.portefeuille(user_id)
#     return {"portefeuille": portefeuille_data}

# @app.post("/api/ajoutaction/")
# async def inscrire_action_portefeuillesactions(id_user:int,id_action: int,prix_achat:int,prix_vente:int,date_achat,date_vente):
#     crud.creer_ligne_action( id_user,id_action,prix_achat,prix_vente,date_achat,date_vente)
#     return {"message": "les attributs de l'action creer ont etait ajoutés ."}


@app.post("/api/auth/token")
async def login_token(user:UserLogin):
    resultat = crud.obtenir_jwt_depuis_email_mdp(user.email, hasher_mdp(user.mdp))
    if resultat is None:
        raise HTTPException(status_code=401, detail="Login ou mot de passe invalide")
    else:
        return {"token":resultat[0]}
    
@app.get("/api/actions")
async def Mes_actions(req: Request):
    try:
        decode = decoder_token(req.headers["Authorization"])
        return {"id_user" : crud.get_users_by_email(decode["email"])[0]}
    except:
        raise HTTPException(status_code=401, detail="Vous devez être identifiés pour accéder à cet endpoint")
    


