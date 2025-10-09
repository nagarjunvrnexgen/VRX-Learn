import data_access_layer.resources as resource_repo 
import data_access_layer.modules as module_repo
import schemas
import exceptions


def list_all_resource():
    resources = resource_repo.get_all_resources()
    return resources


def fetch_resource(resource: schemas.ResourceId):
    
    requested_resource = resource_repo.get_resource(resource)

    if not requested_resource:
        raise exceptions.ResourceNotFoundError(
            f"No resource found with this Id: {resource.id}"
        ) 
    
    return requested_resource




def add_resource(resource: schemas.ResourceCreate):
    
    # Check the module exist. 
    module = module_repo.get_module(
        schemas.ModuleId(id = resource.module_id)
    )

    if not module:
        raise exceptions.CourseModuleNotFoundError(
            f"No Module found with this Id: {resource.module_id}"
        )
    
    new_resource = resource_repo.insert_resource(resource)

    return new_resource



def remove_resource(resource: schemas.ResourceId):

    deleted_resource = resource_repo.delete_resource(resource)

    if not deleted_resource:
        raise exceptions.ResourceNotFoundError(
            f"No resource found with this Id: {resource.id}"
        )
    
    return deleted_resource





