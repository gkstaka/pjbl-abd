from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import MEDIUMINT
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base, Dosage
from services.database import session


class Suggestion(Base):
    __tablename__ = "suggestion"

    id: Mapped[int] = mapped_column(
        "id", MEDIUMINT, nullable=False, autoincrement=True, primary_key=True
    )
    medicine_id: Mapped[int] = mapped_column(ForeignKey("medicine.id"))
    medicine: Mapped["Medicine"] = relationship(back_populates="suggestions")
    dosage_id: Mapped[int] = mapped_column(ForeignKey("dosage.id"))
    dosage: Mapped["Dosage"] = relationship(back_populates="suggestions")
    medical_record_id: Mapped[int] = mapped_column(ForeignKey("medical_record.id"))
    medical_record: Mapped["MedicalRecord"] = relationship(back_populates="suggestions")

    def __init__(self, medicine, dosage, medical_record):
        self.medicine = medicine
        self.dosage = dosage
        self.medical_record = medical_record

    @classmethod
    def find_all(cls):
        return session.query(cls).all()

    @classmethod
    def find_by_id(cls, id):
        return session.query(cls).filter_by(id=id).first()

    @classmethod
    def find_by_medicine_id(cls, medicine_id):
        return session.query(cls).filter_by(medicine_id=medicine_id).all()

    @classmethod
    def find_by_dosage_id(cls, dosage_id):
        return session.query(cls).filter_by(dosage_id=dosage_id).all()

    @classmethod
    def find_by_medical_record_id(cls, medical_record_id):
        return session.query(cls).filter_by(medical_record_id=medical_record_id).all()

    @classmethod
    def save_all(cls, suggestions):
        session.add_all(suggestions)
        session.commit()

    @classmethod
    def save(cls, suggestion):
        session.add(suggestion)
        session.commit()
