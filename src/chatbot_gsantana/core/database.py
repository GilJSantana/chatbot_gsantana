from sqlalchemy.orm import declarative_base

# Apenas a Base declarativa é definida no nível do módulo.
# A criação do engine e da sessão será feita de forma "preguiçosa" (lazy)
# para melhorar a testabilidade.
Base = declarative_base()
