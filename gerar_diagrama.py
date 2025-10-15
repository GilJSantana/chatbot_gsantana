# gerar_diagrama.py
from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import User  # Corrigido
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Postgresql
from diagrams.onprem.vcs import Github
from diagrams.onprem.ci import GithubActions  # Corrigido
from diagrams.programming.framework import Fastapi
from diagrams.programming.language import Python

with Diagram(
        "Nova arquitetura para o Chatbot Gsantana",
        show=True,
        filename="arquitetura_chatbot_gsantana",
        direction="LR",
):
    user = User("Usuário Final")

    with Cluster("GitHub"):
        github_repo = Github("Repositório")
        ci_cd_pipeline = GithubActions("CI/CD Pipeline")

        with Cluster("Etapas do Pipeline"):
            lint_format = Python("Lint & Format\n(Black, Flake8)")
            # Substituído o ícone do Pytest por um genérico do Python
            tests = Python("Testes (Pytest)")
            docker_build = Docker("Build da Imagem")

    with Cluster("Ambiente Docker (docker-compose)"):
        with Cluster("API Service (FastAPI)"):
            api_container = Fastapi(
                "API Endpoints\n(Camada de Apresentação)", width="3.0")
            service_layer = Python(
                "Lógica de Negócio\n(Camada de Serviço)", width="3.0")
            repo_layer = Python(
                "Acesso a Dados\n(Camada de Repositório)", width="3.0")

        postgres_db = Postgresql("PostgreSQL DB")

    # Fluxo de Interação e CI/CD
    github_repo >> Edge(label="Push / PR") >> ci_cd_pipeline
    ci_cd_pipeline >> lint_format >> tests >> docker_build
    docker_build >> Edge(label="Deploy (Futuro)")

    # Fluxo de Interação do Usuário com a Aplicação
    user >> Edge(label="Requisição HTTP") >> api_container

    # Fluxo Interno da Aplicação
    api_container >> service_layer >> repo_layer
    repo_layer >> Edge(label="SQLAlchemy") >> postgres_db
