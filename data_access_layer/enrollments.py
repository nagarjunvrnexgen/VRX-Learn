from database import db_manager, SingleResult
import schemas




def get_enrollement_by_id(enrollment: schemas.EnrollmentId):

    sql: str = "select  * from enrollments where id = %(id)s;"
    requested_enrollment: SingleResult = db_manager.execute_select_statement(
        sql,
        enrollment.model_dump(),
        fetch_all = False
    )

    return requested_enrollment


def get_enrollment_by_user_course(enrollment: schemas.EnrollmentLookUp):
    
    sql: str =  "select * from enrollments where course_id = %(course_id)s and user_id = %(user_id)s;"

    course_enrollment: SingleResult = db_manager.execute_select_statement(
        sql, 
        enrollment.model_dump(),
        fetch_all = False
    )

    return course_enrollment



def get_all_enrollments():
    
    sql: str =  """select * from enrollments;"""
    
    enrollments = db_manager.execute_select_statement(sql)

    return enrollments



def insert_enrollment(enrollment: schemas.EnrollmentCreate):
    
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


def delete_enrollment(enrollment: schemas.EnrollmentId):

    sql: str = "delete from enrollments where id = %(id)s returning *;"

    deleted_enrollment = db_manager.execute_sql_command(
        sql,
        enrollment.model_dump(),
        fetch = True
    )

    return deleted_enrollment

