"""
Prueba rápida de análisis de similitud con publicaciones reales
Valida los 6 algoritmos implementados
"""
import asyncio
import json
import time
from pathlib import Path
import sys

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ml_analysis.similarity import (
    LevenshteinSimilarity,
    TFIDFCosineSimilarity,
    JaccardSimilarity,
    NGramSimilarity,
    BERTEmbeddingsSimilarity,
    SentenceBERTSimilarity
)
from app.models.publication import Publication


async def test_similarity():
    """Prueba los 6 algoritmos de similitud con datos reales"""
    
    print("\n" + "="*70)
    print("🔍 PRUEBA DE ANÁLISIS DE SIMILITUD")
    print("="*70 + "\n")
    
    # Cargar publicaciones reales
    json_path = Path(__file__).parent / 'data' / 'downloads' / 'test_download_5_pubs.json'
    
    if not json_path.exists():
        print(f"❌ Error: No se encontró el archivo de publicaciones")
        print(f"   Ruta esperada: {json_path}")
        print(f"\n💡 Primero ejecuta: python Backend/test_download_priority.py")
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
        print("\n❌ Se necesitan al menos 2 publicaciones para análisis de similitud")
        return
    
    print(f"\n✅ {len(publications)} publicaciones válidas para análisis\n")
    
    print("-"*70)
    print("🚀 EJECUTANDO ANÁLISIS CON 6 ALGORITMOS")
    print("-"*70 + "\n")
    
    results = {}
    
    # Lista de algoritmos a probar con sus instancias
    algorithms = [
        (LevenshteinSimilarity(), '1. Levenshtein Distance'),
        (TFIDFCosineSimilarity(max_features=5000), '2. TF-IDF + Cosine Similarity'),
        (JaccardSimilarity(remove_stopwords=True), '3. Jaccard Similarity'),
        (NGramSimilarity(n=3, ngram_type='char'), '4. N-gramas'),
        (BERTEmbeddingsSimilarity(model_name='bert-base-uncased'), '5. BERT Embeddings'),
        (SentenceBERTSimilarity(model_name='all-MiniLM-L6-v2'), '6. Sentence-BERT'),
    ]
    
    total_start = time.time()
    
    for algorithm, algo_name in algorithms:
        print(f"🔄 {algo_name}...")
        try:
            start = time.time()
            # Calcular similitud usando el método del algoritmo
            result = await algorithm.calculate_similarity_matrix(publications)
            elapsed = time.time() - start
            
            # La matriz es una lista de listas con las similitudes
            matrix_size = len(result) if result else 0
            
            # Calcular pares únicos y encontrar mayor similitud
            max_similarity = 0.0
            max_pair = None
            pairs_count = 0
            
            for i in range(len(result)):
                for j in range(i+1, len(result)):
                    pairs_count += 1
                    sim_value = result[i][j]
                    if sim_value > max_similarity:
                        max_similarity = sim_value
                        max_pair = (i, j)
            
            # Guardar resultado
            algo_key = algo_name.split('.')[0].strip()
            results[algo_key] = {
                'name': algo_name,
                'execution_time': elapsed,
                'status': 'success',
                'matrix_size': f"{matrix_size}x{matrix_size}",
                'pairs_count': pairs_count,
                'max_similarity': max_similarity
            }
            
            print(f"   ✅ Completado en {elapsed:.2f}s")
            print(f"   📊 Matriz: {results[algo_key]['matrix_size']}")
            print(f"   🔗 Pares calculados: {pairs_count}")
            
            if max_pair:
                i, j = max_pair
                print(f"   🏆 Mayor similitud: {max_similarity:.4f}")
                print(f"      Entre: '{publications[i].title[:40]}...'")
                print(f"         y: '{publications[j].title[:40]}...'\n")
            
        except Exception as e:
            algo_key = algo_name.split('.')[0].strip()
            results[algo_key] = {
                'name': algo_name,
                'status': 'error',
                'error': str(e)
            }
            print(f"   ❌ ERROR: {e}\n")
    
    total_elapsed = time.time() - total_start
    
    # Resumen final
    print("\n" + "="*70)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*70 + "\n")
    
    success_count = sum(1 for r in results.values() if r['status'] == 'success')
    error_count = len(results) - success_count
    
    print(f"✅ Algoritmos exitosos: {success_count}/{len(algorithms)}")
    print(f"❌ Algoritmos con error: {error_count}/{len(algorithms)}")
    print(f"⏱️  Tiempo total: {total_elapsed:.2f}s\n")
    
    # Tabla de resultados
    print("-"*70)
    print(f"{'Algoritmo':<30} {'Tiempo':<12} {'Estado':<10}")
    print("-"*70)
    
    for result_data in results.values():
        if result_data['status'] == 'success':
            tiempo = f"{result_data['execution_time']:.2f}s"
            estado = "✅ OK"
        else:
            tiempo = "N/A"
            estado = "❌ ERROR"
        
        print(f"{result_data['name']:<30} {tiempo:<12} {estado:<10}")
    
    print("-"*70 + "\n")
    
    # Guardar resultados completos
    output_path = Path(__file__).parent / 'data' / 'downloads' / 'similarity_test_results.json'
    
    # Preparar datos para guardar (convertir a formato serializable)
    save_data = {
        'test_date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'publications_count': len(publications),
        'algorithms_tested': len(algorithms),
        'total_time': total_elapsed,
        'results': results
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(save_data, f, indent=2, default=str)
    
    print(f"💾 Resultados guardados en: {output_path.name}\n")
    
    # Recomendaciones
    print("="*70)
    print("💡 RECOMENDACIONES")
    print("="*70 + "\n")
    
    if success_count == len(algorithms):
        print("🎉 ¡EXCELENTE! Todos los algoritmos funcionan correctamente")
        print("✅ El sistema está listo para análisis bibliométrico completo")
        print("\n📈 Próximos pasos:")
        print("   1. Descargar más publicaciones (50-100)")
        print("   2. Ejecutar análisis con dataset completo")
        print("   3. Comparar resultados de diferentes algoritmos")
    else:
        print("⚠️  Algunos algoritmos presentaron errores")
        print("💡 Revisa los logs de error arriba para más detalles")
    
    print("\n" + "="*70 + "\n")
    
    return results


if __name__ == '__main__':
    print("\n🚀 Iniciando prueba de similitud...\n")
    results = asyncio.run(test_similarity())
    print("✅ Prueba completada\n")
