import data_access_layer.courses as course_repo
import schemas
import exceptions
from psycopg2.extras import RealDictRow



def add_course(
    course: schemas.CourseCreate
) -> RealDictRow:

    # Need to implement duplicate course name check.
    try: 
        new_course = course_repo.insert_course(course)
        return new_course
    
    except Exception as e:
        print(f"Unexpected Error occur: {str(e)}")



def remove_course(
    id: int
) -> RealDictRow:

    deleted_course = course_repo.delete_course(id)
    
    if not deleted_course:
        raise exceptions.CourseNotFoundError(
            f"Course with ID {id} does not exist"
        )
    
    return deleted_course


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



