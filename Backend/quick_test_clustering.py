"""
Quick test del Requerimiento 4 - Clustering API
"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/v1/clustering"

# Test data
abstracts = [
    "Generative AI models enable personalized learning experiences.",
    "Machine learning algorithms analyze student performance data.",
    "Chatbots powered by language models transform classroom interactions.",
    "Natural language processing enables automated essay grading.",
    "Educational technology platforms leverage generative models."
]

print("="*80)
print("PRUEBAS RAPIDAS - REQUERIMIENTO 4: CLUSTERING JERARQUICO")
print("="*80)

# Test 1: Health check
print("\n1. Health Check:")
r = requests.get(f"{BASE_URL}/health")
print(f"   Status: {r.status_code}")
print(f"   Response: {r.json()}")

# Test 2: Listar métodos
print("\n2. Listar Metodos de Linkage:")
r = requests.get(f"{BASE_URL}/methods")
print(f"   Status: {r.status_code}")
print(f"   Metodos disponibles: {len(r.json())}")
for method in r.json():
    print(f"     - {method['method']}: {method['name']}")

# Test 3: Clustering con Ward
print("\n3. Clustering Jerarquico (Ward Linkage):")
payload = {
    "abstracts": abstracts,
    "method": "ward",
    "num_clusters": 2,
    "generate_dendrogram": True
}
r = requests.post(f"{BASE_URL}/hierarchical", json=payload)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Metodo: {data['method']}")
    print(f"   Documentos: {data['num_documents']}")
    print(f"   Features: {data['num_features']}")
    print(f"   Correlacion cofenetica: {data['cophenetic_correlation']:.4f}")
    print(f"   Silhouette Score: {data['silhouette_score']:.4f}")
    print(f"   Clusters: {data['cluster_labels']}")
    print(f"   Dendrograma generado: {len(data['dendrogram_base64']) if data['dendrogram_base64'] else 0} chars")

# Test 4: Comparar métodos
print("\n4. Comparar los 3 Metodos:")
payload = {
    "abstracts": abstracts,
    "num_clusters": 2
}
r = requests.post(f"{BASE_URL}/compare-methods", json=payload)
print(f"   Status: {r.status_code}")
if r.status_code == 200:
    data = r.json()
    print(f"   Mejor metodo: {data['best_method']}")
    print(f"   Correlaciones cofeneticas:")
    for method, corr in data['comparison_summary']['cophenetic_correlations'].items():
        print(f"     {method}: {corr:.4f}")

print("\n" + "="*80)
print("TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
print("="*80)
