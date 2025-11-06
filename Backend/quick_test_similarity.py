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
    algorithms = []
    
    # Algoritmos clásicos (siempre disponibles)
    algorithms.append((LevenshteinSimilarity(), '1. Levenshtein Distance'))
    algorithms.append((TFIDFCosineSimilarity(max_features=5000), '2. TF-IDF + Cosine Similarity'))
    algorithms.append((JaccardSimilarity(remove_stopwords=True), '3. Jaccard Similarity'))
    algorithms.append((NGramSimilarity(n=3, ngram_type='char'), '4. N-gramas'))
    
    # Algoritmos con IA (requieren dependencias adicionales)
    print("🔍 Verificando disponibilidad de algoritmos con IA...\n")
    
    try:
        print("   Inicializando BERT Embeddings...")
        bert_algo = BERTEmbeddingsSimilarity(model_name='bert-base-uncased')
        algorithms.append((bert_algo, '5. BERT Embeddings'))
        print("   ✅ BERT disponible\n")
    except RuntimeError as e:
        print(f"   ⚠️  BERT no disponible: {e}\n")
        algorithms.append((None, '5. BERT Embeddings'))
    except Exception as e:
        print(f"   ⚠️  Error al cargar BERT: {e}\n")
        algorithms.append((None, '5. BERT Embeddings'))
    
    try:
        print("   Inicializando Sentence-BERT...")
        sbert_algo = SentenceBERTSimilarity(model_name='all-MiniLM-L6-v2')
        algorithms.append((sbert_algo, '6. Sentence-BERT'))
        print("   ✅ Sentence-BERT disponible\n")
    except RuntimeError as e:
        print(f"   ⚠️  Sentence-BERT no disponible: {e}\n")
        algorithms.append((None, '6. Sentence-BERT'))
    except Exception as e:
        print(f"   ⚠️  Error al cargar Sentence-BERT: {e}\n")
        algorithms.append((None, '6. Sentence-BERT'))
    
    total_start = time.time()
    
    for algorithm, algo_name in algorithms:
        print(f"🔄 {algo_name}...")
        
        # Saltar si el algoritmo no está disponible
        if algorithm is None:
            algo_key = algo_name.split('.')[0].strip()
            results[algo_key] = {
                'name': algo_name,
                'status': 'skipped',
                'error': 'Dependencias no instaladas (torch/transformers)'
            }
            print(f"   ⏭️  Omitido (dependencias no disponibles)\n")
            continue
        
        try:
            start = time.time()
            
            # Crear matriz de similitud comparando todos los pares
            n = len(publications)
            matrix = [[0.0 for _ in range(n)] for _ in range(n)]
            
            max_similarity = 0.0
            max_pair = None
            pairs_count = 0
            
            # Comparar cada par de publicaciones
            for i in range(n):
                for j in range(i+1, n):
                    pairs_count += 1
                    
                    # Combinar título + abstract para comparación
                    text1 = f"{publications[i].title or ''} {publications[i].abstract or ''}".strip()
                    text2 = f"{publications[j].title or ''} {publications[j].abstract or ''}".strip()
                    
                    # Calcular similitud
                    sim_value = algorithm.calculate_similarity(text1, text2)
                    
                    # Guardar en matriz (simétrica)
                    matrix[i][j] = sim_value
                    matrix[j][i] = sim_value
                    
                    if sim_value > max_similarity:
                        max_similarity = sim_value
                        max_pair = (i, j)
            
            elapsed = time.time() - start
            matrix_size = n
            
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
    skipped_count = sum(1 for r in results.values() if r['status'] == 'skipped')
    error_count = len(results) - success_count - skipped_count
    
    print(f"✅ Algoritmos exitosos: {success_count}/{len(algorithms)}")
    print(f"⏭️  Algoritmos omitidos: {skipped_count}/{len(algorithms)} (dependencias no instaladas)")
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
        elif result_data['status'] == 'skipped':
            tiempo = "N/A"
            estado = "⏭️  OMITIDO"
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
    
    if success_count >= 4:
        print("🎉 ¡EXCELENTE! Los algoritmos clásicos funcionan correctamente")
        print("✅ El sistema está listo para análisis bibliométrico académico")
        
        if skipped_count > 0:
            print(f"\n⚠️  {skipped_count} algoritmos con IA fueron omitidos (requieren torch/transformers)")
            print("💡 Para usarlos, instala: pip install torch transformers sentence-transformers")
        
        print("\n📈 Próximos pasos:")
        print("   1. Descargar más publicaciones (50-100)")
        print("   2. Ejecutar análisis con dataset completo")
        print("   3. Comparar resultados de diferentes algoritmos")
        print("   4. (Opcional) Instalar dependencias para algoritmos con IA")
    else:
        print("⚠️  Algunos algoritmos presentaron errores")
        print("💡 Revisa los logs de error arriba para más detalles")
    
    print("\n" + "="*70 + "\n")
    
    return results


if __name__ == '__main__':
    print("\n🚀 Iniciando prueba de similitud...\n")
    results = asyncio.run(test_similarity())
    print("✅ Prueba completada\n")
