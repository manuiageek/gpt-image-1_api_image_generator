import os
import glob
import json
import shutil
import base64
from openai import OpenAI

# Chargement de la configuration depuis config.json
def load_config():
    config_file = "config.json"
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Le fichier de configuration '{config_file}' est introuvable.")
    with open(config_file, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

API_KEY = config.get("api_key")
if not API_KEY:
    raise ValueError("La clé API n'a pas été trouvée dans le fichier de configuration.")

client = OpenAI(api_key=API_KEY)

def archive_current_image_copy():
    current_file = "IMG_XXXX.png"
    if not os.path.exists(current_file):
        return

    archives = glob.glob("IMG_[0-9][0-9][0-9][0-9].png")
    max_index = 0
    for file in archives:
        try:
            index = int(os.path.splitext(os.path.basename(file))[0].split("_")[1])
            if index > max_index:
                max_index = index
        except (IndexError, ValueError):
            continue

    new_index = max_index + 1
    new_name = f"IMG_{new_index:04d}.png"
    shutil.copyfile(current_file, new_name)

def generate_image(prompt):
    print(f"En cours, avec le prompt : {prompt}")
    try:
        archive_current_image_copy()
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="medium",
            moderation="low"
        )
        # Selon la version, accès direct à b64_json
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        with open("IMG_XXXX.png", "wb") as img_file:
            img_file.write(image_bytes)
        print("L'image a été téléchargée et sauvegardée sous 'IMG_XXXX.png'.")
    except Exception as e:
        print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    user_prompt = input("Que voulez-vous générer ? :\n")
    generate_image(user_prompt)