import os
import subprocess

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base
from main import app, get_db

load_dotenv()

SQLALCHEMY_TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    # DockerコンテナでPostgreSQLを起動 (docker-compose up)
    subprocess.run(["docker-compose", "up", "-d"], check=True)

    # テスト用DBのテーブル作成
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as c:
        yield c

    # テーブルを削除
    Base.metadata.drop_all(bind=engine)

    # Dockerコンテナを停止 (docker-compose down)
    subprocess.run(["docker-compose", "down"], check=True)
