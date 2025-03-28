from sqlmodel import SQLModel, create_engine, Session


database_filename= "sensorAPI"
connect_args = {"check_same_thread":False}
engine = create_engine(f"sqlite:///app/database/{database_filename}.db", echo=True, connect_args=connect_args)

# Create database tables if they dont exist
def create_db():
    SQLModel.metadata.create_all(engine)

# Generator for handling database connections
def get_session():
    with Session(engine) as session:
        yield session