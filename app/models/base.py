from typing import Any
from sqlalchemy import update, and_, delete, func
from sqlalchemy.orm import DeclarativeBase

from services.database import session


class Base(DeclarativeBase):
    def __init__(self, **kw: Any):
        super().__init__(**kw)

    @classmethod
    def find_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def update_by_id(cls, id, new_data):
        record = session.query(cls).filter_by(id=id).first()
        if record:
            for key, value in new_data.items():
                setattr(record, key, value)
            session.commit()
        return record

    @classmethod
    def delete_item(cls, id):
        item = session.query(cls).filter_by(id=id).first()
        if item:
            session.delete(item)
            session.commit()
            return True
        return False

    @classmethod
    def delete_items(cls, ids):
        deleted_count = 0
        for id in ids:
            item = session.query(cls).filter_by(id=id).first()
            if item:
                session.delete(item)
                deleted_count += 1
        session.commit()

        if deleted_count == 0:
            return None
        elif deleted_count == len(ids):
            return True
        else:
            return False

    @classmethod
    def update_by_column(cls, filter_by: dict, **kwargs):
        stmt = (
            update(cls)
            .where(and_(*[getattr(cls, k) == v for k, v in filter_by.items()]))
            .values(**kwargs)
        )
        session.execute(stmt)
        session.commit()

    @classmethod
    def find_by_column(cls, **kwargs):
        stmt = session.query(cls).where(
            and_(*[getattr(cls, k) == v for k, v in kwargs.items()])
        )
        return stmt.all()

    def __repr__(self):
        return self.__str__()
