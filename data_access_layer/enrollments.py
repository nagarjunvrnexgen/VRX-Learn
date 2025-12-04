from database import db_manager, SingleResult, DBResult
from psycopg2.extras import RealDictRow
import schemas




def get_enrollement_by_id(id: int) -> SingleResult:

    sql: str = "select  * from enrollments where id = %(id)s;"
    requested_enrollment: SingleResult = db_manager.execute_select_statement(
        sql,
        {"id": id},
        fetch_all = False
    )

    return requested_enrollment


def get_enrollment_by_user_course(
    enrollment: schemas.EnrollmentLookUp
) -> SingleResult:
    
    sql: str =  "select * from enrollments where course_id = %(course_id)s and user_id = %(user_id)s;"

    course_enrollment: SingleResult = db_manager.execute_select_statement(
        sql, 
        enrollment.model_dump(),
        fetch_all = False
    )

    return course_enrollment



def get_all_enrollments() -> DBResult:
    
    sql: str =  """select * from enrollments;"""
    
    enrollments = db_manager.execute_select_statement(sql)

    return enrollments



def insert_enrollment(
    enrollment: schemas.EnrollmentCreate
) -> RealDictRow:
    
    sql: str = """
        insert into enrollments(
            user_id, course_id
        )
        values(
            %(user_id)s, %(course_id)s
        )
        returning *
        ;
    """

    new_enrollment = db_manager.execute_sql_command(
        sql,
        enrollment.model_dump(),
        fetch = True
    )

    return new_enrollment    


def delete_enrollment(id: int) -> SingleResult:

    sql: str = "delete from enrollments where id = %(id)s returning *;"

    deleted_enrollment = db_manager.execute_sql_command(
        sql,
        {"id": id},
        fetch = True
    )

    return deleted_enrollment


def get_enrollments() -> list[RealDictRow]:
    
    sql: str = """
        select
            e.id as id,
            u.id as user_id,
            u.fullname as username,
            c.id as course_id,
            c.name as course_name,
            e.enrolled_at as enrolled_at
        from 
            enrollments as e
        join 
            users as u 
        on 
            e.user_id = u.id
        join 
            courses as c
        on 
            e.course_id = c.id
        ;       
    """
    
    enrollments = db_manager.execute_select_statement(
        sql,
        fetch_all = True
    )
    
    return enrollments
