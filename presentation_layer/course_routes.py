from fastapi import APIRouter, HTTPException, status
import schemas
import service_layer.courses as course_services
import exceptions



course_router = APIRouter(
    prefix = "/course",
    tags = ["Courses"] 
)



@course_router.get("/")
async def courses():
    courses = course_services.list_all_courses()
    return courses


@course_router.get("/{course_id}")
async def get_course(course_id: int):
    try: 
        course = course_services.fetch_course(
            schemas.CourseID(id = course_id)
        ) 

        return course
    
    except exceptions.CourseNotFoundError: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No course found with this Id: {course_id}"
        )


@course_router.post("/new")
async def create_course(course: schemas.CourseCreate):
   
    new_course = course_services.add_course(course)

    return new_course



@course_router.delete("/{course_id}")
async def delete_course(course_id: int):
    
    try:
        deleted_course = course_services.remove_course(
            schemas.CourseID(id=course_id)
        )
        return deleted_course
    
    except exceptions.CourseNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "No course found with this ID"
        )
    
