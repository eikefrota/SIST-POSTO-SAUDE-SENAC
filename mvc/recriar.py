from model.model import Base, db_manager

def recreate_database():
    engine = db_manager.engine
    print("Dropping all tables...")
    Base.metadata.drop_all(engine)
    print("Creating all tables...")
    Base.metadata.create_all(engine)
    print("Database recreation completed.")

if __name__ == "__main__":
    recreate_database()