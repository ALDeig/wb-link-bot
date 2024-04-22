from sqlalchemy.dialects.sqlite import insert

from app.src.services.db.dao.base_dao import BaseDao
from app.src.services.db.models import ServiceMessage


class ServiceMessageDao(BaseDao[ServiceMessage]):
    model = ServiceMessage

    async def insert_or_update(self, title: str, text: str):
        query = (
            insert(self.model)
            .values(title=title, text=text)
            .on_conflict_do_update(index_elements=["title"], set_={"text": text})
        )
        await self._session.execute(query)
        await self._session.commit()
