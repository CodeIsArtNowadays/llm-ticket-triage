import pytest

# Тест создания тикета
@pytest.mark.asyncio
async def test_create_ticket_endpoint_success(ac):
    # Пробуем БЕЗ косой черты на конце. Если эндпоинт в FastAPI объявлен как "/api/tickets/", 
    # а не "/api/tickets", то верни черту обратно.
    response = await ac.post('/api/tickets', json={'user': 'Test User 1', 'message': 'Test message 1'})
    assert response.status_code == 201

# Тест получения существующего тикета
@pytest.mark.asyncio
async def test_get_existing_ticket(ac):
    response = await ac.get('/api/tickets/d79e9082-3a51-4e0a-addc-c2aa5161ac73')
    assert response.status_code == 200

# Тест получения несуществующего тикета
@pytest.mark.asyncio
async def test_get_non_existing_ticket(ac):
    response = await ac.get('/api/tickets/d79e9082-3a51-4e0a-addc-c2aa5451ac73')
    assert response.status_code == 404
