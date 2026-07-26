"""Supabase database access helpers for condominium unit data."""

from typing import Any, cast

from supabase import Client, create_client

from settings import settings


def get_supabase_client() -> Client:
    """Cria e retorna a instância do cliente Supabase."""
    return create_client(settings.supabase_url, settings.supabase_key)


def buscar_unidades() -> list[dict[str, Any]]:
    """Busca a lista de unidades do condomínio cadastradas no Supabase."""
    supabase = get_supabase_client()
    try:
        # Substitua 'unidades' pelo nome exato da sua tabela no Supabase
        response = supabase.table("unidades").select("*").execute()
        data = cast(list[dict[str, Any]] | None, response.data)
        return data or []
    except (ConnectionError, TimeoutError, ValueError) as err:
        print(f"[ERRO] Falha ao buscar unidades no Supabase: {err}")
        return []