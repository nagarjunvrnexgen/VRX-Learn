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



def fetch_modules_and_resource_by_course_id(
    course_id: int
) -> list[RealDictRow]:
    
    # check whether the course exist.
    course = course_repo.get_course_by_id(course_id)
    
    if not course:
        raise exceptions.CourseNotFoundError(
            f"Course with Id {course_id} does not exist"
        )
        
    
    def build_course_structure(data: list[RealDictRow]):
        course = None 
        modules: dict = {}
        
        # Prepare course only once.
        for d in data:
            if not course:
                course = {
                    "id": d["id"],
                    "name": d["name"],
                    "author": d["author"],
                    "description": d["description"]
                }
            
            module_id = d["module_id"]
            if module_id not in modules:
                modules[module_id] = {
                    "id": module_id,
                    "name": d["module_name"],
                    "resources": [] # Initally empty list.
                }        

            resource_id = d["resource_id"]
            resource = {
                "id": resource_id,
                "name": d["resource_name"],
                "file_type": d["resource_file_type"],
                "type": d["resource_type"],
                "url": d["resource_url"]
            }
            
            modules[module_id]["resources"].append(resource)
            
        course["modules"] = list(modules.values())
            
        return course
    
    modules_and_resources = course_repo.get_modules_and_resources_by_course_id(course_id)
    
    modules_and_resources = build_course_structure(modules_and_resources) if modules_and_resources else {}
    
    return modules_and_resources



