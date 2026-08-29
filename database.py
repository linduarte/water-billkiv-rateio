"""Neon PostgreSQL database access helpers for condominium unit data."""

import os
from typing import Any, Dict, List

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

load_dotenv()


def buscar_unidades() -> List[Dict[str, Any]]:
    """Busca a lista de unidades do condomínio cadastradas no Neon (PostgreSQL)."""
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("Variável DATABASE_URL não encontrada no arquivo .env")

    try:
        # RealDictCursor retorna os registros diretamente como dicionários Python
        with psycopg2.connect(db_url) as conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT id, moradores, nome_responsavel FROM unidades ORDER BY id;"
                )
                registros = cursor.fetchall()
                return [dict(row) for row in registros]
    except psycopg2.Error as err:
        raise RuntimeError(f"Falha ao buscar unidades no Neon: {err}") from err
