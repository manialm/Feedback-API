import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine, StaticPool

from db import get_session
from main import app

from core.settings import settings

admin_user_data = {"username": "admin", "password": "adminpass"}


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="admin_user")
def admin_user_fixture(session: Session):
    username, password = admin_user_data.values()

    from sqlmodel import select
    from user.model import User
    from auth.service import hash_password

    admin = session.exec(select(User).where(User.username == username)).first()

    if not admin:
        admin = User(
            username=username,
            password_hash=hash_password(bytes(password, "utf-8")),
            is_admin=True,
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)

    yield admin

@pytest.fixture(name="settings")
def settings_fixture():
    yield settings
