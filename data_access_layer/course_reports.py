import schemas
from database import db_manager, SingleResult, DBResult
from psycopg2.extras import RealDictRow



def get_enrolled_courses(
    user_id: int
) -> list[RealDictRow]:
    
    sql: str = """
        select 
            *
        from 
            courses as c
        join 
            enrollments as e
        on 
            c.id = e.course_id 
        where 
            e.user_id = %(user_id)s
        ;
    """
    
    enrolled_courses = db_manager.execute_select_statement(
        sql,
        {"user_id": user_id},
        fetch_all = True
    )
        
    return enrolled_courses


def get_all_courses() -> list[RealDictRow]:
    
    sql: str = """
        select 
            *
        from 
            courses as c
    """
    
    courses = db_manager.execute_select_statement(
        sql,
        fetch_all = True
    )
    
    return courses


def get_course_materials(
    course_id: int
) -> list[RealDictRow]:
    
    sql: str = """
        select
            c.id as course_id,
            c.name as course_name,
            c.author as course_author,
            m.id as module_id,
            m.name as module_name,
            r.id as resource_id,
            r.name as resource_name,
            r.type as resource_type,
            r.file_type as resource_file_type,
            r.url as file_id
        from 
            courses as c
        join 
            modules as m
        on 
            c.id = m.course_id
        join
            resources as r
        on 
            m.id = r.module_id
        where
            course_id = %(course_id)s
        ;
    """
    
    course_materials = db_manager.execute_select_statement(
        sql,
        {"course_id": course_id},
        fetch_all = True
    )
    
    return course_materials


