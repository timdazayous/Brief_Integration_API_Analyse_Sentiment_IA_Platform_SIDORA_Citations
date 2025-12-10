import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import pandas as pd
from backend.modules.db_tools import write_db, read_db, Base, QuoteModel

# ---------------
# --- FIXTURE ---
# ---------------
## create engine
@pytest.fixture(scope="module")
def engine_test():
    """Create engine"""
    return create_engine("sqlite:///:memory:")

## create DB
@pytest.fixture(scope="module")
def setup_db(engine_test):
    """Create table"""
    Base.metadata.create_all(engine_test)
    yield
    Base.metadata.drop_all(engine_test)

## create DB SESSION
@pytest.fixture(scope="function")
def db_session(engine_test, setup_db):
    """Yield DB Session"""
    connection = engine_test.connect()
    transaction = connection.begin()

    SessionTest = sessionmaker(autocommit=False, autoflush= False, bind=engine_test)
    session = SessionTest(bind=connection)

    yield session 

    # clean
    session.close()
    transaction.rollback()
    connection.close()
# ------------
# --- MOCK ---
# ------------
## OVERRIDE SESSION LOCAL
@pytest.fixture(autouse=True)
def override_get_db_session(monkeypatch, db_session):
    """Mock get db session"""
    def mock_get_db_session():
        return db_session
    monkeypatch.setattr('backend.modules.db_tools.get_db_session', mock_get_db_session)
# ------------
# --- TEST ---
# ------------
## TEST write db and read db
def test_add_and_read_quote():
    quote = "test"
    dico = {"text" : [quote]}
    df = pd.DataFrame(dico)
    # add citation
    write_db(df)    
    # read citation
    df2 = read_db()
    citation = df2.iloc[0]["text"]
    assert not df2.empty
    assert citation == quote
