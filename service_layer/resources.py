import data_access_layer.resources as resource_repo 
import data_access_layer.modules as module_repo
import schemas
import exceptions
from psycopg2.extras import RealDictRow



def list_all_resource() -> list[RealDictRow]:
    resources = resource_repo.get_all_resources()
    return resources


def fetch_resource_by_id(
    id: int
) -> RealDictRow:
    
    requested_resource = resource_repo.get_resource_by_id(id)

    if not requested_resource:
        raise exceptions.ResourceNotFoundError(
            f"Resource with ID {id} does not exist"
        ) 
    
    return requested_resource




def add_resource(
    resource: schemas.ResourceCreate
) -> RealDictRow:
    
    # Check the module exist. 
    module = module_repo.get_module_by_id(
        resource.module_id
    )
    
    if not module:
        raise exceptions.CourseModuleNotFoundError(
        f"Module with ID {resource.module_id} does not exist"
    )
        
    # Check the resource name already exist in module.
    existed_resource = resource_repo.get_resource_by_name_and_module_id(
        name = resource.name,
        module_id = resource.module_id
    )
    
    if existed_resource:
        raise exceptions.ResourceNameAlreadyFoundError(
            f"Resource already found with the name {resource.name} in this module"
        )
    
    new_resource = resource_repo.insert_resource(resource)

    return new_resource



def remove_resource(
    id: int
) -> RealDictRow:

    deleted_resource = resource_repo.delete_resource(id)

    if not deleted_resource:
        raise exceptions.ResourceNotFoundError(
            f"Resource with ID {id} does not exist"
        )
    
    return deleted_resource





