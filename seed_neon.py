"""Script para popular a tabela unidades no Neon PostgreSQL."""

import os
from pathlib import Path

import psycopg2  # type: ignore[import-untyped]  # pylint: disable=import-error  # pyright: ignore[reportMissingImports, reportMissingTypeStubs]
from dotenv import (
    load_dotenv,  # type: ignore[import-not-found]  # pylint: disable=import-error  # pyright: ignore[reportMissingImports]
)

load_dotenv(Path(__file__).with_name(".env"))

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise SystemExit(
        "ERRO: DATABASE_URL não encontrada. Crie um arquivo .env na raiz do projeto."
    )

SQL_SCRIPT = """
CREATE TABLE IF NOT EXISTS unidades (
    id INT PRIMARY KEY,
    moradores INT NOT NULL,
    nome_responsavel VARCHAR(100) NOT NULL
);
TRUNCATE TABLE unidades;
INSERT INTO unidades (id, moradores, nome_responsavel) VALUES
    (1, 3, 'Residente 01'),
    (2, 3, 'Residente 02'),
    (101, 2, 'Residente 101'),
    (102, 2, 'Residente 102'),
    (201, 2, 'Residente 201'),
    (202, 2, 'Residente 202'),
    (301, 1, 'Residente 301'),
    (302, 2, 'Residente 302');
"""

try:
    with psycopg2.connect(db_url) as conn:
        with conn.cursor() as cursor:
            cursor.execute(SQL_SCRIPT)
            conn.commit()
            print("COMMIT realizado com sucesso! 8 unidades cadastradas no Neon.")
except psycopg2.Error as err:
    raise SystemExit(f"Erro ao conectar ou popular o Neon: {err}") from err
