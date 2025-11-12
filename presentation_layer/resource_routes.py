from fastapi import APIRouter, HTTPException, status, Security 
import service_layer.resources as resource_services
import schemas
import exceptions
from presentation_layer.auth import get_current_admin_from_cookie

resource_router = APIRouter(
    prefix = "/resources",
    tags = ["Resources"],
    dependencies = [Security(get_current_admin_from_cookie)]
)


@resource_router.get(
    "/",
    response_model = list[schemas.Resource],
)
def get_resources():    
    resources = resource_services.list_all_resource()
    return resources



@resource_router.get(
    "/{resource_id}",
    response_model = schemas.Resource
)
def get_resource(resource_id: int):
    
    try: 
        resource = resource_services.fetch_resource_by_id(resource_id)
        return resource
    
    except exceptions.ResourceNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Resource with Id {resource_id} does not exist"
        )


@resource_router.post(
    "/", 
    response_model = schemas.Resource,
    status_code = status.HTTP_201_CREATED
)
def create_resource(resource: schemas.ResourceCreate):
    
    try: 
        
        new_resource = resource_services.add_resource(resource)
        return new_resource
    

    except exceptions.CourseModuleNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Module with Id {resource.module_id} does not exist"
        )
    

@resource_router.delete(
    "/{resource_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_resource(resource_id: int):
    
    try:
        
        deleted_resource = resource_services.remove_resource(resource_id)
        return 
    
    except exceptions.ResourceNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Resource with Id {resource_id} does not exist"
        )

