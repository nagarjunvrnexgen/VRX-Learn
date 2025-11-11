import data_access_layer.modules as module_repo
from service_layer.courses import fetch_course_by_id
import schemas
import exceptions
from psycopg2.extras import RealDictRow



def fetch_module_by_id(
    id: int
) -> RealDictRow:

    requested_module = module_repo.get_module_by_id(id)
    
    if not requested_module:
        raise exceptions.CourseModuleNotFoundError(
            f"Module with ID {id} does not exist"
        )

    return requested_module


def list_all_modules() -> list[RealDictRow]:

    modules = module_repo.get_all_modules()

    return modules


def add_module(
    module: schemas.ModuleCreate
) -> RealDictRow:

    # Check course exist with given course id.
    course_to_add_module = fetch_course_by_id(module.course_id)

    if not course_to_add_module:
        raise exceptions.CourseNotFoundError(
            f"Course with ID {module.course_id} does not exist"
        )
    
    new_module = module_repo.insert_module(module)

    return new_module



def remove_module(
    id: int
) -> RealDictRow:
    
    deleted_module = module_repo.delete_module(id)

    if not deleted_module:
        raise exceptions.CourseModuleNotFoundError(
            f"Module with ID {id} does not exist"
        )

    return deleted_module



