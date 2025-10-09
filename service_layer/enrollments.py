import data_access_layer.enrollments as enrollement_repo
import service_layer.users as user_services
import service_layer.courses as course_services
import schemas
import exceptions



def fetch_enrollment_by_id(enrollment: schemas.EnrollmentId):
    
    requested_enrollment = enrollement_repo.get_enrollement_by_id(enrollment)

    if not requested_enrollment:
        raise exceptions.EnrollmentNotFoundError(
            f"No enrollment found with this Id: {enrollment.id}"
        )
    
    return requested_enrollment




def fetch_enrollment_by_user_course(enrollement: schemas.EnrollmentLookUp):

    requested_enrollement = enrollement_repo.get_enrollment_by_user_course(enrollement)

    if not requested_enrollement:
        print("Enrollment not found")
        raise exceptions.EnrollmentNotFoundError(
            "No enrollment found with this user id and course id."
        )
    
    return requested_enrollement




def list_all_enrollments():
    enrollments = enrollement_repo.get_all_enrollments()
    return enrollments



def add_enrollment(enrollment: schemas.EnrollmentCreate):

    # Check for User existance.
    user = user_services.fetch_user_by_id(enrollment.user_id)

    if not user:
        raise exceptions.UserNotFoundError(
            "No user found with this Id."
        )
    
    # Check for course existance.

    course = course_services.fetch_course(
        schemas.CourseID(id = enrollment.course_id)
    )

    if not course:
        raise exceptions.CourseNotFoundError(
            "No course found with this Id"
        )
    # Check for duplicate enrollment
    existed_enrollment = enrollement_repo.get_enrollment_by_user_course(enrollment)

    if existed_enrollment:
        raise exceptions.UserAlreadyEnrolledError(
            "User already enrolled in this course"
        )
    
    new_enrollment = enrollement_repo.insert_enrollment(enrollment)

    return new_enrollment



def remove_enrollment(enrollment: schemas.EnrollmentId):

    deleted_enrollment = enrollement_repo.delete_enrollment(enrollment)

    if not deleted_enrollment:    
        raise exceptions.EnrollmentNotFoundError(
            f"No enrollment found with this Id: {enrollment.id}"
        )
    
    return deleted_enrollment 

