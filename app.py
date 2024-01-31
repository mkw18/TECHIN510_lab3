import sqlite3

import streamlit as st
from pydantic import BaseModel
import streamlit_pydantic as sp
from datetime import datetime
from typing import Optional

con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        created_by TEXT DEFAULT Kaiwen,
        category TEXT DEFAULT school,
        state TEXT DEFAULT planned
    )
    """
)

class Task(BaseModel):
    name: str
    description: str
    created_at: Optional[datetime] = None
    created_by: str
    category: str
    state: str

def toggle_is_done():
    global Id
    cur.execute(
        """
        UPDATE tasks SET state = ? WHERE id = ?
        """,
        (st.session_state[Id], Id),
    )

def main():
    st.title("Todo App")
    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        cur.execute(
            """
            INSERT INTO tasks (name, description, created_at, created_by, category, state) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (data.name, data.description, data.created_at, data.created_by, data.category, data.state),
        )

    data = cur.execute(
        """
        SELECT * FROM tasks
        """
    ).fetchall()

    cols = st.columns(6)
    cols[0].write("State")
    cols[1].write("Name")
    cols[2].write("Description")
    cols[3].write("Created At")
    cols[4].write("Created By")
    cols[5].write("Category")
    for row in data:
        cols = st.columns(6)
        global Id
        Id = row[0]
        cols[0].selectbox('state', ["planned", "in-progress", "done"], index = ["planned", "in-progress", "done"].index(row[6]), label_visibility='hidden', key=row[0], on_change=toggle_is_done)
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[3].write(row[3])
        cols[4].write(row[4])
        cols[5].write(row[5])

main()