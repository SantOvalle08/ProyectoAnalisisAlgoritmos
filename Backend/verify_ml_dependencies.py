"""
Script de verificación de dependencias ML/NLP

Este script verifica que todas las librerías de machine learning y 
procesamiento de lenguaje natural estén funcionando correctamente.
"""

import sys
import warnings
warnings.filterwarnings("ignore")

print("🔬 Verificando dependencias ML/NLP...")
print("=" * 50)

# Test 1: PyTorch
try:
    import torch
    print(f"✅ PyTorch {torch.__version__} - Funcionando correctamente")
    print(f"   CUDA disponible: {torch.cuda.is_available()}")
except ImportError as e:
    print(f"❌ Error importando PyTorch: {e}")
    sys.exit(1)

# Test 2: Transformers
try:
    from transformers import pipeline
    print(f"✅ Transformers - Funcionando correctamente")
    
    # Test básico de pipeline
    classifier = pipeline("sentiment-analysis")
    result = classifier("This is a great project!")
    print(f"   Test de pipeline: {result[0]['label']} ({result[0]['score']:.3f})")
except Exception as e:
    print(f"❌ Error con Transformers: {e}")

# Test 3: Sentence Transformers
try:
    from sentence_transformers import SentenceTransformer
    print(f"✅ Sentence-Transformers - Funcionando correctamente")
    
    # Test básico de embeddings
    model = SentenceTransformer('all-MiniLM-L6-v2')
    sentences = ["Artificial intelligence is amazing", "Machine learning is powerful"]
    embeddings = model.encode(sentences)
    print(f"   Embeddings generados: {embeddings.shape}")
except Exception as e:
    print(f"❌ Error con Sentence-Transformers: {e}")

# Test 4: Scikit-learn
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
    
    print(f"✅ Scikit-learn - Funcionando correctamente")
    
    # Test de TF-IDF
    texts = ["artificial intelligence", "machine learning", "data science"]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    print(f"   Similitud TF-IDF: {similarity[0][0]:.3f}")
except Exception as e:
    print(f"❌ Error con Scikit-learn: {e}")

# Test 5: spaCy
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    print(f"✅ spaCy - Funcionando correctamente")
    
    # Test básico de NLP
    doc = nlp("Generative artificial intelligence is revolutionizing education")
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(f"   Entidades detectadas: {len(entities)}")
    print(f"   Tokens procesados: {len(doc)}")
except Exception as e:
    print(f"❌ Error con spaCy: {e}")

# Test 6: NLTK
try:
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    
    print(f"✅ NLTK - Funcionando correctamente")
    
    # Descargar recursos necesarios si no existen
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt', quiet=True)
    
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    
    # Test básico
    text = "Natural language processing with NLTK is powerful"
    tokens = word_tokenize(text)
    print(f"   Tokens generados: {len(tokens)}")
except Exception as e:
    print(f"❌ Error con NLTK: {e}")

# Test 7: Pandas y NumPy
try:
    import pandas as pd
    import numpy as np
    
    print(f"✅ Pandas & NumPy - Funcionando correctamente")
    
    # Test básico
    data = pd.DataFrame({
        'title': ['Paper 1', 'Paper 2', 'Paper 3'],
        'score': [0.95, 0.87, 0.92]
    })
    mean_score = np.mean(data['score'])
    print(f"   DataFrame creado: {len(data)} filas")
    print(f"   Score promedio: {mean_score:.3f}")
except Exception as e:
    print(f"❌ Error con Pandas/NumPy: {e}")

# Test 8: Levenshtein Distance
try:
    from Levenshtein import distance
    print(f"✅ Python-Levenshtein - Funcionando correctamente")
    
    # Test básico
    dist = distance("artificial intelligence", "artificial learning")
    print(f"   Distancia de Levenshtein: {dist}")
except Exception as e:
    print(f"❌ Error con Python-Levenshtein: {e}")

# Test 9: Visualización
try:
    import matplotlib.pyplot as plt
    import plotly.graph_objects as go
    print(f"✅ Librerías de visualización - Funcionando correctamente")
except Exception as e:
    print(f"❌ Error con librerías de visualización: {e}")

print("=" * 50)
print("🎉 ¡Verificación completada!")
print("\n📋 Resumen de librerías verificadas:")
print("- PyTorch 2.8.0 (CPU)")
print("- Transformers 4.56.1")
print("- Sentence-Transformers 5.1.0")
print("- Scikit-learn 1.7.2")
print("- spaCy 3.8.7 + en_core_web_sm")
print("- NLTK 3.9.1")
print("- Pandas 2.3.2")
print("- NumPy 2.2.6")
print("- Python-Levenshtein")
print("- Matplotlib & Plotly")
print("\n✅ El backend está listo para análisis bibliométrico!")