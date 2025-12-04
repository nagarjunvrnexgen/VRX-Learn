import data_access_layer.enrollments as enrollement_repo
import service_layer.users as user_services
import service_layer.courses as course_services
import schemas
import exceptions
from psycopg2.extras import RealDictRow


def fetch_enrollment_by_id(
    id: int
) -> RealDictRow:
    
    requested_enrollment = enrollement_repo.get_enrollement_by_id(id)

    if not requested_enrollment:
        raise exceptions.EnrollmentNotFoundError(
            f"Enrollment with ID {id} does not exist"
        )
    
    return requested_enrollment




def fetch_enrollment_by_user_course(
    enrollement: schemas.EnrollmentLookUp
) -> RealDictRow:

    requested_enrollement = enrollement_repo.get_enrollment_by_user_course(enrollement)

    if not requested_enrollement:
        print("Enrollment not found")
        raise exceptions.EnrollmentNotFoundError(
            f"Enrollment with the given user ID {enrollement.user_id} and course ID {enrollement.course_id} does not exist"
        )
    
    return requested_enrollement




def list_all_enrollments() -> list[RealDictRow]:
    enrollments = enrollement_repo.get_all_enrollments()
    return enrollments



def add_enrollment(
    enrollment: schemas.EnrollmentCreate
) -> RealDictRow:

    # Check for User existance.
    user = user_services.fetch_user_by_id(enrollment.user_id)


    if not user:
        raise exceptions.UserNotFoundError(
            f"User with ID {enrollment.user_id} does not exist"
        )
    
    # Check the user role. 
    if user["role"] == "admin":
        raise exceptions.AdminEnrollmentNotAllowdedError(
            "Admin users are not allowed to enroll in courses"
        )
    
    # Check for course existance.
    course = course_services.fetch_course_by_id(enrollment.course_id)

    if not course:
        raise exceptions.CourseNotFoundError(
            f"Course with ID {enrollment.course_id} does not exist"
        )
    # Check for duplicate enrollment
    existed_enrollment = enrollement_repo.get_enrollment_by_user_course(enrollment)

    if existed_enrollment:
        raise exceptions.UserAlreadyEnrolledError(
            f"User with ID {enrollment.user_id} is already enrolled in course with ID {enrollment.course_id}"
        )
    
    new_enrollment = enrollement_repo.insert_enrollment(enrollment)

    return new_enrollment



def remove_enrollment(
    id: int
) -> RealDictRow:

    deleted_enrollment = enrollement_repo.delete_enrollment(id)

    if not deleted_enrollment:    
        raise exceptions.EnrollmentNotFoundError(
            f"Enrollment with ID {id} does not exist"
        )
    
    return deleted_enrollment 


def fetch_enrollments() -> list[RealDictRow]:
    
    enrollments = enrollement_repo.get_enrollments()
    
    return enrollments

