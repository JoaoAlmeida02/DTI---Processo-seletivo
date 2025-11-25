import os
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.pool import SimpleConnectionPool
from contextlib import contextmanager
from dotenv import load_dotenv

load_dotenv()

# Configuração do pool de conexões
DATABASE_URL = os.getenv("DATABASE_URL")

# Pool de conexões (reutiliza conexões)
_pool: Optional[SimpleConnectionPool] = None


def get_pool():
    """Obtém ou cria o pool de conexões"""
    global _pool
    if _pool is None:
        if not DATABASE_URL:
            raise ValueError(
                "DATABASE_URL não encontrada. Configure a variável de ambiente."
            )
        _pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            dsn=DATABASE_URL,
        )
    return _pool


@contextmanager
def get_connection():
    """Context manager para obter uma conexão do pool"""
    pool = get_pool()
    conn = pool.getconn()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


@contextmanager
def get_cursor():
    """Context manager para obter um cursor com RealDictCursor"""
    with get_connection() as conn:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        try:
            yield cursor
        finally:
            cursor.close()


def init_db():
    """Inicializa o banco de dados executando o schema.sql"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            # Ler o arquivo schema.sql
            schema_path = os.path.join(
                os.path.dirname(__file__), "schema.sql"
            )
            
            with open(schema_path, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            
            # Executar o schema
            cursor.execute(schema_sql)
            conn.commit()
            cursor.close()
            
            print("SUCCESS: Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"ERROR: Erro ao inicializar banco de dados: {e}")
        raise


def test_connection():
    """Testa a conexão com o banco de dados"""
    try:
        with get_cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("SUCCESS: Conexao com banco de dados estabelecida com sucesso!")
            return True
    except Exception as e:
        print(f"ERROR: Erro ao conectar com banco de dados: {e}")
        return False

