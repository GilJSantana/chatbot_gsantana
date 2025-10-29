import structlog
from sqlalchemy.orm import Session

from ..models.voluntario import Voluntario
from ..repositories.voluntario import VoluntarioRepository

logger = structlog.get_logger(__name__)


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
        conhecimentos: dict
    ) -> Voluntario:
        """
        Orquestra a criação ou atualização de um perfil de voluntário.
        """
        log = logger.bind(session_id=session_id)
        log.info("service.voluntario.persist.start", nome=nome)

        perfil = self.repository.get_by_session_id(db, session_id=session_id)

        if not perfil:
            log.info("service.voluntario.persist.creating", message="Perfil não encontrado, criando novo.")
            perfil = Voluntario(session_id=session_id)
        else:
            log.info("service.voluntario.persist.updating", message="Perfil encontrado, atualizando.")

        perfil.nome = nome
        perfil.local = local
        perfil.hobbies = hobbies
        perfil.conhecimentos = conhecimentos

        saved_perfil = self.repository.save_or_update(db, voluntario=perfil)
        log.info("service.voluntario.persist.success", perfil_id=saved_perfil.id)
        return saved_perfil


# Função de dependência para o FastAPI
def get_voluntario_service() -> VoluntarioService:
    """
    Dependência do FastAPI que cria e fornece uma instância de VoluntarioService.
    """
    repository = VoluntarioRepository()
    return VoluntarioService(repository=repository)
