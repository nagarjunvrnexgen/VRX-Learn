from database import db_manager, SingleResult,DBResult
from psycopg2.extras import RealDictRow
import schemas



def get_all_resources() -> DBResult:
    
    sql: str = """select * from resources;"""
    resources = db_manager.execute_select_statement(sql)

    return resources


def get_resource_by_id(id: int) -> SingleResult:
    
    sql: str = "select * from resources where id = %(id)s;"

    requested_resource = db_manager.execute_select_statement(
        sql, 
        {"id": id},
        fetch_all = False
    )

    return requested_resource


def get_resource_by_name_and_module_id(
    name: str,
    module_id: int
) -> SingleResult:
    
    sql: str = """select * from resources where name = %(name)s and module_id = %(module_id)s;"""
    
    resource = db_manager.execute_select_statement(
        sql,
        {
            "name": name,
            "module_id": module_id
        },
        fetch_all = False
    )
    
    return resource


def insert_resource(
    resource: schemas.ResourceCreate
) -> RealDictRow:
    
    sql: str = """
        insert into resources(
            name, type, file_type, url, module_id
        )
        values(
            %(name)s, %(type)s, %(file_type)s, %(url)s, %(module_id)s
        )
        returning *
        ;
    """

    new_resource: SingleResult = db_manager.execute_sql_command(
        sql, 
        resource.model_dump(),
        fetch = True
    )

    return new_resource




def delete_resource(id: int) -> SingleResult:
    sql: str = """delete from resources where id = %(id)s returning *;"""

    deleted_resource = db_manager.execute_sql_command(
        sql, 
        {"id": id},
        fetch = True
    )

    return deleted_resource


