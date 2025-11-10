"""
Prueba rápida de clustering jerárquico con publicaciones reales
Versión standalone (sin necesidad del backend)
"""
import json
import sys
from pathlib import Path
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.spatial.distance import pdist
import numpy as np

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ml_analysis.similarity import TFIDFCosineSimilarity
from app.models.publication import Publication


def main():
    """Ejecuta prueba de clustering jerárquico"""
    
    print("\n" + "="*70)
    print("🌳 PRUEBA DE CLUSTERING JERÁRQUICO")
    print("="*70 + "\n")
    
    # Cargar publicaciones reales
    json_path = Path(__file__).parent / 'data' / 'downloads' / 'test_download_5_pubs.json'
    
    if not json_path.exists():
        print(f"❌ Error: No se encontró el archivo de publicaciones")
        print(f"   Ruta esperada: {json_path}")
        return
    
    print(f"📂 Cargando publicaciones desde: {json_path.name}")
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"✅ {len(data)} publicaciones cargadas\n")
    
    # Convertir a objetos Publication
    publications = []
    for i, pub_data in enumerate(data, 1):
        try:
            pub = Publication(**pub_data)
            publications.append(pub)
            print(f"   {i}. {pub.title[:60]}...")
        except Exception as e:
            print(f"   ⚠️  Error en publicación {i}: {e}")
    
    if len(publications) < 2:
        print("\n❌ Se necesitan al menos 2 publicaciones para clustering")
        return
    
    print(f"\n✅ {len(publications)} publicaciones válidas para clustering\n")
    
    # Preparar textos para clustering
    print("-"*70)
    print("🔄 CALCULANDO DISTANCIAS CON TF-IDF...")
    print("-"*70 + "\n")
    
    texts = []
    labels = []
    
    for pub in publications:
        # Combinar título y abstract para mejor clustering
        text = f"{pub.title or ''} {pub.abstract or ''}"
        texts.append(text)
        
        # Usar primeras 50 caracteres del título como label
        label = (pub.title[:47] + "...") if pub.title and len(pub.title) > 50 else (pub.title or f"Pub {len(labels)+1}")
        labels.append(label)
    
    # Calcular matriz de similitud con TF-IDF
    algo = TFIDFCosineSimilarity(max_features=5000)
    
    print("   Calculando matriz de similitud...")
    similarity_matrix = []
    for i, text1 in enumerate(texts):
        row = []
        for j, text2 in enumerate(texts):
            sim = algo.calculate_similarity(text1, text2)
            row.append(sim)
        similarity_matrix.append(row)
        print(f"   ✅ Fila {i+1}/{len(texts)} calculada")
    
    # Convertir similitud a distancia (distancia = 1 - similitud)
    similarity_matrix = np.array(similarity_matrix)
    distance_matrix = 1 - similarity_matrix
    
    print(f"\n✅ Matriz de distancias calculada: {distance_matrix.shape}\n")
    
    # Mostrar matriz de similitud
    print("-"*70)
    print("📊 MATRIZ DE SIMILITUD")
    print("-"*70 + "\n")
    
    print("        ", end="")
    for i in range(len(publications)):
        print(f"Pub{i+1:2d}  ", end="")
    print()
    
    for i in range(len(publications)):
        print(f"Pub {i+1:2d}: ", end="")
        for j in range(len(publications)):
            sim = similarity_matrix[i][j]
            if i == j:
                print(" 1.00 ", end="")
            else:
                print(f"{sim:5.2f} ", end="")
        print()
    
    print()
    
    # Probar diferentes métodos de linkage
    linkage_methods = ['ward', 'complete', 'average', 'single']
    
    print("-"*70)
    print("🌳 GENERANDO DENDROGRAMAS")
    print("-"*70 + "\n")
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Clustering Jerárquico - Comparación de Métodos', fontsize=16, fontweight='bold')
    
    for idx, method in enumerate(linkage_methods):
        print(f"🔄 Método: {method.upper()}")
        
        try:
            # Calcular linkage
            # Para 'ward' necesitamos usar pdist con distancias euclidianas
            if method == 'ward':
                # Convertir matriz de distancias a forma condensada
                condensed_dist = pdist(distance_matrix, metric='euclidean')
                Z = linkage(condensed_dist, method=method)
            else:
                # Para otros métodos, usar la matriz de distancias directamente
                condensed_dist = pdist(distance_matrix, metric='euclidean')
                Z = linkage(condensed_dist, method=method)
            
            # Plotear dendrograma
            ax = axes[idx // 2, idx % 2]
            dendrogram(Z, labels=labels, ax=ax, orientation='right')
            ax.set_title(f'Método: {method.upper()}', fontsize=12, fontweight='bold')
            ax.set_xlabel('Distancia')
            ax.set_ylabel('Publicaciones')
            
            print(f"   ✅ Dendrograma generado\n")
            
        except Exception as e:
            print(f"   ❌ Error: {e}\n")
            ax = axes[idx // 2, idx % 2]
            ax.text(0.5, 0.5, f'Error: {str(e)}', 
                   ha='center', va='center', transform=ax.transAxes)
    
    plt.tight_layout()
    
    # Guardar figura
    output_path = Path(__file__).parent / 'data' / 'downloads' / 'clustering_dendrograms.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"💾 Dendrogramas guardados en: {output_path.name}\n")
    
    # Mostrar figura
    plt.show()
    
    # Análisis de clusters
    print("-"*70)
    print("📊 ANÁLISIS DE CLUSTERS")
    print("-"*70 + "\n")
    
    # Usar método 'average' para análisis
    condensed_dist = pdist(distance_matrix, metric='euclidean')
    Z = linkage(condensed_dist, method='average')
    
    # Extraer clusters a diferentes alturas
    from scipy.cluster.hierarchy import fcluster
    
    for n_clusters in [2, 3]:
        clusters = fcluster(Z, n_clusters, criterion='maxclust')
        
        print(f"🔹 Con {n_clusters} clusters:")
        for cluster_id in range(1, n_clusters + 1):
            indices = np.where(clusters == cluster_id)[0]
            print(f"\n   Cluster {cluster_id} ({len(indices)} publicaciones):")
            for idx in indices:
                print(f"      - {labels[idx]}")
        print()
    
    # Resumen final
    print("="*70)
    print("✅ PRUEBA DE CLUSTERING COMPLETADA")
    print("="*70 + "\n")
    
    print("📈 Resultados:")
    print(f"   ✅ {len(publications)} publicaciones analizadas")
    print(f"   ✅ {len(linkage_methods)} métodos de linkage probados")
    print(f"   ✅ Dendrogramas generados y guardados")
    print(f"   ✅ Análisis de clusters completado")
    
    print(f"\n💡 Los dendrogramas muestran cómo se agrupan las publicaciones")
    print(f"   según su similitud textual (TF-IDF).\n")
    
    print(f"📁 Archivos generados:")
    print(f"   - {output_path.name}")
    
    print("\n" + "="*70 + "\n")


if __name__ == '__main__':
    print("\n🚀 Iniciando prueba de clustering...\n")
    main()
    print("✅ Prueba completada\n")
