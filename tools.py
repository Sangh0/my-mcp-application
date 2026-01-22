from sqlalchemy import func, select

from database import SessionLocal, engine
from models import Base, Person
from schemas import PersonCreate, PersonUpdate


def _to_dict(p: Person) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "age": p.age,
        "email": p.email,
        "city": p.city,
        "country": p.country,
    }


def init_db_with_seed() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as s:
        count = s.scalar(select(func.count(Person.id)))
        if count == 0:
            s.add(
                Person(
                    name="John Doe",
                    age=30,
                    email="john.doe@example.com",
                    city="New York",
                    country="USA",
                )
            )
            s.add(
                Person(
                    name="Jane Smith",
                    age=25,
                    email="jane.smith@example.com",
                    city="Los Angeles",
                    country="USA",
                )
            )
            s.commit()


def get_person(person_id: int) -> dict:
    with SessionLocal() as db:
        p = db.execute(
            select(Person).where(Person.id == person_id)
        ).scalar_one_or_none()
        if not p:
            raise ValueError(f"person_id={person_id} 를 찾지 못했습니다.")
        return _to_dict(p)


def add_person(person: PersonCreate) -> dict:
    with SessionLocal() as db:
        db_person = Person(**person.model_dump())
        db.add(db_person)
        db.commit()
        db.refresh(db_person)
        return _to_dict(db_person)


def update_person(person_id: int, person: PersonUpdate) -> dict:
    with SessionLocal() as db:
        db_person = db.get(Person, person_id)
        if not db_person:
            raise ValueError(f"person_id={person_id} 를 찾지 못했습니다.")
        for field, value in person.model_dump().items():
            setattr(db_person, field, value)
        db.commit()
        db.refresh(db_person)
        return _to_dict(db_person)


def delete_person(person_id: int) -> dict:
    with SessionLocal() as db:
        db_person = db.get(Person, person_id)
        if not db_person:
            raise ValueError(f"person_id={person_id} 를 찾지 못했습니다.")
        db.delete(db_person)
        db.commit()
        return {"ok": True, "deleted_id": person_id}


def list_people(limit: int = 10, offset: int = 0) -> list[dict]:
    with SessionLocal() as db:
        people = db.execute(select(Person).limit(limit).offset(offset)).scalars().all()
        return [_to_dict(p) for p in people]


def find_people_by_name(query: str, limit: int = 10) -> list[dict]:
    with SessionLocal() as db:
        people = (
            db.execute(
                select(Person).where(Person.name.like(f"%{query}%")).limit(limit)
            )
            .scalars()
            .all()
        )
        return [_to_dict(p) for p in people]
