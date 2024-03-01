import os
import requests
import subprocess
import unicodedata
import re
from pathlib import Path
import yaml

# Configuration et définition des constantes
API_KEY = 'YOUR API KEY'
API_URL = "https://api.openai.com/v1/chat/completions"
HEADERS = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}
PROJECT_DIRECTORY = 'YOUR DEFAULT BLOG FOLDER'
DEFAULT_TAGS = ['other']
DEFAULT_CATEGORY = "Other"

def clean_title(title):
    title_no_accents = ''.join(c for c in unicodedata.normalize('NFD', title) if unicodedata.category(c) != 'Mn')
    title_cleaned = re.sub(r'[^a-zA-Z0-9\s-]', '', title_no_accents)
    title_cleaned = re.sub(r'\s+', '-', title_cleaned)
    return title_cleaned.lower()

def generate_content(prompt):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=HEADERS, json=data)
    result = response.json()
    return result.get('choices')[0]['message']['content'] if result.get('choices') else None

def update_article(article_path, content, new_tags=None, category=None):
    if new_tags is None:
        new_tags = DEFAULT_TAGS
    if category is None:
        category = DEFAULT_CATEGORY

    article_file = Path(article_path)
    if not article_file.exists():
        print(f"Le fichier {article_path} n'existe pas.")
        return False

    original_content = article_file.read_text()
    end_of_yaml_index = original_content.find('---', 3)
    yaml_content = original_content[:end_of_yaml_index].strip()
    yaml_dict = yaml.safe_load(yaml_content)
    yaml_dict['tags'] = new_tags
    yaml_dict['categories'] = [category]
    updated_yaml = yaml.dump(yaml_dict, sort_keys=False)
    updated_content = '---\n' + updated_yaml + '---\n' + content
    article_file.write_text(updated_content)
    return True

def create_and_publish_article(project_directory, sujet, tags=None, category=None, blog_type='Hexo'):
    if tags is None:
        tags = DEFAULT_TAGS
    if category is None:
        category = DEFAULT_CATEGORY
    print(category)
    os.chdir(project_directory)
    title = clean_title(sujet)
    article_title = sujet  # Titre de l'article pour Hexo ou Jekyll

    # Création du prompt pour l'IA
    prompt = (
        f"Génère un article pédagogique pour débutants en {category}, structuré au format Markdown, "
        f"traitant de ce sujet {category} : {sujet}. "
        f"L'article doit inclure toutes les sections nécessaires pour devenir connaisseur sur le {sujet} "
        f"Le style doit être léger mais rigoureux, "
        f"adapté à un blog éducatif. Inclure des exemples pour illustrer chaque "
        f"concept, et expliquer chaque étape clairement. La conclusion doit ouvrir sur les applications"
        f"possible de {sujet}. Utilise le langage Markdown efficacement "
        f"pour améliorer la lisibilité et la mise en page, en utilisant des titres, sous-titres, "
        f"listes, blocs de code, et liens. La conclusion doit être sobre. Assure-toi que le contenu "
        f"est cohérent, bien structuré et que le "
        f"Markdown est correctement utilisé."
        )

    # Création de l'article avec Hexo ou Jekyll
    subprocess.run(['hexo', 'new', article_title], check=True)
    posts_directory = Path(project_directory) / 'source' / '_posts'
    latest_file = max(posts_directory.glob('*.md'), key=os.path.getctime)
    article_path = str(latest_file)

    # Génération du contenu avec OpenAI
    content = generate_content(prompt)
    if content is None:
        raise Exception("La génération de contenu par OpenAI a échoué.")

    # Mise à jour de l'article
    update_success = update_article(article_path, content, tags, category)
    if not update_success:
        return False

    # Génération et déploiement du site
    subprocess.run(['hexo', 'clean'], check=True)
    subprocess.run(['hexo', 'generate'], check=True)

    return True


def deploy():
    subprocess.run(['hexo', 'deploy'], check=True)

def titles_generation(number,category):

    prompt = (
        f"Je vais créer une série d'articles pédagogique sur {category}."
        f"Divise le sujet en {number} chapitres d'introduction qui passe en vue tous les sujets nécessaire pour devenir expert."
        f"fournit cette liste directement en texte, non numéroté, sans autre commentaire"
    )

    # Génération du contenu avec OpenAI
    content = generate_content(prompt)
    if content is None:
        raise Exception("La génération de contenu par OpenAI a échoué.")
    else:
        return(content)
