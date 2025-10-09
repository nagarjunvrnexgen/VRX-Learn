import data_access_layer.courses as course_repo
import schemas
import exceptions



def add_course(course: schemas.CourseCreate):

    try: 
        new_course = course_repo.insert_course(course)
        return new_course
    
    except Exception as e:
        print(f"Unexpected Error occur: {str(e)}")



def remove_course(course: schemas.CourseID):

    deleted_course = course_repo.delete_course(course)
    
    if not deleted_course:
        raise exceptions.CourseNotFoundError(
            "No course found with this ID"
        )
    
    return deleted_course


def fetch_course(course: schemas.CourseID):

    requested_course = course_repo.get_course(course)

    if not requested_course:
        raise exceptions.CourseNotFoundError(
            f"No course found with this ID: {course.id}"
        )
    
    return requested_course


def list_all_courses():
    
    courses = course_repo.get_all_courses()

    return courses



