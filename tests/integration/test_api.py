import pytest


@pytest.mark.asyncio
async def test_create_ticket_endpoint_success(ac):
    response = await ac.post('/api/tickets', json={'user': 'Test User 1', 'message': 'Test message 1'})
    assert response.status_code == 201


@pytest.mark.asyncio
async def test_get_existing_ticket(ac):
    response = await ac.get('/api/tickets/d79e9082-3a51-4e0a-addc-c2aa5161ac73')
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_non_existing_ticket(ac):
    response = await ac.get('/api/tickets/d79e9082-3a51-4e0a-addc-c2aa5451ac73')
    assert response.status_code == 404
