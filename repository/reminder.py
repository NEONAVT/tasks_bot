from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from datetime import date
from models import User


@dataclass
class ReminderRepository:
    db_session: Session

    def get_chat_ids(self) -> list[int]:
        query = select(User.chat_id).where(
            or_(
                User.last_updated_date == None,
                User.last_updated_date < date.today()
            )
        )
        # chat_ids = self.db_session.execute(query).scalars().all()
        # return chat_ids
        result = self.db_session.execute(query)
        chat_ids = [chat_id for (chat_id,) in result]
        return chat_ids