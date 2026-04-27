from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import urllib

conn_str = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=ТВОЙ_СЕРВЕР;" 
    "Database=ИМЯ_БАЗЫ;"
    "Trusted_Connection=yes;"
)

params = urllib.parse.quote_plus(conn_str)
connection_url = f"mssql+pyodbc:///?odbc_connect={params}"

engine = create_engine(connection_url, echo=True)

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50)) 

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def run_transaction():
    with Session() as session:
        with session.begin():
            print("\n--- Начало транзакции на SQL Server ---")
            
            user1 = User(name="Rodion")
            user2 = User(name="Artem")
            
            session.add_all([user1, user2])
            print("Данные в сессии, ожидаем COMMIT...")
            
        print("--- Транзакция успешно завершена ---\n")

if __name__ == "__main__":
    run_transaction()
    
    with Session() as session:
        users = session.query(User).all()
        print(f"Пользователи в SQL Server: {[u.name for u in users]}")
