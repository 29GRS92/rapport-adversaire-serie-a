import sys  # pour lire les informations données au lancement du script
import os  # pour créer le dossier de sauvegarde et tester l'existence des fichiers
import re  # pour fabriquer des noms de fichiers à partir des adresses
import random  # pour varier légèrement les pauses entre les demandes
from playwright.sync_api import sync_playwright  # pour piloter un vrai navigateur

dossier = sys.argv[1]  # dossier où seront sauvegardées les données, donné au lancement
chemins = []  # liste de toutes les adresses de données à demander, sans le nom du site
for element in sys.argv[2:]:  # parcourt les informations données après le dossier
    if element.endswith('.txt'):  # si c'est un fichier texte, il contient une adresse par ligne
        with open(element, encoding='utf-8') as f:  # ouvre ce fichier
            chemins.extend([ligne.strip() for ligne in f if ligne.strip()])  # ajoute chaque ligne non vide à la liste
    else:  # sinon, c'est directement une adresse
        chemins.append(element)  # l'ajoute à la liste
os.makedirs(dossier, exist_ok=True)  # crée le dossier s'il n'existe pas encore


def nom_fichier(chemin):  # petite recette : fabrique le nom du fichier de sauvegarde d'une adresse
    return re.sub('[^a-zA-Z0-9]+', '_', chemin).strip('_') + '.json'  # remplace tout caractère spécial par un tiret bas


a_faire = [c for c in chemins if not os.path.exists(os.path.join(dossier, nom_fichier(c)))]  # garde seulement les adresses dont le fichier n'existe pas encore, ce qui permet de reprendre après une coupure
print("Adresses demandées :", len(chemins), "| déjà sauvegardées :", len(chemins) - len(a_faire), "| à télécharger :", len(a_faire))  # affiche le bilan avant de commencer

echecs = []  # liste des adresses qui n'ont pas pu être téléchargées

if a_faire:  # s'il y a quelque chose à télécharger
    with sync_playwright() as p:  # démarre le pilote de navigateur
        navigateur = p.chromium.launch(headless=False)  # ouvre un vrai navigateur visible
        page = navigateur.new_page()  # ouvre un nouvel onglet
        page.goto('https://www.sofascore.com/fr/', wait_until='domcontentloaded', timeout=60000)  # ouvre la page d'accueil de Sofascore, pour être dans les conditions d'une vraie visite
        page.wait_for_timeout(8000)  # attend 8 secondes pour laisser la page s'installer
        for n, chemin in enumerate(a_faire, 1):  # parcourt les adresses à télécharger, n est le compteur
            try:  # essaie de télécharger cette adresse
                resultat = page.evaluate("async (chemin) => { const r = await fetch(chemin, {credentials: 'include'}); const t = await r.text(); return {statut: r.status, texte: t}; }", chemin)  # demande la donnée depuis la page elle-même, comme le fait le site
            except Exception as erreur:  # si la demande plante
                echecs.append((chemin, str(erreur)[:80]))  # note l'adresse et le début du message d'erreur
                continue  # passe à l'adresse suivante
            if resultat['statut'] == 200:  # si la demande a réussi
                with open(os.path.join(dossier, nom_fichier(chemin)), 'w', encoding='utf-8') as f:  # ouvre le fichier de sauvegarde
                    f.write(resultat['texte'])  # sauvegarde la donnée reçue
            else:  # sinon, la demande a été refusée ou l'adresse n'existe pas
                echecs.append((chemin, resultat['statut']))  # note l'adresse et le code de réponse
            if n % 10 == 0:  # toutes les 10 adresses
                print(n, "sur", len(a_faire), "traitées")  # affiche l'avancement
            page.wait_for_timeout(random.randint(1000, 2000))  # attend entre 1 et 2 secondes avant la demande suivante, pour rester poli avec le site
        navigateur.close()  # ferme le navigateur

print("Échecs :", len(echecs))  # affiche le nombre d'échecs, on en attend 0
for e in echecs[:10]:  # parcourt les dix premiers échecs
    print(e)  # affiche l'adresse concernée et la cause
