
# 🚀 Guide de Lancement – API_Adresse_Risques

## 📦 1. Prérequis

Avant de commencer, assurez-vous d’avoir les outils suivants installés sur votre machine :

- 🐳 Docker & Docker Compose : pour exécuter l’API et la base de données sans configuration manuelle.

---

## ▶️ 2. Lancer l’application

### 🧬 Cloner le dépôt Git

```bash
git clone https://github.com/fawziben/API_Adresses_Risques.git
cd API_Adresses_Risques
```

### 🛠️ Configurer les variables d’environnement

Reonnomer le fichier `.env.example` en `.env` :

modifiez la variable DJANGO_SECRET_KEY dans votre .env en y mettant une clé secrète.

### 🔧 Lancer le projet avec Docker

```bash
docker-compose up --build
```

🕐 Patientez quelques secondes que les services soient prêts, puis ouvrez votre navigateur à l’adresse :

📎 [http://localhost:8000/api](http://localhost:8000/api)

---

## 📡 3. Interrogation des Endpoints

### 🧭 Méthode 1 : Interface Visuelle

#### 🔍 Recherche d'une adresse

- 📎 [http://localhost:8000/api/form](http://localhost:8000/api/form)
- 👉 Accès à une page de saisie pour interroger l'API

![image](https://github.com/user-attachments/assets/c1a2214d-d3ad-45a1-9592-1b3a605d28bd)

- 👉 Saisir une adresse à rechercher, puis cliquer sur **Rechercher**
- 👉 Une page contenant les informations de sortie de la requête s’affiche

![image](https://github.com/user-attachments/assets/53ec3308-4351-4417-855b-f2b7fb1b9361)

#### ⚠️ Récupérer les risques liés à une adresse

- 📎 [http://localhost:8000/api/addresses/1/risks](http://localhost:8000/api/addresses/1/risks)
- 👉 Une page contenant les informations de sortie s’affiche

![image](https://github.com/user-attachments/assets/4242461c-fe1b-41e6-87f9-62d9ecdc1f13)

---

### 📬 Méthode 2 : Utilisation de Postman

#### 🔍 Recherche d’une adresse

1. Définir la méthode à `POST`
2. Saisir l’URL : `http://localhost:8000/api/addresses/`
3. Dans l’onglet **Body**, choisir `form-data`
   - `Key` : `address`  
   - `Value` : `9 bd du port`
4. Cliquer sur **Send**
5. Résultat visible dans l’onglet **Preview**

![image](https://github.com/user-attachments/assets/540c52af-0000-49a1-bf3a-42984a9b899e)

#### ⚠️ Récupérer les risques liés à une adresse

1. Définir la méthode à `GET`
2. Saisir l’URL : `http://localhost:8000/api/addresses/1/risks`
3. Cliquer sur **Send**

---

## 📝 Remarque : Affichage JSON au lieu de HTML

Si vous souhaitez recevoir les résultats sous **format JSON** (au lieu de pages HTML), modifiez le retour dans la vue Django :

```python
# Pour affichage HTML
return render(request, "api/sortie.html", context)

# Pour affichage JSON (à activer à la place du précédent)
# return JsonResponse(context, status=200)
```

> 💡 Il suffit de commenter le `render()` et de décommenter la ligne `JsonResponse`.

---

## 📁 Structure du Projet

```
API_Adresses_Risques/
├── api/                      # App principale contenant les vues et modèles
├── templates/api/            # Templates HTML pour les interfaces
├── docker-compose.yml        # Fichier Docker Compose pour lancer le projet
├── manage.py                 # Script de gestion Django
└── requirements.txt          # Dépendances Python
```

---

