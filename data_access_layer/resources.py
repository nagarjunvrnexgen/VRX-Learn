from database import db_manager, SingleResult
import schemas



def get_all_resources():
    sql: str = """select * from resources;"""
    resources = db_manager.execute_select_statement(sql)

    return resources


def get_resource(resource: schemas.ResourceId):
    
    sql: str = "select * from resources where id = %(id)s;"

    requested_resource = db_manager.execute_select_statement(
        sql, resource.model_dump(),
        fetch_all = False
    )

    return requested_resource



def insert_resource(resource: schemas.ResourceCreate):
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




def delete_resource(resource: schemas.ResourceId):
    sql: str = """delete from resources where id = %(id)s returning *;"""

    deleted_resource = db_manager.execute_sql_command(
        sql, resource.model_dump(),
        fetch = True
    )

    return deleted_resource


