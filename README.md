## Fonctionnalités

- Génération d'une image en fonction d'un prompt utilisateur.
- Archivage automatique de l'image précédente (nommée `IMG_XXXX.png`) en la copiant dans un fichier d'archive (`IMG_0001.png`, `IMG_0002.png`, etc.), pour éviter tout écrasement.
- Téléchargement et sauvegarde locale de l'image générée.

## Prérequis

- Python 3.x
- Une clé API pour OpenAI. Vous devez créer un fichier `config.json` dans le même répertoire que le script, contenant au minimum la clé API sous la forme :
  ```json config.json
  {
    "api_key": "VOTRE_CLÉ_API_ICI"
  }
  ```
- Les bibliothèques Python suivantes :
  - requests
  - shutil (module standard)
  - glob (module standard)
  - json (module standard)
  - os (module standard)

## Installation

Tout d'abord, installez la bibliothèque OpenAI (nécessaire pour certaines fonctionnalités ou interactions futures) en utilisant pip :

```bash
pip install openai
```

pip install --upgrade openai

Installez également la bibliothèque Requests si elle n'est pas déjà installée :

```bash
pip install requests
```

## Utilisation

1. Configurez votre fichier `config.json` avec votre clé API.
2. Exécutez le script dans votre terminal :

```bash
python gpt-image-1_api_image_generator.py
```

3. Saisissez le prompt correspondant à l'image que vous souhaitez générer quand il vous le demande.

L'image générée sera téléchargée sous le nom `IMG_XXXX.png`. Si ce fichier existe déjà, il sera archivé automatiquement en le copiant sous un nouveau nom avec un indice incrémenté (par exemple `IMG_0001.png`, `IMG_0002.png`, etc.) avant d'être écrasé.

## À propos du Code

- `load_config()` : Charge la configuration depuis le fichier `config.json`.
- `archive_current_image_copy()` : Archive l'image existante avant de télécharger une nouvelle image.
- `generate_image(prompt)` : Envoie une requête à l'API avec le prompt fourni, puis télécharge et sauvegarde l'image générée.

## Remarques

- Assurez-vous que votre connexion Internet fonctionne correctement pour interagir avec l'API.
- Ce script est un exemple simple et peut être adapté ou étendu en fonction de vos besoins.
