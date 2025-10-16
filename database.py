from psycopg2.extras import RealDictCursor, RealDictRow
from psycopg2.extensions import connection
from psycopg2.pool import SimpleConnectionPool
from typing import Any, List, Optional, Union
from configs import settings
from contextlib import contextmanager



CONNECTION_PARAMS: dict[str, Any] = {
    "database": settings.database.name,
    "user": settings.database.user,
    "password": settings.database.password,
    "port": settings.database.port,
    "host": settings.database.host,
    "cursor_factory": RealDictCursor
}


# Define the type of a result.
SingleResult = Union[RealDictRow | None]
MultiResult = List[RealDictRow]
DBResult = Union[SingleResult | MultiResult]


DATABASE_TABLE_LIST: list[str] = [

    """
        create table if not exists users(
            id serial primary key not null,
            fullname varchar(100) not null,
            email_id varchar(100) not null unique,
            password varchar(500) not null,
            role varchar(20) not null default 'trainee',
            created_at timestamp not null default now()
        );
    """,
    """
        create table if not exists courses(
            id serial primary key not null,
            name varchar(200) not null,
            description varchar not null,
            author varchar(200) not null,
            created_at timestamp not null default now()
        );
    """,

    """
        create table if not exists modules(
            id serial primary key not null,
            name varchar(200) not null,
            course_id integer references courses(id) not null,
            created_at timestamp not null default now()
        );
    """,

    """
        create table if not exists resources(
            id serial primary key not null,
            name varchar(200) not null,
            type varchar(200) not null,
            file_type varchar(200) not null,
            url varchar not null,
            module_id integer references modules(id) not null,
            created_at timestamp not null default now()
        );
    """,
    """
        create table if not exists enrollments(
            id serial primary key not null,
            user_id integer references users(id) not null,
            course_id integer references courses(id) not null,
            enrolled_at timestamp not null default now(),
            unique(user_id, course_id)
        );
    """

]

class DBManager:

    def __init__(self):
        self._pool: Optional[SimpleConnectionPool] = None 

    
    def init_database_pool(self, minconn: int = 5, maxconn: int = 15):
        try:
            self._pool = SimpleConnectionPool(
                minconn = minconn,
                maxconn = maxconn,
                **CONNECTION_PARAMS 
            )
            print("DB Pool Initialized.")

        except Exception as e:
            print(f"FATAL: Database connection failed {str(e)}")
            raise 
    
    def close_database_pool(self):
        if self._pool is not None:
            self._pool.closeall()
            print("Database Pool closed.")
            self._pool = None 


    def init_db_tables(self) -> None: 
        for table_schema in DATABASE_TABLE_LIST:
            self.execute_sql_command(table_schema, fetch = False)
        
        print("All tables created successfully.")


    @contextmanager
    def get_connection(self):
        if self._pool is None:
            raise RuntimeError("Database is not initialized.")
        conn: connection = self._pool.getconn()
        try:
            yield conn 
        finally:
            self._pool.putconn(conn)


    def execute_select_statement(
        self,
        sql: str,
        vars: Optional[dict] = None,
        fetch_all: bool = True
    ) -> DBResult:
        
        with self.get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, vars)
                if fetch_all:
                    return cur.fetchall()
                return cur.fetchone()
            

    def execute_sql_command(
        self,
        sql: str,
        vars: Optional[dict] = None,
        fetch: bool = True
    ) -> SingleResult:
        
        conn = None 
        result: SingleResult = None 

        try:
            with self.get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, vars) 
                    if fetch:
                        result = cur.fetchone()
                conn.commit()
            return result 
        
        except Exception as e:
            print(f"Unexpected Error Occur: {str(e)}")
            if conn:
                conn.rollback()
            raise e
        
       

db_manager = DBManager()        
     

