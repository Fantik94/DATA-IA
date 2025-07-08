#!/usr/bin/env python3
"""
Script de test pour le système de function calling itératif
"""

from llm_function_calling import iterative_function_calling_system

def test_iterative_system():
    """Test du système itératif avec différents scénarios"""
    
    print("🧪 TESTS DU SYSTÈME ITÉRATIF")
    print("=" * 60)
    
    # Test 1: Création et exécution d'un script simple
    print("\n📝 TEST 1: Création d'un script calculatrice")
    print("-" * 40)
    
    request1 = "Crée un fichier Python qui demande deux nombres à l'utilisateur et affiche leur somme, puis exécute-le"
    result1 = iterative_function_calling_system(request1, max_iterations=4)
    
    print(f"\n✅ Test 1 terminé - {result1.get('total_iterations')} itérations")
    
    # Test 2: Création d'un script plus complexe
    print("\n" + "=" * 60)
    print("\n📝 TEST 2: Script avec gestion d'erreurs")
    print("-" * 40)
    
    request2 = "Crée un script Python qui calcule la factorielle d'un nombre avec gestion d'erreurs, teste-le avec différentes valeurs"
    result2 = iterative_function_calling_system(request2, max_iterations=5)
    
    print(f"\n✅ Test 2 terminé - {result2.get('total_iterations')} itérations")
    
    # Test 3: Amélioration itérative
    print("\n" + "=" * 60)
    print("\n📝 TEST 3: Amélioration itérative d'un script")
    print("-" * 40)
    
    request3 = "Crée un jeu de devinette de nombre, puis améliore-le en ajoutant un système de score et des niveaux de difficulté"
    result3 = iterative_function_calling_system(request3, max_iterations=6)
    
    print(f"\n✅ Test 3 terminé - {result3.get('total_iterations')} itérations")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    tests = [
        ("Test 1 - Calculatrice", result1),
        ("Test 2 - Factorielle", result2),
        ("Test 3 - Jeu devinette", result3)
    ]
    
    for test_name, result in tests:
        status = "✅ Réussi" if result.get('success') else "❌ Échoué"
        iterations = result.get('total_iterations', 0)
        actions = len(result.get('task_results', []))
        
        print(f"{test_name}: {status}")
        print(f"  - Itérations: {iterations}")
        print(f"  - Actions: {actions}")
        print(f"  - Statut: {result.get('final_status', 'unknown')}")
        print()

if __name__ == "__main__":
    test_iterative_system() 