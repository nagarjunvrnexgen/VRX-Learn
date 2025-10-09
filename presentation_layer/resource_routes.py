from fastapi import APIRouter, HTTPException, status 
import service_layer.resources as resource_services
import schemas
import exceptions


resource_router = APIRouter(
    prefix = "/resources",
    tags = ["Resources"]
)


@resource_router.get("/")
async def get_resources():    
    resources = resource_services.list_all_resource()
    return resources



@resource_router.get("/{resource_id}")
async def get_resource(resource_id: int):
    
    try: 
        resource = resource_services.fetch_resource(
            schemas.ResourceId(id = resource_id)
        )
        return resource
    
    except exceptions.ResourceNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No resource found with this Id: {resource_id}"
        )


@resource_router.post("/")
async def create_resource(resource: schemas.ResourceCreate):
    
    try: 
        
        new_resource = resource_services.add_resource(resource)
        return new_resource
    

    except exceptions.CourseModuleNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No Module found with this Id: {resource.module_id}"
        )
    

@resource_router.delete("/{resource_id}")
async def delete_resource(resource_id: int):
    
    try:
        deleted_resource = resource_services.remove_resource(
            schemas.ResourceId(id = resource_id)
        )
        return deleted_resource 
    
    except exceptions.ResourceNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No resource found with this Id: {resource_id}"
        )

