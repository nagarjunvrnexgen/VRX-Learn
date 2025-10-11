import schemas
from database import db_manager, SingleResult




def get_user_by_email(email_id: str) -> SingleResult:
    sql: str = "select* from users where email_id = %(email_id)s;"
    user: SingleResult = db_manager.execute_select_statement(
        sql,
        {"email_id": email_id},
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

def get_user(
    user_detail: (
        schemas.UserGetById | 
        schemas.UserGetByEmail
    )
) -> SingleResult:
    
    email_sql: str = "select * from users where email_id = %(email_id)s;"
    id_sql: str = "select * from users where id = %(id)s;"

    sql: str = email_sql if isinstance(user_detail, schemas.UserGetByEmail) else id_sql
    
    user = db_manager.execute_select_statement(
        sql, 
        vars = user_detail.model_dump(),
        fetch_all = False 
    )

    return user



def get_all_users():
    sql: str = "select * from users;"
    
    users = db_manager.execute_select_statement(sql)

    return users


def insert_user(
    user: schemas.UserCreate
):
    
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

    new_user: SingleResult = db_manager.execute_sql_command(
        sql,
        vars = user.model_dump(exclude = {"confirm_password"}),
        fetch = True
    )  # type: ignore;


    return new_user


    
def delete_user(user: schemas.UserId):

    sql: str = "delete from users where id = %(id)s returning * ;"

    deleted_user: SingleResult = db_manager.execute_sql_command(sql, user.model_dump())

    return deleted_user






