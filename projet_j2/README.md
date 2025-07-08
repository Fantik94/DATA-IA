# Projet Jour 2 - LLM Function Calling avec Mistral

Ce projet implémente l'utilisation d'un LLM via API et un système de function calling avec l'API Mistral.

## Fonctionnalités

### A. Utilisation d'un LLM via API

- **`generateText(prompt: str) -> str`** : Fonction qui envoie un prompt à l'API Mistral et retourne la réponse

### B. Function Calling

- **`writeFile(path: str, content: str) -> bool`** : Écrit du contenu dans un fichier
- **`launchPythonFile(path: str) -> str`** : Exécute un fichier Python
- **`function_calling_system(user_request: str) -> Dict`** : Système qui demande au LLM de choisir et exécuter une fonction

## Installation

1. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Test complet
```bash
python llm_function_calling.py
```

### Utilisation des fonctions individuelles

```python
from llm_function_calling import generateText, writeFile, launchPythonFile, function_calling_system

# Test de génération de texte
response = generateText("Bonjour, comment ça va ?")
print(response)

# Écriture d'un fichier
success = writeFile("test.py", "print('Hello')")

# Exécution d'un fichier Python
result = launchPythonFile("test.py")

# Function calling
result = function_calling_system("Crée un fichier Python qui affiche 'Bonjour le monde'")
```

## Structure du projet

- `llm_function_calling.py` : Script principal avec toutes les fonctions
- `requirements.txt` : Dépendances Python
- `hello_world.py` : Fichier exemple créé par le LLM

## Configuration

L'API key Mistral est configurée dans le script. Pour utiliser votre propre clé :

1. Remplacez la valeur de `MISTRAL_API_KEY` dans le script
2. Ou définissez une variable d'environnement `MISTRAL_API_KEY`

## Tests effectués

✅ **Test de generateText** : Fonction opérationnelle, génère du texte via l'API Mistral  
✅ **Test de writeFile** : Crée correctement des fichiers  
✅ **Test de launchPythonFile** : Exécute correctement les scripts Python  
✅ **Test de function calling** : Le LLM choisit et exécute les bonnes fonctions  
✅ **Test Hello World** : Le LLM a créé et exécuté avec succès un fichier "Hello World"

## Résultats

Le système fonctionne parfaitement :
1. Le LLM reçoit une demande en langage naturel
2. Il retourne un JSON avec la fonction à exécuter et ses arguments
3. Le système parse le JSON et exécute la fonction demandée
4. Les résultats sont retournés à l'utilisateur

Exemple de fonctionnement :
- Demande : "Écris un fichier Python qui affiche Hello World"
- LLM retourne : `{"function_name": "writeFile", "arguments": {"path": "hello_world.py", "content": "print('Hello World')"}}`
- Système exécute : `writeFile("hello_world.py", "print('Hello World')")`
- Résultat : Fichier créé et contenu vérifié ✅ 