from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.mysql import MEDIUMINT
from models import Base, Psychologist, Treatment
from services.database import session


class PsychologistHelpsTreatment(Base):
    __tablename__ = "psychologist_helps_treatment"

    id: Mapped[int] = mapped_column(
        "id", MEDIUMINT, nullable=False, autoincrement=True, primary_key=True
    )

    psychologist_id: Mapped[int] = mapped_column(ForeignKey("psychologist.id"))
    psychologist: Mapped["Psychologist"] = relationship(
        back_populates="psychologist_helps_treatments"
    )

    treatment_id: Mapped[int] = mapped_column(ForeignKey("treatment.id"))
    treatment: Mapped["Treatment"] = relationship(
        back_populates="psychologist_helps_treatments"
    )

    def __init__(self, psychologist, treatment, **kw):
        super().__init__(**kw)
        self.psychologist = psychologist
        self.treatment = treatment

    @classmethod
    def find_by_psychologist_id(cls, psychologist_id):
        return session.query(cls).filter_by(psychologist_id=psychologist_id).all()

    @classmethod
    def find_by_treatment_id(cls, treatment_id):
        return session.query(cls).filter_by(treatment_id=treatment_id).all()

    @classmethod
    def save_all(cls, psychologist_helps_treatments):
        session.add_all(psychologist_helps_treatments)
        session.commit()

    @classmethod
    def save(cls, psychologist_helps_treatment):
        session.add(psychologist_helps_treatment)
        session.commit()

    def __str__(self):
        return f"Psychologist Helps Treatment: {self.id}, {self.psychologist.name} - {self.treatment.name}"
