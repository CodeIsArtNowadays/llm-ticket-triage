import asyncio
import pytest
from httpx import ASGITransport, AsyncClient
from main import app
from src.core.database import local_session  # твоя фабрика сессий (async_sessionmaker)

# 1. Жестко привязываем pytest к ОДНОМУ глобальному циклу событий на всю сессию
@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

# 2. Фикстура чистого клиента. Забудь про `async with AsyncClient` в самих тестах
@pytest.fixture
async def ac():
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as client:
        yield client

# 3. СИСТЕМНАЯ ФИКСТУРА: Сбрасывает пулы SQLAlchemy/asyncpg после КАЖДОГО теста.
# Она выполняется автоматически (autouse=True) и лечит "attached to a different loop"
@pytest.fixture(autouse=True)
async def clear_db_connections():
    yield
    # Принудительно закрываем все зависшие транзакции сессии
    await local_session.remove() if hasattr(local_session, "remove") else None
    
    # Пытаемся найти движок внутри фабрики и корректно утилизировать его пул
    if hasattr(local_session, "kw") and "bind" in local_session.kw:
        engine = local_session.kw["bind"]
        await engine.dispose()
