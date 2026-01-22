from fastmcp import FastMCP

import tools
from schemas import PersonCreate, PersonUpdate


mcp = FastMCP(__name__)


@mcp.tool()
def init_db():
    """SQLite DB(people.db)를 생성하고 seed 데이터를 넣습니다(비어있을 때만)."""
    tools.init_db_with_seed()
    return {"ok": True}


@mcp.tool()
def get_person(person_id: int):
    return tools.get_person(person_id)


@mcp.tool()
def add_person(person: PersonCreate):
    return tools.add_person(person)


@mcp.tool()
def update_person(person_id: int, person: PersonUpdate):
    return tools.update_person(person_id, person)


@mcp.tool()
def delete_person(person_id: int):
    return tools.delete_person(person_id)


@mcp.tool()
def list_people(limit: int = 10, offset: int = 0):
    return tools.list_people(limit, offset)


@mcp.tool()
def find_people_by_name(query: str, limit: int = 10):
    return tools.find_people_by_name(query, limit)


def run() -> None:
    tools.init_db_with_seed()
    mcp.run(transport="stdio")
