from database import SingleResult, db_manager
import schemas


def insert_module(module: schemas.ModuleCreate): 
    sql: str = """
        insert into modules(
            name, course_id
        )
        values(
            %(name)s, %(course_id)s
        )
        returning *
        ;
    """
    new_module: SingleResult = db_manager.execute_sql_command(
        sql, module.model_dump(), fetch = True
    )

    return new_module


    
def delete_module(module: schemas.ModuleId):
    
    sql: str = """delete from modules where id = %(id)s returning *;"""
    
    deleted_module = db_manager.execute_sql_command(
        sql, module.model_dump(),
        fetch = True
    )

    return deleted_module


def get_module(module: schemas.ModuleId):
    sql: str = "select * from modules where id = %(id)s;"

    requested_module: SingleResult = db_manager.execute_select_statement(
        sql, module.model_dump(),
        fetch_all = False
    ) #type: ignore

    return requested_module


def get_all_modules():
    sql: str = """select * from modules;"""
    
    modules = db_manager.execute_select_statement(sql)

    return modules




