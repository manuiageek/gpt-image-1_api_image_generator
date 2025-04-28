import os
import glob
import json
import shutil
import base64
from openai import OpenAI

# Chemin du dossier images
IMAGES_DIR = "IMAGES"
os.makedirs(IMAGES_DIR, exist_ok=True)

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
    current_file = os.path.join(IMAGES_DIR, "IMG_XXXX.png")
    if not os.path.exists(current_file):
        return

    archives = glob.glob(os.path.join(IMAGES_DIR, "IMG_[0-9][0-9][0-9][0-9].png"))
    max_index = 0
    for file in archives:
        try:
            index = int(os.path.splitext(os.path.basename(file))[0].split("_")[1])
            if index > max_index:
                max_index = index
        except (IndexError, ValueError):
            continue

    new_index = max_index + 1
    new_name = os.path.join(IMAGES_DIR, f"IMG_{new_index:04d}.png")
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
            quality="high",
            moderation="low"
        )
        image_base64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_base64)
        output_path = os.path.join(IMAGES_DIR, "IMG_XXXX.png")
        with open(output_path, "wb") as img_file:
            img_file.write(image_bytes)
        print(f"L'image a été téléchargée et sauvegardée sous '{output_path}'.")
    except Exception as e:
        print("Une erreur s'est produite :", e)

if __name__ == "__main__":
    prompt_file = "your_prompt.txt"
    if not os.path.exists(prompt_file):
        print(f"Le fichier '{prompt_file}' est introuvable.")
    else:
        with open(prompt_file, "r", encoding="utf-8") as f:
            user_prompt = f.read().strip()
        generate_image(user_prompt)