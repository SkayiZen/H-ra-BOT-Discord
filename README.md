# 🤖 Héra - Bot Discord

**Héra** est un bot Discord conçu pour gérer une flotte de véhicules et discuter avec les utilisateurs via un scénario interactif. Ce projet a été réalisé dans le cadre d'un cursus B2 (Python).

---

## ✨ Fonctionnalités

### 🚗 Gestion du Garage
Accédez à la base de données des véhicules (fichier CSV).
- `/garage` : Affiche la liste des véhicules (avec filtres : Dispo, Panne, etc.).
- `/search [marque]` : Recherche un véhicule par marque (avec menu déroulant).
- `/check [plaque]` : Vérifie l'état précis d'une voiture via sa plaque.

### 💬 Discussion Interactive
Un système de questions/réponses basé sur un arbre de décision.
- `/discuss` : Lance le questionnaire interactif (boutons et menus).
- `/speak_about [sujet]` : Vérifie si le bot connaît un sujet précis.

### 📜 Historique
Le bot mémorise vos actions (implémentation via Liste Chaînée).
- `/history` : Affiche toutes vos commandes passées.
- `/last` : Affiche votre dernière commande.
- `/clear_history` : Efface votre historique.

---

## 🛠️ Installation

1. **Prérequis**
   - Python 3.9 ou supérieur.
   - Les fichiers du projet (`main.py`, dossiers `config`, `core`, `commandes`).

2. **Installation des modules**
   Ouvrez un terminal et tapez :
   ```bash
   pip install discord.py python-dotenv
   ```

3. **Configuration Créez un fichier nommé .env à la racine et ajoutez votre token :**
    ```bash
   DISCORD_TOKEN=VOTRE_TOKEN_ICI
   ```

4. **Lancement**
    ```bash
    python main.py
    ```
  
📂 **Structure du Projet**
Le projet est organisé de manière modulaire pour être propre et maintenable :

`main.py` : Le fichier de lancement.

`config/` : Contient le `scenario.json` (dialogues) et le fichier CSV des véhicules.

`core/` : Le "moteur" du bot (Algorithmes, Sauvegardes, Affichage).

`commandes/` : Les fichiers de commandes (triés par dossiers).

ℹ️ Infos Techniques
**Langage** : Python.

**Bibliothèque** : `discord.py`

**Particularité **: Les structures de données (Arbre de décision et Liste chaînée pour l'historique) sont codées à la main, sans utiliser de modules tout faits.