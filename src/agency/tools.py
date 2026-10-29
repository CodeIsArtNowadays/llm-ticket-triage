from langchain_core.tools import tool
from sqlalchemy import select

from src.agency.mock_data.models import ClientModel, TransactionModel
from src.core.database import local_session
from src.core.exceptions import NotFoundException


@tool
async def get_customer_by_username(username: str):
    """Get client info from database. 
    input
        username: str
    output
        client model with fields:
            id,
            username,
            status - discount for user
    """
    async with local_session.begin() as session:
        stmt = select(ClientModel).where(ClientModel.username == username)
        res = await session.scalar(stmt)
        if not res:
            return {'error': f'User with username {username} not found'}
        customer = {
            'client_id': res.id,
            'username': res.username,
            'discount_status': res.status
        }
    return customer

@tool
async def get_transactions_by_customer_id(client_id: int):
    """Get a list of transactions that user made. 
    input
        client_id - id of user to find transactions
    output
        list of transactions each contains fields:
            id,
            amout,
            client_id
    """
    async with local_session.begin() as session:
        stmt = select(TransactionModel).where(TransactionModel.client_id == client_id)
        res = await session.scalars(stmt)
        if not res.all():
            return {
                'error': f'No transactions for user with id {client_id}'
            }

        txs = []
        for tx in res.all():
            txs.append({
                'id': tx.id,
                'amount': tx.amount,
                'client_id': tx.client_id,
                'created': tx.created_at
            })

    return txs

