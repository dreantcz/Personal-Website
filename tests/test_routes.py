import sys
import os
import tempfile
from pathlib import Path

# Ensure project root is on sys.path so tests can import app and DAL
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pytest
from app import app
import DAL

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary DB for tests
    db_file = tmp_path / "test_projects.db"
    # monkeypatch DAL.DB_PATH to point to our temp DB
    monkeypatch.setattr(DAL, 'DB_PATH', str(db_file))
    # Reinitialize DB for a clean state
    DAL.init_db()

    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_projects_empty(client):
    # Initially, the DB seeded by init_db() will have example rows; make sure route renders
    rv = client.get('/subfolder/projects')
    assert rv.status_code == 200
    assert b'Featured Projects' in rv.data


def test_post_new_project_and_redirect(client):
    # Post valid form data to add a new project
    data = {
        'title': 'Test Project',
        'description': 'A test project description',
        'image': 'test.png'
    }
    rv = client.post('/subfolder/contact', data=data, follow_redirects=True)
    # Should redirect to projects page and show the new project title
    assert rv.status_code == 200
    assert b'Test Project' in rv.data
