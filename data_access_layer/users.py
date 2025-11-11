import schemas
from database import db_manager, SingleResult, DBResult
from psycopg2.extras import RealDictRow


def standardize_email(email: str) -> str:
    
    return email.strip().lower()


def get_user_by_email(
    email_id: str
) -> SingleResult:
    
    sql: str = "select* from users where email_id = %(email_id)s;"
    user: SingleResult = db_manager.execute_select_statement(
        sql,
        {"email_id": standardize_email(email_id)},
        fetch_all = False
    )

    return user



def get_user_by_id(id: int) -> SingleResult:
    
    sql: str = "select* from users where id = %(id)s;"
    user: SingleResult = db_manager.execute_select_statement(
        sql,
        {"id": id},
        fetch_all = False
    )

    return user 



def get_all_users() -> DBResult:
    
    sql: str = "select * from users;"
    
    users = db_manager.execute_select_statement(sql)

    return users


def insert_user(
    user: schemas.UserCreate
) -> RealDictRow:
    
    sql: str = """
        insert into users(
            fullname, email_id, password, role
        )
        values(
            %(fullname)s, %(email_id)s, %(password)s, %(role)s
        )
        returning *
        ;
    """  

    # Strip the email id and lower case it for consistency.
    user.email_id = standardize_email(user.email_id)
    
    new_user: SingleResult = db_manager.execute_sql_command(
        sql,
        vars = user.model_dump(exclude = {"confirm_password"}),
        fetch = True
    )  # type: ignore;


    return new_user


    
def delete_user(id: int) -> SingleResult:

    sql: str = "delete from users where id = %(id)s returning * ;"

    deleted_user: SingleResult = db_manager.execute_sql_command(
        sql, 
        {"id": id},
        fetch = True
    )

    return deleted_user






