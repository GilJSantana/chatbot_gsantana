import structlog
from fastapi import Depends
from sqlalchemy.orm import Session

from ..core.database import get_db
from ..models.voluntario import Voluntario
from ..repositories.voluntario import VoluntarioRepository

logger = structlog.get_logger(__name__)


class VoluntarioService:

    def __init__(
        self,
        repository: VoluntarioRepository = Depends(),
        db: Session = Depends(get_db),
    ):
        self.repository = repository
        self.db = db

    def persistir_perfil_voluntario(
        self, session_id: str, nome: str, local: str, hobbies: str, conhecimentos: dict
    ) -> Voluntario:
        log = logger.bind(session_id=session_id)
        log.info("service.voluntario.persist.start", nome=nome)

        # CORREÇÃO: Passa session_id como argumento posicional
        perfil = self.repository.get_by_session_id(self.db, session_id)

        if not perfil:
            log.info(
                "service.voluntario.persist.creating",
                message="Perfil não encontrado, criando novo.",
            )
            perfil = Voluntario(session_id=session_id)
        else:
            log.info(
                "service.voluntario.persist.updating",
                message="Perfil encontrado, atualizando.",
            )

        perfil.nome = nome
        perfil.local = local
        perfil.hobbies = hobbies
        perfil.conhecimentos = conhecimentos

        saved_perfil = self.repository.save_or_update(self.db, voluntario=perfil)
        log.info("service.voluntario.persist.success", perfil_id=saved_perfil.id)
        return saved_perfil
