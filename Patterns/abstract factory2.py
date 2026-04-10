from abc import ABC, abstractmethod

class Connection(ABC):
    @abstractmethod
    def connect(self, dsn: str) -> None: pass

    @abstractmethod
    def close(self) -> None: pass

class QueryBuilder(ABC):
    @abstractmethod
    def select(self, table: str, columns: list[str]) -> str: pass

    @abstractmethod
    def where(self, condition: str) -> str: pass

class Transaction(ABC):
    @abstractmethod
    def begin(self) -> None: pass

    @abstractmethod
    def commit(self) -> None: pass

    @abstractmethod
    def rollback(self) -> None: pass

class MySQLConnection(Connection):
    def connect(self, dsn: str) -> None:
        print(f"MySQL: подключение к {dsn}")

    def close(self) -> None:
        print("MySQL: соединение закрыто")

class MySQLQueryBuilder(QueryBuilder):
    def select(self, table: str, columns: list[str]) -> str:
        return f"SELECT {', '.join(columns)} FROM {table}"

    def where(self, condition: str) -> str:
        return f"WHERE {condition}"

class MySQLTransaction(Transaction):
    def begin(self) -> None:
        print("MySQL: START TRANSACTION")

    def commit(self) -> None:
        print("MySQL: COMMIT")

    def rollback(self) -> None:
        print("MySQL: ROLLBACK")

class PostgreSQLConnection(Connection):
    def connect(self, dsn: str) -> None:
        print(f"PostgreSQL: подключение к {dsn}")

    def close(self) -> None:
        print("PostgreSQL: соединение закрыто")

class PostgreSQLQueryBuilder(QueryBuilder):
    def select(self, table: str, columns: list[str]) -> str:
        return f'SELECT {", ".join(columns)} FROM {table}'

    def where(self, condition: str) -> str:
        return f"WHERE {condition}"

class PostgreSQLTransaction(Transaction):
    def begin(self) -> None:
        print("PostgreSQL: BEGIN")

    def commit(self) -> None:
        print("PostgreSQL: COMMIT")

    def rollback(self) -> None:
        print("PostgreSQL: ROLLBACK")

class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection: pass

    @abstractmethod
    def create_query_builder(self) -> QueryBuilder: pass

    @abstractmethod
    def create_transaction(self) -> Transaction: pass

class MySQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return MySQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        return MySQLQueryBuilder()

    def create_transaction(self) -> Transaction:
        return MySQLTransaction()

class PostgreSQLFactory(DatabaseFactory):
    def create_connection(self) -> Connection:
        return PostgreSQLConnection()

    def create_query_builder(self) -> QueryBuilder:
        return PostgreSQLQueryBuilder()

    def create_transaction(self) -> Transaction:
        return PostgreSQLTransaction()

def run_query(factory):
    conn = factory.create_connection()
    qb = factory.create_query_builder()
    tx = factory.create_transaction()

    conn.connect("host=localhost dbname=shop")
    tx.begin()
    sql = qb.select("orders", ["id", "total"]) + " " + qb.where("status = 'new'")
    print(f"Запрос: {sql}")
    tx.commit()
    conn.close()