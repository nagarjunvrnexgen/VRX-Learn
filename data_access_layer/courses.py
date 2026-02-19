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



def get_course_by_name(name: str) -> SingleResult:
    
    sql: str = "select * from courses where name = %(name)s;"

    course = db_manager.execute_select_statement(
        sql,
        {"name": name},
        fetch_all = False
    )
    print(course)
    return course 


def delete_course(id: int) -> SingleResult:

    sql: str = "delete from courses where id = %(id)s returning * ;"

    deleted_course: SingleResult = db_manager.execute_sql_command(
        sql,
        {"id": id},
        fetch = True
    )

    return deleted_course


def get_modules_and_resources_by_course_id(
    course_id:  int
) -> list[RealDictRow]:
    
    sql: str = """
        select  
            c.id as id,
            c.name as name,
            c.author as author,
            c.description as description,
            m.id as module_id,
            m.name as module_name,
            r.id as resource_id,
            r.name as resource_name,
            r.type as resource_type,
            r.file_type as resource_file_type,
            r.url as resource_url
        from 
            courses as c
        left join 
            modules as m 
        on 
            c.id = m.course_id
        left join 
            resources as r 
        on 
            m.id = r.module_id
        where 
            c.id = %(course_id)s
        ;
    """
    
    modules_and_resources = db_manager.execute_select_statement(
        sql,
        {"course_id": course_id},
        fetch_all = True
    )
    
    
    return modules_and_resources
