import requests
import json
import subprocess
import os
import time
from typing import Dict, Any, List

MISTRAL_API_KEY = "OHgvSY6RrhHNkTY1M3RQ7ici0iLuDwPv"
MISTRAL_API_URL = "https://api.mistral.ai/v1/chat/completions"

def generateText(prompt: str, force_json: bool = False, conversation_history: List[Dict] = None) -> str:
    """
    Fonction qui prend en entrée un prompt et envoie la requête à Mistral via leur API.
    
    Args:
        prompt (str): Le prompt à envoyer au LLM
        force_json (bool): Si True, force le format JSON en sortie
        conversation_history (List[Dict]): Historique de la conversation
        
    Returns:
        str: La réponse du LLM
    """
    headers = {
        "Authorization": f"Bearer {MISTRAL_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Construire les messages avec l'historique
    messages = []
    
    # Ajouter l'historique s'il existe
    if conversation_history:
        messages.extend(conversation_history)
    
    # Ajouter le message actuel
    messages.append({
        "role": "user", 
        "content": prompt
    })
    
    data = {
        "model": "mistral-small-latest",
        "messages": messages,
        "max_tokens": 8000,  # Tokens augmentés pour des réponses plus longues
        "temperature": 0.7
    }
    
    # Ajouter le format JSON seulement si demandé
    if force_json:
        data["response_format"] = {
            "type": "json_object"
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
        
        # Construire le contexte pour cette itération
        context = build_iteration_context(user_request, conversation_history, task_results, iteration)
        
        # Demander au LLM de choisir la prochaine action
        action_result = choose_next_action(context)
        
        if not action_result.get("success"):
            print(f"❌ Erreur dans le choix d'action: {action_result.get('error')}")
            break
            
        chosen_action = action_result.get("action")
        action_args = action_result.get("arguments", {})
        
        print(f"🎯 Action choisie: {chosen_action}")
        print(f"📋 Arguments: {action_args}")
        
        # Exécuter l'action choisie
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
        
        # Enregistrer les résultats
        task_results.append(execution_result)
        conversation_history.append({
            "iteration": iteration,
            "user_request": user_request if iteration == 1 else "continuation",
            "chosen_action": chosen_action,
            "execution_result": execution_result
        })
        
        print(f"✅ Résultat: {execution_result.get('details')}")
        
        # Évaluer si on doit continuer
        if execution_result.get("success") and chosen_action in ["writeFile", "launchPythonFile"]:
            # Demander un feedback au LLM sur le résultat
            feedback = get_feedback(execution_result, user_request, iteration)
            if feedback.get("should_continue", True):
                print(f"💭 Feedback: {feedback.get('message', 'Continuation...')}")
            else:
                print(f"✨ Feedback: {feedback.get('message', 'Tâche accomplie!')}")
                break
    
    # Résultat final
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
3. choose_tool(context) - Choisir un outil spécifique
4. stop(reason) - Arrêter le processus

Analysez la situation et choisissez la prochaine action appropriée.
"""
    
    return context


def choose_next_action(context: str) -> Dict[str, Any]:
    """Demande au LLM de choisir la prochaine action"""
    prompt = f"""
{context}

Vous devez choisir la prochaine action à effectuer. Répondez UNIQUEMENT avec un JSON valide:

{{
    "action": "nom_de_l_action",
    "arguments": {{
        "param1": "valeur1",
        "param2": "valeur2"
    }},
    "reasoning": "Explication de votre choix"
}}

Actions possibles:
- writeFile: pour créer/modifier un fichier
- launchPythonFile: pour exécuter un script Python
- choose_tool: pour sélectionner un outil spécifique
- stop: pour terminer le processus

Choisissez intelligemment en fonction du contexte et de l'objectif.
"""
    
    try:
        response = generateText(prompt, force_json=True)
        action_data = json.loads(response)
        
        return {
            "success": True,
            "action": action_data.get("action"),
            "arguments": action_data.get("arguments", {}),
            "reasoning": action_data.get("reasoning", "")
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Erreur lors du choix d'action: {e}"
        }


def get_feedback(execution_result: Dict, user_request: str, iteration: int) -> Dict[str, Any]:
    """Obtient un feedback du LLM sur le résultat d'une action"""
    prompt = f"""
DEMANDE UTILISATEUR: {user_request}
ITÉRATION: {iteration}
ACTION EXÉCUTÉE: {execution_result.get('action')}
RÉSULTAT: {execution_result.get('details')}

Évaluez si cette action a bien progressé vers l'objectif de l'utilisateur.
Répondez UNIQUEMENT avec un JSON valide:

{{
    "should_continue": true/false,
    "message": "Votre évaluation et recommandation",
    "confidence": 0.8
}}

Si should_continue est false, cela signifie que la tâche est accomplie.
Si true, donnez des suggestions pour l'amélioration.
"""
    
    try:
        response = generateText(prompt, force_json=True)
        feedback_data = json.loads(response)
        
        return {
            "should_continue": feedback_data.get("should_continue", True),
            "message": feedback_data.get("message", ""),
            "confidence": feedback_data.get("confidence", 0.5)
        }
    except Exception as e:
        return {
            "should_continue": False,
            "message": f"Erreur feedback: {e}",
            "confidence": 0.0
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
    
    # Obtenir la réponse du LLM en format JSON natif
    llm_response = generateText(function_calling_prompt, force_json=True)
    print(f"Réponse du LLM: {llm_response}")
    
    try:
        # Parser directement la réponse JSON (plus de nettoyage nécessaire !)
        function_call = json.loads(llm_response)
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
    print("✅") 