from collections import defaultdict

KEYWORDS = {
    "Machine Learning": [
        "machine learning",
        "classification",
        "regression",
        "supervised learning",
        "unsupervised learning",
    ],
    "Deep Learning": [
        "deep learning",
        "neural network",
        "cnn",
        "rnn",
        "lstm",
    ],
    "Natural Language Processing": [
        "nlp",
        "language model",
        "transformer",
        "bert",
        "gpt",
        "llm",
        "token",
        "text generation",
    ],
    "Computer Vision": [
        "computer vision",
        "image",
        "object detection",
        "segmentation",
        "yolo",
        "vision transformer",
    ],
    "Robotics": [
        "robot",
        "robotics",
        "manipulation",
        "autonomous robot",
    ],
    "Reinforcement Learning": [
        "reinforcement learning",
        "q-learning",
        "policy gradient",
        "actor critic",
    ],
    "Generative AI": [
        "diffusion",
        "gan",
        "generative",
        "stable diffusion",
    ],
    "Graph Neural Networks": [
        "graph neural network",
        "gnn",
        "graph convolution",
    ],
    "Quantum Computing": [
        "quantum",
        "qubit",
        "quantum circuit",
    ],
    "Cybersecurity": [
        "cybersecurity",
        "malware",
        "intrusion",
        "phishing",
        "authentication",
    ],
    "Data Science": [
        "data mining",
        "analytics",
        "data science",
    ],
}


def classify_topics(title: str, abstract: str) -> list[str]:
    """
    Returns a list of topic names based on keyword matching.
    """
    text = f"{title} {abstract}".lower()

    scores = defaultdict(int)

    for topic, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                scores[topic] += 1

    return sorted(scores, key=scores.get, reverse=True)