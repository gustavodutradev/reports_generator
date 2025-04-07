from sqlalchemy import create_engine, text
import dotenv
import os

dotenv.load_dotenv()
DB_URL = os.getenv("DATABASE_PUBLIC_URL")
engine = create_engine(DB_URL)


def carregar_mapas_relacionamento():
    with engine.connect() as conn:
        clientes_result = conn.execute(text("""
            SELECT nr_conta, nome_completo FROM "public"."Clientes"
        """)).fetchall()

        vinculos_result = conn.execute(text("""
            SELECT nr_conta, nm_officer FROM "public"."vinculo_de_contas"
        """)).fetchall()

    # Normalizar contas com zero à esquerda
    mapa_clientes = {str(row[0]).zfill(9): row[1] for row in clientes_result}
    mapa_assessores = {str(row[0]).zfill(9): row[1] for row in vinculos_result}

    return mapa_clientes, mapa_assessores
