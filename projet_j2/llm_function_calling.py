import json
import subprocess
import os
import time
import requests
import base64
from typing import Dict, Any, List
from dotenv import load_dotenv
from mistralai import Mistral
from bs4 import BeautifulSoup
from PIL import Image

load_dotenv()

api_key = os.environ["MISTRAL_API_KEY"]
client = Mistral(api_key=api_key)

def generateText(prompt: str, force_json: bool = False, conversation_history: List[Dict] = None) -> str:
    """
    Fonction qui prend en entrée un prompt et envoie la requête à Mistral via leur SDK.
    
    Args:
        prompt (str): Le prompt à envoyer au LLM
        force_json (bool): Si True, force le format JSON en sortie
        conversation_history (List[Dict]): Historique de la conversation
        
    Returns:
        str: La réponse du LLM
    """
    messages = []
    
    if conversation_history:
        messages.extend(conversation_history)
    
    messages.append({"role": "user", "content": prompt})
    
    try:
        kwargs = {
            "model": "mistral-small-latest",
            "messages": messages,
            "max_tokens": 8000,
            "temperature": 0.7
        }
        
        if force_json:
            kwargs["response_format"] = {"type": "json_object"}
        
        response = client.chat.complete(**kwargs)
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Erreur lors de l'appel à l'API Mistral: {e}"


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


def choose_tool(context: str) -> str:
    """
    Fonction pour demander au LLM de choisir le prochain outil à utiliser.
    
    Args:
        context (str): Le contexte actuel de la tâche
        
    Returns:
        str: Le nom de l'outil choisi ou des informations sur la décision
    """
    return f"Outil sélectionné basé sur le contexte: {context}"


def stop(reason: str = "Tâche terminée") -> Dict[str, Any]:
    """
    Fonction pour arrêter le processus d'itération.
    
    Args:
        reason (str): La raison de l'arrêt
        
    Returns:
        Dict: Informations sur l'arrêt
    """
    return {
        "action": "stop",
        "reason": reason,
        "timestamp": time.time() if 'time' in globals() else None
    }


def listFiles(directory: str = ".") -> Dict[str, Any]:
    """
    Liste les fichiers et dossiers d'un répertoire.
    
    Args:
        directory (str): Le répertoire à explorer (par défaut le répertoire courant)
        
    Returns:
        Dict: Informations sur les fichiers et dossiers
    """
    try:
        files = []
        directories = []
        
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files.append({
                    "name": item,
                    "path": item_path,
                    "size": size,
                    "extension": os.path.splitext(item)[1]
                })
            elif os.path.isdir(item_path):
                directories.append({
                    "name": item,
                    "path": item_path
                })
        
        return {
            "success": True,
            "directory": directory,
            "files": files,
            "directories": directories,
            "total_files": len(files),
            "total_directories": len(directories)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors de la lecture du répertoire {directory}: {e}"
        }


def readFile(file_path: str) -> Dict[str, Any]:
    """
    Lit le contenu d'un fichier existant.
    
    Args:
        file_path (str): Le chemin du fichier à lire
        
    Returns:
        Dict: Le contenu du fichier et ses métadonnées
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        file_stats = os.stat(file_path)
        
        return {
            "success": True,
            "file_path": file_path,
            "content": content,
            "lines": len(content.split('\n')),
            "size": file_stats.st_size,
            "extension": os.path.splitext(file_path)[1]
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors de la lecture du fichier {file_path}: {e}"
        }


def runTests(test_path: str = "test_*.py") -> Dict[str, Any]:
    """
    Exécute des tests unitaires avec pytest.
    
    Args:
        test_path (str): Le chemin ou pattern des fichiers de test
        
    Returns:
        Dict: Résultat de l'exécution des tests
    """
    try:
        result = subprocess.run(['python', '-m', 'pytest', test_path, '-v'], 
                              capture_output=True, 
                              text=True)
        
        return {
            "success": result.returncode == 0,
            "return_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "test_path": test_path
        }
    except FileNotFoundError:
        return {
            "success": False,
            "error": "pytest n'est pas installé. Installez-le avec: pip install pytest"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors de l'exécution des tests: {e}"
        }


def webScraping(url: str, selector: str = None) -> Dict[str, Any]:
    """
    Effectue du web scraping sur une URL donnée.
    
    Args:
        url (str): L'URL à scraper
        selector (str): Sélecteur CSS optionnel pour extraire des éléments spécifiques
        
    Returns:
        Dict: Données scrapées
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        if selector:
            elements = soup.select(selector)
            data = [elem.get_text(strip=True) for elem in elements]
        else:
            data = {
                "title": soup.title.string if soup.title else "Pas de titre",
                "text_content": soup.get_text()[:1000],  # Premier 1000 caractères
                "links": [a.get('href') for a in soup.find_all('a', href=True)[:10]]
            }
        
        return {
            "success": True,
            "url": url,
            "data": data,
            "status_code": response.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors du scraping de {url}: {e}"
        }


def analyzeImage(image_path: str, prompt: str = "Décris cette image en détail") -> Dict[str, Any]:
    """
    Analyse une image avec le modèle vision Pixtral de Mistral.
    
    Args:
        image_path (str): Le chemin vers l'image à analyser
        prompt (str): La question/prompt pour l'analyse
        
    Returns:
        Dict: Résultat de l'analyse de l'image
    """
    try:
        # Vérifier que le fichier image existe
        if not os.path.exists(image_path):
            return {
                "success": False,
                "error": f"Image non trouvée: {image_path}"
            }
        
        # Encoder l'image en base64
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Préparer les messages pour Pixtral
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": f"data:image/jpeg;base64,{encoded_image}"
                    }
                ]
            }
        ]
        
        # Appel à Pixtral (modèle vision de Mistral)
        response = client.chat.complete(
            model="pixtral-12b-2409",
            messages=messages,
            max_tokens=1000
        )
        
        return {
            "success": True,
            "image_path": image_path,
            "prompt": prompt,
            "analysis": response.choices[0].message.content
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors de l'analyse de l'image {image_path}: {e}"
        }


def iterative_function_calling_system(user_request: str, max_iterations: int = 5) -> Dict[str, Any]:
    """
    Système de function calling itératif avec feedback et choix d'outils.
    
    Args:
        user_request (str): La demande initiale de l'utilisateur
        max_iterations (int): Nombre maximum d'itérations
        
    Returns:
        Dict: Résultat final avec historique des actions
    """
    conversation_history = []
    task_results = []
    iteration = 0
    
    print(f"🚀 Démarrage du système itératif pour: {user_request}")
    print(f"📊 Maximum {max_iterations} itérations autorisées")
    
    while iteration < max_iterations:
        iteration += 1
        print(f"\n{'='*60}")
        print(f"🔄 ITÉRATION {iteration}/{max_iterations}")
        print(f"{'='*60}")
        
        context = build_iteration_context(user_request, conversation_history, task_results, iteration)
        
        action_result = choose_next_action(context)
        
        if not action_result.get("success"):
            print(f"❌ Erreur dans le choix d'action: {action_result.get('error')}")
            break
            
        chosen_action = action_result.get("action")
        action_args = action_result.get("arguments", {})
        
        print(f"🎯 Action choisie: {chosen_action}")
        print(f"📋 Arguments: {action_args}")
        
        if chosen_action == "stop":
            print(f"🛑 Arrêt demandé: {action_args.get('reason', 'Tâche terminée')}")
            break
            
        elif chosen_action == "writeFile":
            result = writeFile(action_args.get("path"), action_args.get("content"))
            execution_result = {
                "success": result,
                "action": chosen_action,
                "details": f"Fichier {'créé' if result else 'non créé'}: {action_args.get('path')}"
            }
            
        elif chosen_action == "launchPythonFile":
            result = launchPythonFile(action_args.get("path"))
            execution_result = {
                "success": True,
                "action": chosen_action,
                "details": result
            }
            
        elif chosen_action == "listFiles":
            result = listFiles(action_args.get("directory", "."))
            execution_result = {
                "success": result.get("success", False),
                "action": chosen_action,
                "details": f"Listage {'réussi' if result.get('success') else 'échoué'}: {result.get('total_files', 0)} fichiers, {result.get('total_directories', 0)} dossiers" if result.get("success") else result.get("error")
            }
            
        elif chosen_action == "readFile":
            result = readFile(action_args.get("file_path"))
            execution_result = {
                "success": result.get("success", False),
                "action": chosen_action,
                "details": f"Lecture {'réussie' if result.get('success') else 'échouée'}: {result.get('lines', 0)} lignes" if result.get("success") else result.get("error")
            }
            
        elif chosen_action == "runTests":
            result = runTests(action_args.get("test_path", "test_*.py"))
            execution_result = {
                "success": result.get("success", False),
                "action": chosen_action,
                "details": f"Tests {'réussis' if result.get('success') else 'échoués'}: {result.get('stdout', result.get('stderr', ''))[:200]}"
            }
            
        elif chosen_action == "webScraping":
            result = webScraping(action_args.get("url"), action_args.get("selector"))
            execution_result = {
                "success": result.get("success", False),
                "action": chosen_action,
                "details": f"Scraping {'réussi' if result.get('success') else 'échoué'}: {action_args.get('url')}" if result.get("success") else result.get("error")
            }
            
        elif chosen_action == "analyzeImage":
            result = analyzeImage(action_args.get("image_path"), action_args.get("prompt", "Décris cette image"))
            execution_result = {
                "success": result.get("success", False),
                "action": chosen_action,
                "details": f"Analyse {'réussie' if result.get('success') else 'échouée'}: {action_args.get('image_path')}" if result.get("success") else result.get("error")
            }
            
        elif chosen_action == "choose_tool":
            result = choose_tool(action_args.get("context", ""))
            execution_result = {
                "success": True,
                "action": chosen_action,
                "details": result
            }
            
        else:
            execution_result = {
                "success": False,
                "action": chosen_action,
                "details": f"Action inconnue: {chosen_action}"
            }
        
        task_results.append(execution_result)
        conversation_history.append({
            "iteration": iteration,
            "user_request": user_request if iteration == 1 else "continuation",
            "chosen_action": chosen_action,
            "execution_result": execution_result
        })
        
        print(f"✅ Résultat: {execution_result.get('details')}")
        
        if execution_result.get("success") and chosen_action in ["writeFile", "launchPythonFile", "runTests"]:
            feedback = get_feedback(execution_result, user_request, iteration)
            if feedback.get("should_continue", True):
                print(f"💭 Feedback: {feedback.get('message', 'Continuation...')}")
            else:
                print(f"✨ Feedback: {feedback.get('message', 'Tâche accomplie!')}")
                break
    
    final_result = {
        "success": True,
        "total_iterations": iteration,
        "final_status": "completed" if iteration <= max_iterations else "max_iterations_reached",
        "conversation_history": conversation_history,
        "task_results": task_results,
        "user_request": user_request
    }
    
    print(f"\n🏁 RÉSULTAT FINAL")
    print(f"📊 {iteration} itérations effectuées")
    print(f"✅ Statut: {final_result['final_status']}")
    
    return final_result


def build_iteration_context(user_request: str, history: List, results: List, iteration: int) -> str:
    """Construit le contexte pour une itération donnée"""
    context = f"""
DEMANDE UTILISATEUR INITIALE: {user_request}

ITÉRATION ACTUELLE: {iteration}

HISTORIQUE DES ACTIONS:
"""
    
    for i, entry in enumerate(history, 1):
        context += f"{i}. Action: {entry['chosen_action']} - Résultat: {entry['execution_result']['details']}\n"
    
    if not history:
        context += "Aucune action précédente.\n"
    
    context += f"""
TÂCHES DISPONIBLES:
1. writeFile(path, content) - Écrire du contenu dans un fichier
2. launchPythonFile(path) - Exécuter un fichier Python
3. listFiles(directory) - Lister les fichiers d'un répertoire
4. readFile(file_path) - Lire le contenu d'un fichier existant
5. runTests(test_path) - Exécuter des tests unitaires avec pytest
6. webScraping(url, selector) - Faire du web scraping
7. analyzeImage(image_path, prompt) - Analyser une image avec Pixtral
8. stop(reason) - Arrêter le processus

Analysez la situation et choisissez la prochaine action appropriée.
"""
    
    return context


def choose_next_action(context: str) -> Dict[str, Any]:
    """Demande au LLM de choisir la prochaine action"""
    prompt = f"""
{context}

RÈGLES LOGIQUES À SUIVRE :
1. Si un fichier doit être créé ET exécuté : d'abord writeFile, puis launchPythonFile
2. Si un fichier existe déjà et doit être exécuté : utiliser launchPythonFile
3. Ne PAS recréer un fichier qui vient d'être créé avec succès
4. Si la tâche est accomplie, utiliser stop

Répondez UNIQUEMENT avec un JSON valide:

{{
    "action": "nom_de_l_action",
    "arguments": {{
        "param1": "valeur1",
        "param2": "valeur2"
    }},
    "reasoning": "Explication de votre choix"
}}

Actions possibles:
- writeFile: pour créer/modifier un fichier (uniquement si pas encore créé)
- launchPythonFile: pour exécuter un script Python (après création)
- listFiles: pour explorer les fichiers du projet (utile pour comprendre la structure)
- readFile: pour lire le contenu d'un fichier existant (avant modification)
- runTests: pour exécuter des tests unitaires avec pytest (vérifier que le code marche)
- webScraping: pour extraire des données depuis une URL
- analyzeImage: pour analyser des images avec l'IA vision Pixtral
- stop: pour terminer le processus quand tout est fait

RÈGLES SPÉCIALES POUR LES TESTS:
- Si vous créez du code, créez AUSSI les tests unitaires
- Utilisez runTests après création de tests pour vérifier que tout fonctionne
- Nommez les fichiers de test avec le préfixe 'test_'

Analysez l'historique pour voir ce qui a déjà été fait et choisissez la PROCHAINE étape logique.
"""
    
    try:
        print(f"🔍 Envoi du prompt au LLM...")
        response = generateText(prompt, force_json=True)
        print(f"📝 Réponse brute du LLM: '{response}'")
        
        if not response or response.strip() == "":
            print(f"⚠️ Réponse vide du LLM")
            return {
                "success": False,
                "error": "Réponse vide du LLM"
            }
            
        # Nettoyer la réponse au cas où il y aurait des caractères parasites
        response = response.strip()
        if response.startswith("```json"):
            response = response[7:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        print(f"🧹 Réponse nettoyée: '{response}'")
        
        action_data = json.loads(response)
        
        return {
            "success": True,
            "action": action_data.get("action"),
            "arguments": action_data.get("arguments", {}),
            "reasoning": action_data.get("reasoning", "")
        }
    except json.JSONDecodeError as e:
        print(f"❌ Erreur JSON: {e}")
        print(f"❌ Réponse problématique: '{response}'")
        return {
            "success": False,
            "error": f"Erreur JSON: {e} - Réponse: '{response[:100]}'"
        }
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
        return {
            "success": False,
            "error": f"Erreur lors du choix d'action: {e}"
        }


def get_feedback(execution_result: Dict, user_request: str, iteration: int) -> Dict[str, Any]:
    """Obtient un feedback simplifié basé sur la logique"""
    action = execution_result.get('action')
    success = execution_result.get('success')
    
    # Analyse simple : si création réussie et demande d'exécution, alors continuer
    if action == "writeFile" and success:
        if "execute" in user_request.lower() or "exécute" in user_request.lower():
            return {
                "should_continue": True,
                "message": "Fichier créé avec succès. Prochaine étape : exécuter le fichier.",
                "confidence": 0.9
            }
        elif "test" in user_request.lower():
            return {
                "should_continue": True,
                "message": "Code créé avec succès. Prochaine étape : créer et exécuter les tests.",
                "confidence": 0.9
            }
        else:
            return {
                "should_continue": False,
                "message": "Fichier créé avec succès. Tâche accomplie.",
                "confidence": 0.9
            }
    
    # Si exécution réussie, arrêter sauf si tests demandés
    elif action == "launchPythonFile" and success:
        if "test" in user_request.lower():
            return {
                "should_continue": True,
                "message": "Code exécuté avec succès. Prochaine étape : créer les tests unitaires.",
                "confidence": 0.9
            }
        else:
            return {
                "should_continue": False,
                "message": "Fichier exécuté avec succès. Tâche accomplie.",
                "confidence": 0.9
            }
    
    # Si tests exécutés avec succès, arrêter
    elif action == "runTests" and success:
        return {
            "should_continue": False,
            "message": "Tests exécutés avec succès. Code vérifié et validé !",
            "confidence": 0.9
        }
    
    # Si échec, continuer pour réessayer
    elif not success:
        return {
            "should_continue": True,
            "message": f"Échec de l'action {action}. Réessayer.",
            "confidence": 0.7
        }
    
    # Par défaut, arrêter après quelques itérations
    else:
        return {
            "should_continue": iteration < 2,
            "message": "Action terminée.",
            "confidence": 0.5
        }


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
    
    llm_response = generateText(function_calling_prompt, force_json=True)
    print(f"Réponse du LLM: {llm_response}")
    
    try:
        function_call = json.loads(llm_response)
        function_name = function_call.get("function_name")
        arguments = function_call.get("arguments", {})
        
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
    print("✅") 