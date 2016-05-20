from flask import g

from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String, MetaData, create_engine

from regress import RegressException
from regress.model import Model

metadata = MetaData()

models = Table(
    "model", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
    Column("x_title", String),
    Column("y_title", String),
    Column("description", String)
)

data_points = Table(
    "data", metadata,
    Column("id", Integer, primary_key=True),
    Column("model_id", None, ForeignKey("model.id")),
    Column("x_val", Integer),
    Column("y_val", Integer),
    Column("p_val", Float),
)

engine = create_engine("sqlite:////tmp/test.db", echo=True)


def init_database():
    metadata.create_all(engine)


def get_database():
    db = getattr(g, "_db", None)
    if db is None:
        db = g._db = engine.connect()
    return db


def create_model(model):
    db = get_database()
    primary_key = db.execute(
        models.insert(),
        name=model.name,
        x_title=model.x_title,
        y_title=model.y_title,
        description=model.description,
    ).inserted_primary_key[0]
    db.execute(data_points.insert(), [
        {
            "model_id": primary_key,
            "x_val": x[0],
            "y_val": x[1],
            "p_val": x[2],
        } for x in model.to_dict()["data"]
        ])


def read(statement):
    db = get_database()
    results = []
    for row in db.execute(statement):
        previous = [x for x in results if x.name == row[1]]
        if previous:
            previous[0].add(row[7], row[8], row[9])
        else:
            results.append(Model(row[1], row[2], row[3], row[4]))
    return results


def read_model(name):
    stm = select([models, data_points]).where(
        models.c.id == data_points.c.model_id).where(
        models.c.name == name)
    result = read(stm)
    if len(result) != 1:
        raise RegressException
    return result[0]


def read_all_models():
    return read(select([models, data_points]).where(models.c.id == data_points.c.model_id))


