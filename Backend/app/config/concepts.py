"""
Conceptos Predefinidos para Análisis de Frecuencias
===================================================

Contiene las categorías y conceptos predefinidos que se utilizarán
para el análisis de frecuencias en abstracts científicos.

Requerimiento 3: Categoría "Concepts of Generative AI in Education"
"""

from typing import Dict, List


# Categoría principal con sus palabras asociadas
GENERATIVE_AI_EDUCATION_CONCEPTS = {
    "category": "Concepts of Generative AI in Education",
    "description": "Conceptos fundamentales relacionados con inteligencia artificial "
                   "generativa aplicada al contexto educativo",
    "concepts": [
        "Generative models",
        "Prompting",
        "Machine learning",
        "Multimodality",
        "Fine-tuning",
        "Training data",
        "Algorithmic bias",
        "Explainability",
        "Transparency",
        "Ethics",
        "Privacy",
        "Personalization",
        "Human-AI interaction",
        "AI literacy",
        "Co-creation"
    ]
}


# Variantes alternativas de los conceptos (para mejor detección)
CONCEPT_VARIANTS = {
    "Generative models": [
        "generative model",
        "generative models",
        "generative modeling",
        "generative ai",
        "generative artificial intelligence",
        "gen ai"
    ],
    "Prompting": [
        "prompting",
        "prompt",
        "prompts",
        "prompt engineering",
        "prompt design"
    ],
    "Machine learning": [
        "machine learning",
        "ml",
        "machine-learning",
        "supervised learning",
        "unsupervised learning"
    ],
    "Multimodality": [
        "multimodality",
        "multimodal",
        "multi-modal",
        "multiple modalities",
        "cross-modal"
    ],
    "Fine-tuning": [
        "fine-tuning",
        "fine tuning",
        "finetuning",
        "model tuning",
        "parameter tuning"
    ],
    "Training data": [
        "training data",
        "training dataset",
        "training set",
        "labeled data",
        "annotated data"
    ],
    "Algorithmic bias": [
        "algorithmic bias",
        "algorithm bias",
        "ai bias",
        "model bias",
        "bias in ai"
    ],
    "Explainability": [
        "explainability",
        "explainable",
        "explainable ai",
        "xai",
        "interpretability"
    ],
    "Transparency": [
        "transparency",
        "transparent",
        "model transparency",
        "ai transparency"
    ],
    "Ethics": [
        "ethics",
        "ethical",
        "ai ethics",
        "ethical considerations",
        "ethical implications"
    ],
    "Privacy": [
        "privacy",
        "data privacy",
        "privacy concerns",
        "privacy protection",
        "confidentiality"
    ],
    "Personalization": [
        "personalization",
        "personalisation",
        "personalized",
        "personalised",
        "adaptive learning",
        "customization"
    ],
    "Human-AI interaction": [
        "human-ai interaction",
        "human ai interaction",
        "human-computer interaction",
        "hci",
        "user interaction"
    ],
    "AI literacy": [
        "ai literacy",
        "artificial intelligence literacy",
        "digital literacy",
        "computational literacy"
    ],
    "Co-creation": [
        "co-creation",
        "cocreation",
        "collaborative creation",
        "human-ai collaboration",
        "collaborative learning"
    ]
}


# Conceptos adicionales relacionados con educación
EDUCATION_RELATED_CONCEPTS = {
    "category": "Education and Learning",
    "concepts": [
        "Learning",
        "Teaching",
        "Education",
        "Pedagogy",
        "Assessment",
        "Curriculum",
        "Student engagement",
        "Learning outcomes",
        "Educational technology",
        "Online learning",
        "Blended learning",
        "Adaptive learning",
        "Formative assessment",
        "Summative assessment",
        "Feedback"
    ]
}


# Conceptos técnicos de IA (para contexto adicional)
AI_TECHNICAL_CONCEPTS = {
    "category": "AI Technical Concepts",
    "concepts": [
        "Neural networks",
        "Deep learning",
        "Natural language processing",
        "NLP",
        "Computer vision",
        "Reinforcement learning",
        "Transfer learning",
        "Attention mechanism",
        "Transformer",
        "GPT",
        "BERT",
        "Large language models",
        "LLM",
        "Embeddings",
        "Tokenization"
    ]
}


def get_all_concepts() -> List[str]:
    """
    Obtiene todos los conceptos predefinidos como una lista plana.
    
    Returns:
        Lista de todos los conceptos
    """
    all_concepts = []
    all_concepts.extend(GENERATIVE_AI_EDUCATION_CONCEPTS["concepts"])
    all_concepts.extend(EDUCATION_RELATED_CONCEPTS["concepts"])
    all_concepts.extend(AI_TECHNICAL_CONCEPTS["concepts"])
    return all_concepts


def get_generative_ai_concepts() -> List[str]:
    """
    Obtiene los 15 conceptos principales de IA Generativa en Educación.
    
    Returns:
        Lista de 15 conceptos
    """
    return GENERATIVE_AI_EDUCATION_CONCEPTS["concepts"]


def get_concept_with_variants(concept: str) -> List[str]:
    """
    Obtiene un concepto con todas sus variantes.
    
    Args:
        concept: Concepto principal
    
    Returns:
        Lista con el concepto y sus variantes
    """
    if concept in CONCEPT_VARIANTS:
        return CONCEPT_VARIANTS[concept]
    else:
        return [concept]


def expand_concepts_with_variants() -> Dict[str, List[str]]:
    """
    Expande todos los conceptos con sus variantes.
    
    Returns:
        Diccionario {concepto_principal: [variantes]}
    """
    return CONCEPT_VARIANTS.copy()
