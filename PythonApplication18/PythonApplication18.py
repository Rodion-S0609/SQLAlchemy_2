from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///:memory:", echo=True)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def run_transaction():

    with Session() as session:
        with session.begin():
            print("\n--- Начало транзакции ---")
            
            user1 = User(name="Rodion")
            user2 = User(name="Artem")
            
            session.add_all([user1, user2])
            
            print("Данные добавлены в сессию, ожидаем коммита...")
            
        print("--- Транзакция успешно завершена (COMMIT) ---\n")

if __name__ == "__main__":
    run_transaction()
    
    with Session() as session:
        users = session.query(User).all()
        print(f"Пользователи в базе: {[u.name for u in users]}")
