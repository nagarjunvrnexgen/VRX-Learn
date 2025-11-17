import data_access_layer.courses as course_repo
from database import SingleResult
import schemas
import exceptions
from psycopg2.extras import RealDictRow
from psycopg2.errors import ForeignKeyViolation




def add_course(
    course: schemas.CourseCreate
) -> RealDictRow:

    # Need to implement duplicate course name check.
    existed_course = course_repo.get_course_by_name(course.name)
    if existed_course:
        raise exceptions.CourseNameAlreadyFoundError(
            f"Course already found with this name {course.name}"
        )
    
    new_course = course_repo.insert_course(course)
    
    return new_course



def remove_course(
    id: int
) -> RealDictRow:

    try:
        deleted_course = course_repo.delete_course(id)
    
        if not deleted_course:
            raise exceptions.CourseNotFoundError(
                f"Course with ID {id} does not exist"
            )
        
        return deleted_course
    
    except ForeignKeyViolation:
        raise exceptions.CourseHasModulesError(
            f"Course with ID {id} has associated modules and cannot be deleted"
        )


def fetch_course_by_id(
    id: int
) -> RealDictRow:

    requested_course = course_repo.get_course_by_id(id)

    if not requested_course:
        raise exceptions.CourseNotFoundError(
            f"Course with ID {id} does not exist"
        )
    
    return requested_course


def list_all_courses() -> list[RealDictRow]:
    
    courses = course_repo.get_all_courses()

    return courses



