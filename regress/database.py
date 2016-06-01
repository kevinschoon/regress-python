import os

from sqlalchemy.sql import select
from sqlalchemy import Table, Column, Integer, Float, ForeignKey, String, MetaData, create_engine

from regress import RegressException
from regress.model import Model

metadata = MetaData()

models = Table(
    "model", metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String(length=100)),
    Column("x_title", String(length=100)),
    Column("y_title", String(length=100)),
    Column("description", String(length=1000))
)

data_points = Table(
    "data", metadata,
    Column("id", Integer, primary_key=True),
    Column("model_id", None, ForeignKey("model.id")),
    Column("x_val", Float),
    Column("y_val", Float),
    Column("p_val", Float),
)


class Database:
    def __init__(self):
        url = os.environ.get("MYSQL_URL")
        if url is None:
            url = "sqlite:////tmp/regress.db"
        self.engine = create_engine(url, echo=True, pool_recycle=3600)

    def init_db(self):
        metadata.create_all(self.engine)

    def _read(self, statement):
        results = []
        for row in self.engine.execute(statement):
            previous = [x for x in results if x.name == row[1]]
            if previous:
                previous[0].add(row[7], row[8], row[9])
            else:
                results.append(Model(row[1], row[2], row[3], row[4]))
        return results

    def create(self, model):
        primary_key = self.engine.execute(
            models.insert(),
            name=model.name,
            x_title=model.x_title,
            y_title=model.y_title,
            description=model.description,
        ).inserted_primary_key[0]
        self.engine.execute(data_points.insert(), [
            {
                "model_id": primary_key,
                "x_val": x[0],
                "y_val": x[1],
                "p_val": x[2],
            } for x in model.to_dict()["data"]
        ])

    def model(self, name):
        result = self._read(select(
            [models, data_points]).where(
            models.c.id == data_points.c.model_id).where(
            models.c.name == name))
        if len(result) != 1:
            raise RegressException
        return result[0]

    def models(self):
        return self._read(select([models, data_points]).where(models.c.id == data_points.c.model_id))


db = Database()
