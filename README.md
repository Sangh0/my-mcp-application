### mcp-prac (SQLite + MCP + CRUD 데모)

Claude Desktop에 **MCP(Model Context Protocol)** 서버를 연결해서, 로컬 **SQLite(people.db)** 에 사람 정보를 **조회/추가/수정/삭제(CRUD)** 하는 데모 프로젝트입니다.

---

### 구성
- **MCP 서버(stdio)**: `server.py` (FastMCP)
- **DB 연결/세션**: `database.py` (SQLAlchemy + SQLite)
- **모델**: `models.py` (`Person`)
- **스키마**: `schemas.py` (Pydantic)
- **CRUD 로직**: `tools.py`
- **엔트리포인트**: `main.py`

DB 파일은 프로젝트 루트에 `people.db`로 생성됩니다(최초 실행 시 seed 데이터 자동 생성).

---

### 요구사항
- Python **3.13+** (`.python-version` 참고)
- [`uv`](https://github.com/astral-sh/uv) (권장)

---

### 실행 (로컬에서 MCP 서버 띄우기)
프로젝트 루트에서:

```bash
uv run python main.py
```

이 프로세스는 **stdio로 MCP 프로토콜을 말하는 서버**라서, 터미널에서 실행해두고 **Claude Desktop 같은 MCP Host**가 붙어서 tool을 호출하는 형태입니다.

---

### 제공되는 MCP Tools
`server.py`가 아래 tool들을 노출합니다.

- `init_db()`: DB 생성 + seed (비어있을 때만 insert)
- `list_people(limit=10, offset=0)`
- `find_people_by_name(query, limit=10)`
- `get_person(person_id)`
- `add_person(person)` (`PersonCreate`)
- `update_person(person_id, person)` (`PersonUpdate`)
- `delete_person(person_id)`

#### 데이터 스키마
현재 `Person` 필드는 다음과 같습니다.
- `name` (str)
- `age` (int)
- `email` (str)
- `city` (str)
- `country` (str)

---

### Claude Desktop에 MCP 연결하기 (macOS)
가장 쉬운 방법은 Claude Desktop에서 설정 화면으로 들어가 **Config 파일 편집**을 여는 것입니다.

1) Claude Desktop → **Settings(설정)** → **Developer** → **Edit Config**

2) `mcpServers`에 아래를 추가 (경로는 본인 프로젝트 경로 그대로 유지)

```json
{
  "mcpServers": {
    "people-db": {
      "command": "bash",
      "args": [
        "-lc",
        "cd /Users/sanghokim/Desktop/project/mcp-prac && uv run python main.py"
      ]
    }
  }
}
```

3) Claude Desktop을 **완전히 종료 후 재실행**

4) 새 대화에서 “사람 목록 보여줘” 같은 요청을 하면, Claude가 `list_people` 같은 tool을 호출합니다.

---

### 예시 프롬프트(Claude에게)
- “`list_people`로 전체 목록 보여줘”
- “이름이 John인 사람 찾아줘”
- “사람 추가해줘: 김상호, 29, hop7311@gmail.com, 수원, 대한민국”
