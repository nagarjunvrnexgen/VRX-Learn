import data_access_layer.course_reports as course_reports_repo
import data_access_layer.courses as courses_repo
import schemas
import exceptions
from psycopg2.extras import RealDictRow
import data_access_layer.enrollments as enrollments_repo



def fetch_enrolled_courses(user_id: int) -> list[RealDictRow]:
    
    return course_reports_repo.get_enrolled_courses(user_id)


def fetch_all_courses() -> list[RealDictRow]:
    
    return course_reports_repo.get_all_courses()



def fetch_course_materials(
    enrollment: schemas.EnrollmentLookUp
) -> list[RealDictRow]:
    
    # Check whether the course exist.
    course = courses_repo.get_course_by_id(enrollment.course_id)
    
    if not course:
        raise exceptions.CourseNotFoundError(
            f"Course with Id {enrollment.course_id} does not exist"
        )
    
    # Check whether the user is enrolled in the course.
    enrolled_course = enrollments_repo.get_enrollment_by_user_course(enrollment)
    
    if not enrolled_course:
        raise exceptions.UserNotEnrolledError(
            f"User with id {enrollment.user_id} is not enrolled in the course with id {enrollment.course_id}"
        )
        
    return course_reports_repo.get_course_materials(enrollment.course_id)
    

