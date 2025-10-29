from sqlalchemy.orm import Session

from ..models.voluntario import Voluntario


class VoluntarioRepository:
    """
    Camada de acesso a dados para o modelo Voluntario.

    Encapsula a lógica de consulta e persistência, abstraindo a sessão do SQLAlchemy.
    """

    def get_by_session_id(self, db: Session, session_id: str) -> Voluntario | None:
        """Busca um perfil de voluntário pela session_id."""
        return db.query(Voluntario).filter(Voluntario.session_id == session_id).first()

    def save_or_update(self, db: Session, voluntario: Voluntario) -> Voluntario:
        """
        Salva um novo perfil de voluntário ou atualiza um existente.
        """
        merged_voluntario = db.merge(voluntario)
        db.commit()
        db.refresh(merged_voluntario)  # Atualiza o objeto com os dados do banco
        return merged_voluntario


# A instância singleton foi removida para adotar a injeção de dependência do FastAPI.
# voluntario_repository = VoluntarioRepository()
