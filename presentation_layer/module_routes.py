from fastapi import APIRouter, status, HTTPException
import service_layer.modules as module_services
import schemas
import exceptions

module_router = APIRouter(
    prefix = "/modules",
    tags = ["Modules"]
)


@module_router.get("/")
async def modules():
    return module_services.list_all_modules()


@module_router.get("/{module_id}")
async def get_module(module_id: int):
    try:
        requested_module = module_services.fetch_module(
            schemas.ModuleId(id = module_id)
        )
        return requested_module 
    
    except exceptions.CourseModuleNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No module found with this course id."
        )


@module_router.post("/new")
async def create_module(module: schemas.ModuleCreate):
    try:
        new_module = module_services.add_module(module)
        return new_module 
    
    except exceptions.CourseNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = "No course found with this course id."
        )
    

@module_router.delete("/{module_id}")
async def delete_module(module_id: int):
    try: 
        deleted_module = module_services.remove_module(
            schemas.ModuleId(
                id = module_id
            )
        ) 

        return deleted_module
    
    except exceptions.CourseModuleNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No module found with this Id: {module_id}"
        )



