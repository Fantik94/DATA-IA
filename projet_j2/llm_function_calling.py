import requests
import json
import subprocess
import os
from typing import Dict, Any

MISTRAL_API_KEY = "OHgvSY6RrhHNkTY1M3RQ7ici0iLuDwPv"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def generateText(prompt: str) -> str:
    """
    Fonction qui prend en entrée un prompt et envoie la requête à Mistral via leur API.
    
    Args:
        prompt (str): Le prompt à envoyer au LLM
        
    Returns:
        str: La réponse du LLM
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "mistral-small-latest",
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(MISTRAL_API_URL, headers=headers, json=data)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
        
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la requête à l'API Mistral: {e}"
    except KeyError as e:
        return f"Erreur lors du parsing de la réponse: {e}"
    except Exception as e:
        return f"Erreur inattendue: {e}"


def writeFile(path: str, content: str) -> bool:
    """
    Fonction pour écrire du contenu dans un fichier.
    
    Args:
        path (str): Le chemin du fichier à créer
        content (str): Le contenu à écrire
        
    Returns:
        bool: True si le fichier a été créé avec succès, False sinon
    """
    try:
        directory = os.path.dirname(path)
        if directory:  # Seulement si le répertoire n'est pas vide
            os.makedirs(directory, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fichier créé avec succès: {path}")
        return True
    except Exception as e:
        print(f"Erreur lors de la création du fichier {path}: {e}")
        return False


def launchPythonFile(path: str) -> str:
    """
    Fonction pour exécuter un fichier Python.
    
    Args:
        path (str): Le chemin du fichier Python à exécuter
        
    Returns:
        str: La sortie du programme ou un message d'erreur
    """
    try:
        result = subprocess.run(['python', path], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        return f"Exécution réussie:\n{result.stdout}"
    except subprocess.CalledProcessError as e:
        return f"Erreur lors de l'exécution: {e.stderr}"
    except FileNotFoundError:
        return f"Fichier non trouvé: {path}"
    except Exception as e:
        return f"Erreur inattendue: {e}"


def function_calling_system(user_request: str) -> Dict[str, Any]:
    """
    Système de function calling qui demande au LLM de choisir une fonction à exécuter.
    
    Args:
        user_request (str): La demande de l'utilisateur
        
    Returns:
        Dict: Résultat de l'exécution de la fonction
    """
    function_calling_prompt = f"""
Tu es un assistant qui peut exécuter des fonctions. Tu as accès aux fonctions suivantes:

1. writeFile(path, content) - Écrit du contenu dans un fichier
   - path: le chemin du fichier (str)
   - content: le contenu à écrire (str)

2. launchPythonFile(path) - Exécute un fichier Python
   - path: le chemin du fichier Python (str)

Demande de l'utilisateur: {user_request}

Réponds UNIQUEMENT avec un JSON valide dans ce format:
{{
    "function_name": "nom_de_la_fonction",
    "arguments": {{
        "param1": "valeur1",
        "param2": "valeur2"
    }}
}}

Si aucune fonction n'est appropriée, réponds avec:
{{
    "function_name": "none",
    "arguments": {{}}
}}
"""
    
    # Obtenir la réponse du LLM
    llm_response = generateText(function_calling_prompt)
    print(f"Réponse du LLM: {llm_response}")
    
    try:
        # Nettoyer la réponse pour enlever les balises markdown si présentes
        clean_response = llm_response.strip()
        if clean_response.startswith("```json"):
            clean_response = clean_response[7:]  # Enlever ```json
        if clean_response.endswith("```"):
            clean_response = clean_response[:-3]  # Enlever ```
        clean_response = clean_response.strip()
        
        # Parser la réponse JSON
        function_call = json.loads(clean_response)
        function_name = function_call.get("function_name")
        arguments = function_call.get("arguments", {})
        
        # Exécuter la fonction demandée
        if function_name == "writeFile":
            path = arguments.get("path")
            content = arguments.get("content")
            if path and content:
                success = writeFile(path, content)
                return {
                    "success": success,
                    "function": function_name,
                    "arguments": arguments,
                    "result": f"Fichier {'créé' if success else 'non créé'}: {path}"
                }
            else:
                return {
                    "success": False,
                    "error": "Arguments manquants pour writeFile (path, content)"
                }
        
        elif function_name == "launchPythonFile":
            path = arguments.get("path")
            if path:
                result = launchPythonFile(path)
                return {
                    "success": True,
                    "function": function_name,
                    "arguments": arguments,
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": "Argument manquant pour launchPythonFile (path)"
                }
        
        elif function_name == "none":
            return {
                "success": True,
                "function": "none",
                "result": "Aucune fonction à exécuter"
            }
        
        else:
            return {
                "success": False,
                "error": f"Fonction inconnue: {function_name}"
            }
            
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"Erreur lors du parsing JSON: {e}",
            "raw_response": llm_response
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur inattendue: {e}"
        }


def test_generateText():
    """Test de la fonction generateText"""
    print("=== Test de la fonction generateText ===")
    
    test_prompt = "Bonjour ! Peux-tu me dire une phrase simple pour tester ton fonctionnement ?"
    response = generateText(test_prompt)
    
    print(f"Prompt: {test_prompt}")
    print(f"Réponse: {response}")
    print()


def test_hello_world():
    """Test du function calling pour créer un fichier hello world"""
    print("=== Test du function calling - Hello World ===")
    
    user_request = "Écris un fichier Python appelé 'hello_world.py' qui contient un simple print('Hello World')"
    
    result = function_calling_system(user_request)
    print(f"Résultat: {json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # Si le fichier a été créé, essayons de l'exécuter
    if result.get("success") and result.get("function") == "writeFile":
        print("\n=== Test d'exécution du fichier créé ===")
        exec_result = function_calling_system("Exécute le fichier hello_world.py")
        print(f"Résultat d'exécution: {json.dumps(exec_result, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    print("🚀 Démarrage du projet LLM Function Calling avec Mistral")
    print("=" * 60)
    
    # Test 1: Fonction generateText
    test_generateText()
    
    # Test 2: Function calling pour Hello World
    test_hello_world()
    
    print("=" * 60)
    print("✅ Tests terminés !") 