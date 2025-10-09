import schemas
from database import db_manager, SingleResult



def insert_course(course: schemas.CourseCreate):
    
    sql: str = """
        insert into courses(
            name, description, author
        )
        values(
            %(name)s, %(description)s, %(author)s
        )
        returning *
        ;
    """

    new_course = db_manager.execute_sql_command(
        sql, course.model_dump()
    )

    return new_course



def get_all_courses():

    sql: str = """
        select * from courses;
    """

    course = db_manager.execute_select_statement(sql)

    return course


def get_course(course: schemas.CourseID):
    
    sql: str = "select * from courses where id = %(id)s;"

    requested_course: SingleResult = db_manager.execute_select_statement(sql, course.model_dump(), fetch_all = False) #type: ignore

    return requested_course



def delete_course(course: schemas.CourseID):

    sql: str = "delete from courses where id = %(id)s returning * ;"

    deleted_course: SingleResult = db_manager.execute_sql_command(
        sql,
        course.model_dump(),
        fetch = True
    )

    return deleted_course

