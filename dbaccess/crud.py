import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.dialects import postgresql
from datamodels.models import Base, Contract, NFT
from config import config as cfg

engine = create_engine(cfg.DATABASE_URI)


def start_session():
    session = sessionmaker()                                                                      
    session.configure(bind=engine)
    Base.metadata.create_all(engine)
    return session()

def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def compile_query(query):
    """Via http://nicolascadou.com/blog/2014/01/printing-actual-sqlalchemy-queries"""
    compiler = query.compile if not hasattr(query, 'statement') else query.statement.compile
    return compiler(dialect=postgresql.dialect())

def upsert(session, model, rows, no_update_cols=[]):
    table = model.__table__

    stmt = insert(table).values(rows)
    print(rows)

    update_cols = [c.name for c in table.c
                   if c not in list(table.primary_key.columns)
                   and c.name not in no_update_cols]

    on_conflict_stmt = stmt.on_conflict_do_update(
        index_elements=table.primary_key.columns,
        set_={k: getattr(stmt.excluded, k) for k in update_cols})

    session.execute(on_conflict_stmt)
    session.commit()


def insert_contract(session : sessionmaker, rows):
    upsert(session,Contract,rows)


def insert_nft(session : sessionmaker, rows):
    upsert(session,NFT,rows)


def query_nft_by_name(nft_name : str, session):
    records = session.query(NFT).filter(
              NFT.meta["name"].astext == '%'+nft_name+'%'
          ).all()
    return records
