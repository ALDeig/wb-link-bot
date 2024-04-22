import sqlalchemy as sa
from sqlalchemy.dialects.sqlite import insert

from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.models import User


class UserDao(BaseDao[User]):
    model = User

    async def insert_or_nothing(
        self, user_id: int, full_name: str, username: str | None
    ):
        query = (
            insert(self.model)
            .values(id=user_id, full_name=full_name, username=username)
            .on_conflict_do_nothing(index_elements=["id"])
        )
        await self._session.execute(query)
        await self._session.commit()

    async def count(self, **filter_by) -> int:
        query = sa.select(sa.func.count(self.model.id)).filter_by(**filter_by)
        response = await self._session.execute(query)
        return response.scalar_one()
