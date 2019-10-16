from sqlalchemy import exc, Column, Integer, String, DateTime, ForeignKey, \
                        Float, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine


db_uri = "sqlite:///data/example.db"
Base = declarative_base()
engine = create_engine(db_uri, echo=True)


class MeasurementModel(Base):
    __tablename__ = "measurements"
    #__table_args__ = {"schema": "smarthome"}

    id = Column(Integer,
                primary_key=True,
                nullable=False)
    # MODIFIED
    sensor_id = Column(Integer,nullable=True)
    node_uuid = Column(String(120),
                        nullable=True)
    timestamp = Column(DateTime,
                       nullable=False)
    temperature = Column(Float,
                         nullable=True)
    humidity = Column(Float,
                         nullable=True)
    pressure = Column(Float,
                         nullable=True)
    light_on = Column(Boolean,
                         nullable=True)

    def __repr__(self):
        return f"<Measurement Model {self.id}>"


class SensorModel(Base):
    __tablename__ = "sensors"
    #__table_args__ = {"schema": "smarthome"}

    id = Column(Integer,
                primary_key=True,
                nullable=False)
    node_id = Column(Integer,
                     ForeignKey("nodes.id"),
                     nullable=False)
    name = Column(String(20),
                  nullable=True)
    location = Column(String(80),
                      nullable=True)

    node = relationship("NodeModel", backref="sensor")

    def __repr__(self):
        return f"<Sensor Model {self.id}>"


class NodeModel(Base):
    __tablename__ = "nodes"
    #__table_args__ = {"schema": "smarthome"}

    id = Column(Integer,
                primary_key=True,
                nullable=False)
    name = Column(String(20),
                  unique=True,
                  nullable=True)
    location = Column(String(80),
                      nullable=True)
    description = Column(Text,
                        nullable=True)

    def __repr__(self):
        return f"<Node Model {self.id}>"


# Create all tables in the engine.
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
