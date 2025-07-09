import sys
import os
import time
import threading
from llm_function_calling import generateText, function_calling_system, iterative_function_calling_system

class Couleurs:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    ROUGE = '\033[31m'
    VERT = '\033[32m'
    JAUNE = '\033[33m'
    BLEU = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    BLANC = '\033[37m'
    
    ROUGE_VIF = '\033[91m'
    VERT_VIF = '\033[92m'
    JAUNE_VIF = '\033[93m'
    BLEU_VIF = '\033[94m'
    MAGENTA_VIF = '\033[95m'
    CYAN_VIF = '\033[96m'
    
    # Arrière-plans
    BG_NOIR = '\033[40m'
    BG_ROUGE = '\033[41m'
    BG_VERT = '\033[42m'
    BG_JAUNE = '\033[43m'
    BG_BLEU = '\033[44m'

def animation_chargement(message, duree=2):
    """Animation de chargement avec points"""
    def animate():
        for i in range(duree * 4):  
            if i % 4 == 0:
                print(f"\r{Couleurs.CYAN}{message}   {Couleurs.RESET}", end="", flush=True)
            elif i % 4 == 1:
                print(f"\r{Couleurs.CYAN}{message}.  {Couleurs.RESET}", end="", flush=True)
            elif i % 4 == 2:
                print(f"\r{Couleurs.CYAN}{message}.. {Couleurs.RESET}", end="", flush=True)
            else:
                print(f"\r{Couleurs.CYAN}{message}...{Couleurs.RESET}", end="", flush=True)
            time.sleep(0.25)
        print()  
    
    thread = threading.Thread(target=animate)
    thread.daemon = True
    thread.start()
    return thread

def afficher_titre():
    
    titre = [
        "╔══════════════════════════════════════════════════════════╗",
        "║                                                          ║",
        "║     🤖 CHAT INTERACTIF AVEC MISTRAL IA 🚀                ║",
        "║                                                          ║",
        "║     Discutez librement ou utilisez le function calling   ║",
        "║                                                          ║",
        "╚══════════════════════════════════════════════════════════╝"
    ]
    
    for ligne in titre:
        print(f"{Couleurs.CYAN_VIF}{ligne}{Couleurs.RESET}")
        time.sleep(0.1)

def afficher_aide():
    
    print(f"\n{Couleurs.JAUNE_VIF}╔════════════════════════════════════════════════════════════╗{Couleurs.RESET}")
    print(f"{Couleurs.JAUNE_VIF}║                         AIDE                               ║{Couleurs.RESET}")
    print(f"{Couleurs.JAUNE_VIF}╚════════════════════════════════════════════════════════════╝{Couleurs.RESET}")
    
    commandes = [
        ("💡 /aide", "Afficher cette aide"),
        ("🔧 /function", "Activer le mode function calling"),
        ("💬 /normal", "Revenir au mode chat normal"),
        ("🧠 /memoire", "Activer/désactiver la mémoire conversationnelle"),
        ("📜 /historique", "Voir l'historique de la conversation"),
        ("🧹 /clear", "Effacer l'écran et la mémoire"),
        ("🚪 /quit", "Quitter le chat")
    ]
    
    print(f"\n{Couleurs.VERT_VIF}Commandes disponibles :{Couleurs.RESET}")
    for cmd, desc in commandes:
        print(f"  {Couleurs.CYAN}{cmd:<12}{Couleurs.RESET} - {desc}")
    
    print(f"\n{Couleurs.MAGENTA_VIF}🔧 Mode function calling :{Couleurs.RESET}")
    print(f"  {Couleurs.DIM}• Demandez au LLM de créer des fichiers ou d'exécuter du code{Couleurs.RESET}")
    print(f"  {Couleurs.DIM}• Ex: 'Crée un fichier Python qui calcule la factorielle'{Couleurs.RESET}")
    
    print(f"\n{Couleurs.BLEU_VIF}💬 Mode chat normal :{Couleurs.RESET}")
    print(f"  {Couleurs.DIM}• Discussion libre avec le LLM{Couleurs.RESET}")
    print(f"  {Couleurs.DIM}• Posez toutes vos questions !{Couleurs.RESET}")
    
    print(f"\n{Couleurs.JAUNE_VIF}{'═'*60}{Couleurs.RESET}")

def effacer_ecran():
    """Efface l'écran selon l'OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def chat_interactif():
    """Interface de chat interactive avec le LLM"""
    mode_function_calling = False
    conversation_history = [] 
    memoire_active = False  
    
    effacer_ecran()
    afficher_titre()
    
    print(f"\n{Couleurs.VERT_VIF}✨ Bienvenue dans votre assistant IA personnel !{Couleurs.RESET}")
    print(f"{Couleurs.DIM}Tapez {Couleurs.CYAN}/aide{Couleurs.DIM} pour voir les commandes • {Couleurs.CYAN}/quit{Couleurs.DIM} pour quitter{Couleurs.RESET}")
    print(f"{Couleurs.DIM}💡 Astuce: Utilisez {Couleurs.CYAN}/memoire{Couleurs.DIM} pour activer le contexte conversationnel{Couleurs.RESET}")
    print(f"{Couleurs.CYAN_VIF}{'─' * 60}{Couleurs.RESET}")
    
    while True:
        try:
            if mode_function_calling:
                mode_text = f"{Couleurs.MAGENTA_VIF}🔧 FUNCTION{Couleurs.RESET}"
                mode_bg = f"{Couleurs.BG_NOIR}{Couleurs.MAGENTA_VIF}"
            else:
                mode_text = f"{Couleurs.BLEU_VIF}💬 CHAT{Couleurs.RESET}"
                mode_bg = f"{Couleurs.BG_NOIR}{Couleurs.BLEU_VIF}"
            
            memoire_indicator = f"{Couleurs.JAUNE}🧠{Couleurs.RESET}" if memoire_active else f"{Couleurs.DIM}🧠{Couleurs.RESET}"
            
            prompt_user = f"\n{mode_bg} {mode_text} {Couleurs.RESET} {memoire_indicator} {Couleurs.VERT_VIF}Vous:{Couleurs.RESET} "
            
            user_input = input(prompt_user).strip()
            
            if user_input.lower() in ['/quit', '/exit', '/q']:
                print(f"\n{Couleurs.JAUNE_VIF}👋 Au revoir ! Merci d'avoir utilisé le chat interactif.{Couleurs.RESET}")
                print(f"{Couleurs.DIM}À bientôt ! 🚀{Couleurs.RESET}")
                break
            
            elif user_input.lower() in ['/aide', '/help', '/h']:
                afficher_aide()
                continue
            
            elif user_input.lower() == '/function':
                mode_function_calling = True
                print(f"\n{Couleurs.MAGENTA_VIF}🔧 Mode function calling activé !{Couleurs.RESET}")
                print(f"{Couleurs.DIM}Vous pouvez maintenant demander au LLM de créer des fichiers ou d'exécuter du code.{Couleurs.RESET}")
                continue
            
            elif user_input.lower() == '/normal':
                mode_function_calling = False
                print(f"\n{Couleurs.BLEU_VIF}💬 Mode chat normal activé !{Couleurs.RESET}")
                print(f"{Couleurs.DIM}Vous pouvez maintenant discuter librement avec le LLM.{Couleurs.RESET}")
                if len(conversation_history) > 0:
                    print(f"{Couleurs.JAUNE}🧠 Historique conservé ({len(conversation_history)//2} échanges){Couleurs.RESET}")
                continue
            
            elif user_input.lower() in ['/memoire', '/memory']:
                memoire_active = not memoire_active
                status = f"{Couleurs.VERT_VIF}activée{Couleurs.RESET}" if memoire_active else f"{Couleurs.ROUGE_VIF}désactivée{Couleurs.RESET}"
                print(f"\n{Couleurs.JAUNE_VIF}🧠 Mémoire conversationnelle {status} !{Couleurs.RESET}")
                if memoire_active:
                    print(f"{Couleurs.DIM}Le LLM se souviendra de vos échanges précédents dans cette session.{Couleurs.RESET}")
                else:
                    print(f"{Couleurs.DIM}Le LLM traitera chaque message indépendamment.{Couleurs.RESET}")
                continue
            
            elif user_input.lower() in ['/historique', '/history']:
                print(f"\n{Couleurs.JAUNE_VIF}🧠 HISTORIQUE DE LA CONVERSATION{Couleurs.RESET}")
                print(f"{Couleurs.JAUNE_VIF}{'═' * 40}{Couleurs.RESET}")
                
                if not conversation_history:
                    print(f"{Couleurs.DIM}Aucun historique pour le moment.{Couleurs.RESET}")
                else:
                    for i, msg in enumerate(conversation_history):
                        role = "👤 Vous" if msg["role"] == "user" else "🤖 Mistral"
                        color = Couleurs.VERT_VIF if msg["role"] == "user" else Couleurs.CYAN_VIF
                        content = msg["content"][:100] + "..." if len(msg["content"]) > 100 else msg["content"]
                        print(f"{color}{role}:{Couleurs.RESET} {content}")
                    
                    print(f"\n{Couleurs.DIM}Total: {len(conversation_history)//2} échanges en mémoire{Couleurs.RESET}")
                continue
            
            elif user_input.lower() in ['/clear', '/cls']:
                effacer_ecran()
                afficher_titre()
                conversation_history = []  # Effacer aussi l'historique
                print(f"\n{Couleurs.VERT_VIF}✨ Chat et mémoire effacés ! Nouvelle conversation...{Couleurs.RESET}")
                continue
            
            if not user_input:
                continue
            
            print(f"\n{Couleurs.CYAN_VIF}🤖 Mistral:{Couleurs.RESET} ", end="", flush=True)
            
            if mode_function_calling:
                animation_thread = animation_chargement("Analyse et planification en cours", 1)
                time.sleep(1)
                print()  
                
               
                result = iterative_function_calling_system(user_input, max_iterations=3)
                
                if result.get("success"):
                    # Affichage du résumé du système itératif
                    print(f"{Couleurs.VERT_VIF}✅ Processus itératif terminé !{Couleurs.RESET}")
                    print(f"{Couleurs.CYAN}📊 Résumé :{Couleurs.RESET}")
                    print(f"   {Couleurs.DIM}• Itérations: {result.get('total_iterations', 0)}{Couleurs.RESET}")
                    print(f"   {Couleurs.DIM}• Statut: {result.get('final_status', 'unknown')}{Couleurs.RESET}")
                    
                    if result.get('task_results'):
                        print(f"{Couleurs.MAGENTA}🔧 Actions effectuées :{Couleurs.RESET}")
                        for i, task in enumerate(result.get('task_results', []), 1):
                            status_emoji = "✅" if task.get('success') else "❌"
                            print(f"   {status_emoji} {i}. {task.get('action')} - {task.get('details', 'N/A')}")
                else:
                    print(f"{Couleurs.ROUGE_VIF}❌ Erreur dans le processus itératif :{Couleurs.RESET} {result.get('error', 'Erreur inconnue')}")
            
            else:
                animation_thread = animation_chargement("Réflexion en cours", 1)
                # Utiliser l'historique seulement si la mémoire est activée
                history_to_use = conversation_history if memoire_active else None
                response = generateText(user_input, conversation_history=history_to_use)
                time.sleep(0.5)  # Petite pause pour l'effet
                print(f"\n{Couleurs.BLANC}{response}{Couleurs.RESET}")
                
                # Toujours sauvegarder l'historique pour /historique, même si mémoire désactivée
                conversation_history.extend([
                    {"role": "user", "content": user_input},
                    {"role": "assistant", "content": response}
                ])
                
                max_history_pairs = 5 
                if len(conversation_history) > max_history_pairs * 2:
                    conversation_history = conversation_history[-(max_history_pairs * 2):]
        
        except KeyboardInterrupt:
            print(f"\n\n{Couleurs.JAUNE_VIF}👋 Chat interrompu. Au revoir !{Couleurs.RESET}")
            break
        except Exception as e:
            print(f"\n{Couleurs.ROUGE_VIF}❌ Erreur inattendue :{Couleurs.RESET} {e}")
            print(f"{Couleurs.DIM}Vous pouvez continuer à utiliser le chat.{Couleurs.RESET}")

if __name__ == "__main__":
    try:
        chat_interactif()
        
    except Exception as e:
        print(f"{Couleurs.ROUGE_VIF}❌ Erreur lors du démarrage :{Couleurs.RESET} {e}")
        sys.exit(1) 