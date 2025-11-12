from fastapi import APIRouter, status, HTTPException, Security
import service_layer.modules as module_services
import schemas
import exceptions
from presentation_layer.auth import get_current_admin_from_cookie

module_router = APIRouter(
    prefix = "/modules",
    tags = ["Modules"],
    dependencies = [Security(get_current_admin_from_cookie)]
)


@module_router.get(
    "/",
    response_model = list[schemas.Module]
)
def get_modules():
    return module_services.list_all_modules()


@module_router.get(
    "/{module_id}",
    response_model = schemas.Module
)
def get_module(module_id: int):
    try:
        requested_module = module_services.fetch_module_by_id(module_id)
        return requested_module 
    
    except exceptions.CourseModuleNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Module with Id {module_id} does not exist"
        )


@module_router.post(
    "/",
    response_model = schemas.Module,
    status_code = status.HTTP_201_CREATED
)
def create_module(module: schemas.ModuleCreate):
    
    try:
        new_module = module_services.add_module(module)
        return new_module 
    
    except exceptions.CourseNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = f"Course with Id {module.course_id} does not exist"
        )
        
    except exceptions.ModuleNameAlreadyFoundError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = f"Module already found with the name {module.name} in the course."
        )
    

@module_router.delete(
    "/{module_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
def delete_module(module_id: int):
    try: 
        
        deleted_module = module_services.remove_module(module_id)
        return
    
    except exceptions.CourseModuleNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Module with Id {module_id} does not exist"
        )



