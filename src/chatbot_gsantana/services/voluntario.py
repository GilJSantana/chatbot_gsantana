from sqlalchemy.orm import Session

from ..models.voluntario import Voluntario
from ..repositories.voluntario import VoluntarioRepository


class VoluntarioService:
    """
    Camada de serviço para a lógica de negócio relacionada ao perfil do voluntário.
    """

    def __init__(self, repository: VoluntarioRepository):
        self.repository = repository

    def persistir_perfil_voluntario(
        self,
        db: Session,
        session_id: str,
        nome: str,
        local: str,
        hobbies: str,
        conhecimentos: dict,
    ) -> Voluntario:
        """
        Orquestra a criação ou atualização de um perfil de voluntário.
        """
        perfil = self.repository.get_by_session_id(db, session_id=session_id)

        if not perfil:
            perfil = Voluntario(session_id=session_id)

        perfil.nome = nome
        perfil.local = local
        perfil.hobbies = hobbies
        perfil.conhecimentos = conhecimentos

        return self.repository.save_or_update(db, voluntario=perfil)


# Função de dependência para o FastAPI
def get_voluntario_service() -> VoluntarioService:
    """
    Dependência do FastAPI que cria e fornece uma instância de VoluntarioService.
    """
    repository = VoluntarioRepository()
    return VoluntarioService(repository=repository)
