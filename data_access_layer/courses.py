import schemas
from database import db_manager, SingleResult, DBResult
from psycopg2.extras import RealDictRow


def insert_course(course: schemas.CourseCreate) -> RealDictRow:
    
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



def get_all_courses() -> DBResult:

    sql: str = """
        select * from courses;
    """

    course = db_manager.execute_select_statement(sql, fetch_all = True)

    return course


def get_course_by_id(id: int) -> SingleResult:
    
    sql: str = "select * from courses where id = %(id)s;"

    requested_course: SingleResult = db_manager.execute_select_statement(
        sql, 
        {"id": id}, 
        fetch_all = False
    )

    return requested_course



def delete_course(id: int) -> SingleResult:

    sql: str = "delete from courses where id = %(id)s returning * ;"

    deleted_course: SingleResult = db_manager.execute_sql_command(
        sql,
        {"id": id},
        fetch = True
    )

    return deleted_course

