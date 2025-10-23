import sys
from pathlib import Path

# Ensure project root is on sys.path so tests can import DAL
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import tempfile
import sqlite3
import DAL


def test_dal_add_and_get_projects(tmp_path, monkeypatch):
    db_file = tmp_path / "dal_test.db"
    monkeypatch.setattr(DAL, 'DB_PATH', str(db_file))
    # Reinitialize DB
    DAL.init_db()

    # Ensure seed data present
    projects = DAL.get_projects()
    assert isinstance(projects, list)

    # Add a new project
    DAL.add_project('UnitTest Project', 'desc', 'img.png')

    projects = DAL.get_projects()
    titles = [p['title'] for p in projects]
    assert 'UnitTest Project' in titles
