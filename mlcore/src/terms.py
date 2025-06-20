tech_terms = {
    # Programming languages
    "python", "java", "javascript", "typescript", "go", "rust",
    "c", "c++", "c#", "php", "ruby", "swift", "kotlin", "scala",
    "perl", "r", "julia",

    # Web frameworks & libraries
    "django", "flask", "fastapi", "spring", "springboot", "express",
    "react", "angular", "vue", "svelte", "nextjs", "nuxt", "ember",
    "laravel", "rails", "aspnet", "dotnet", "jquery",

    # Data & ML libraries
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost",
    "spark", "hadoop", "pandas", "numpy", "matplotlib", "seaborn",

    # Databases & storage
    "mysql", "postgresql", "mongodb", "redis", "cassandra",
    "elasticsearch", "sqlite", "mariadb", "dynamodb", "firebase",

    # Messaging & streaming
    "kafka", "rabbitmq", "mqtt", "activemq", "zeromq",

    # Containerization & orchestration
    "docker", "kubernetes", "helm", "openshift", "ecs", "eks", "gke",

    # Cloud providers & services
    "aws", "azure", "gcp", "digitalocean", "heroku",

    # DevOps & CI/CD
    "jenkins", "circleci", "githubactions", "gitlabci", "travisci",
    "terraform", "ansible", "puppet", "chef",

    # Monitoring & observability
    "prometheus", "grafana", "elk", "logstash", "filebeat", "jaeger",

    # API styles & protocols
    "rest", "graphql", "grpc", "soap", "websocket",

    # Frontend build & tooling
    "webpack", "rollup", "babel", "eslint", "prettier", "parcel",

    # Testing & QA
    "pytest", "junit", "mocha", "jest", "selenium", "cypress",

    # Buzzwords & methodologies
    "microservices", "serverless", "edgecomputing", "iot",
    "devops", "devsecops", "sre", "tdd", "bdd", "agile", "scrum",
    "kanban", "chaosengineering", "observability",

    # AI/ML buzz
    "ai", "ml", "dl", "nlp", "computer vision", "cv", "reinforcement learning",
    "transfer learning", "deep learning", "anomaly detection"
}

def filter_tech_terms(candidates: list[str], glossary: set[str]):
    return [w for w in candidates if w.lower() in glossary]