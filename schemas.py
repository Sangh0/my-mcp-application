from pydantic import BaseModel, Field


class PersonBase(BaseModel):
    name: str = Field(..., description="The name of the person")
    age: int = Field(..., description="The age of the person")
    email: str = Field(..., description="The email of the person")
    city: str = Field(..., description="The city of the person")
    country: str = Field(..., description="The country of the person")


class PersonCreate(PersonBase):
    pass


class PersonUpdate(PersonBase):
    pass


class Person(PersonBase):
    id: int

    class Config:
        from_attributes = True
