from fastapi import APIRouter, HTTPException, status, Security
import schemas
import service_layer.courses as course_services
import exceptions
from presentation_layer.auth import get_current_admin_from_cookie


course_router = APIRouter(
    prefix = "/courses",
    tags = ["Courses"],
    dependencies = [Security(get_current_admin_from_cookie)] 
)



@course_router.get(
    "/", 
    response_model = list[schemas.Course]
)
async def courses():
    courses = course_services.list_all_courses()
    return courses


@course_router.get(
    "/{course_id}", 
    response_model = schemas.Course
)
async def get_course(course_id: int):
    try: 
        course = course_services.fetch_course_by_id(course_id) 

        return course
    
    except exceptions.CourseNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Course with Id {course_id} does not exist."
        )


@course_router.post(
    "/", 
    response_model = schemas.Course, 
    status_code = status.HTTP_201_CREATED
)
async def create_course(course: schemas.CourseCreate):
   
    new_course = course_services.add_course(course)

    return new_course



@course_router.delete(
    "/{course_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
async def delete_course(course_id: int):
    try:
        deleted_course = course_services.remove_course(course_id)
        return 
    
    except exceptions.CourseNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Course with Id {course_id} does not exist."
        )
    
