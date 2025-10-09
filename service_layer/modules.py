import data_access_layer.modules as module_repo
from service_layer.courses import fetch_course
import schemas
import exceptions



def fetch_module(module: schemas.ModuleId):

    requested_module = module_repo.get_module(module)
    
    if not requested_module:
        raise exceptions.CourseModuleNotFoundError(
            f"No Module found with this ID: {module.id}"
        )

    return requested_module


def list_all_modules():

    modules = module_repo.get_all_modules()

    return modules


def add_module(module: schemas.ModuleCreate):

    # Check course exist with given course id.
    course_to_add_module = fetch_course(
        schemas.CourseID(id = module.course_id)
    )

    if not course_to_add_module:
        raise exceptions.CourseNotFoundError(
            f"No course found with this ID: {module.course_id}"
        )
    
    new_module = module_repo.insert_module(module)

    return new_module



def remove_module(module: schemas.ModuleId):
    
    deleted_module = module_repo.delete_module(module)

    if not deleted_module:
        raise exceptions.CourseModuleNotFoundError(
            f"No module found with this ID: {module.id}"
        )

    return deleted_module



