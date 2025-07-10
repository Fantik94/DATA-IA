#!/usr/bin/env python3
"""
Démonstration des nouvelles capacités de l'agent intelligent
"""

from llm_function_calling import (
    listFiles, readFile, runTests, webScraping, 
    analyzeImage, iterative_function_calling_system
)

def demo_nouvelles_capacites():
    """Démonstration des nouvelles fonctionnalités"""
    
    print("🚀 DÉMONSTRATION DES NOUVELLES CAPACITÉS DE L'AGENT")
    print("=" * 60)
    
    # 1. Listage des fichiers
    print("\n📁 1. EXPLORATION DE FICHIERS")
    result = listFiles(".")
    if result["success"]:
        print(f"✅ Trouvé {result['total_files']} fichiers et {result['total_directories']} dossiers")
        print("Fichiers Python trouvés:")
        for file in result["files"]:
            if file["extension"] == ".py":
                print(f"  📄 {file['name']} ({file['size']} bytes)")
    
    # 2. Lecture de fichier
    print("\n📖 2. LECTURE DE FICHIER")
    if result["success"] and any(f["name"] == "chat_interactif.py" for f in result["files"]):
        read_result = readFile("chat_interactif.py")
        if read_result["success"]:
            print(f"✅ Fichier lu: {read_result['lines']} lignes, {read_result['size']} bytes")
            print(f"Premières lignes:\n{read_result['content'][:200]}...")
    
    # 3. Tests exemple
    print("\n🧪 3. TESTS UNITAIRES")
    test_result = runTests("test_*.py")
    if test_result["success"]:
        print("✅ Tests réussis!")
    else:
        print(f"⚠️ Pas de tests trouvés ou échec: {test_result.get('error', 'Unknown')}")
    
    # 4. Web scraping exemple
    print("\n🌐 4. WEB SCRAPING")
    try:
        scrape_result = webScraping("https://httpbin.org/json", None)
        if scrape_result["success"]:
            print("✅ Web scraping réussi!")
            print(f"Données récupérées: {str(scrape_result['data'])[:100]}...")
        else:
            print(f"⚠️ Échec du scraping: {scrape_result.get('error')}")
    except Exception as e:
        print(f"⚠️ Erreur réseau: {e}")
    
    print("\n🎉 DÉMONSTRATION TERMINÉE!")
    print("L'agent dispose maintenant de capacités avancées:")
    print("✅ Exploration de fichiers")
    print("✅ Lecture/écriture de fichiers")
    print("✅ Tests unitaires automatiques")
    print("✅ Web scraping")
    print("✅ Analyse d'images (Pixtral)")
    print("✅ Logique itérative intelligente")

if __name__ == "__main__":
    demo_nouvelles_capacites() 