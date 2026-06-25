

from .trie import Trie

KNOWN_SKILLS = [
    # Languages
    "python", "java", "javascript", "typescript", "c++", "golang", "rust",
    "ruby", "php", "kotlin", "swift", "scala", "r",
    # Web / backend
    "flask", "django", "fastapi", "node js", "express", "spring boot",
    "rest api", "graphql", "microservices", "websockets",
    # Frontend
    "react", "vue", "angular", "html", "css", "tailwind", "redux",
    # Data
    "sql", "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
    "data structures", "algorithms", "pandas", "numpy",
    # ML / AI
    "machine learning", "deep learning", "natural language processing",
    "tensorflow", "pytorch", "scikit learn", "computer vision",
    # DevOps / infra
    "docker", "kubernetes", "terraform", "ansible", "jenkins",
    "ci cd", "aws", "azure", "gcp", "linux", "nginx", "git", "github",
    "gitlab", "bash",
    # Practices / methodology
    "agile", "scrum", "unit testing", "test driven development", "oop",
    "object oriented programming", "design patterns", "system design",
    "data structures and algorithms",
    # Tools
    "jira", "figma", "postman", "kafka", "rabbitmq", "grpc",
]


def build_skill_trie():
    trie = Trie()
    for skill in KNOWN_SKILLS:
        trie.insert(skill)
    return trie
