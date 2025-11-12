import service_layer.course_reports as course_report_services
from presentation_layer.auth import get_current_user_from_cookie
from fastapi import Security, APIRouter, HTTPException, status
from typing import Annotated
import schemas  
import exceptions


course_reports_router = APIRouter(
    prefix = "",
    tags = ["Course Reports"]
)



@course_reports_router.get(
    "/my_courses", 
    response_model = list[schemas.Course]
)
def get_enrolled_couses(
    user: Annotated[
        schemas.TokenData,
        Security(get_current_user_from_cookie)
    ]
):
    return course_report_services.fetch_enrolled_courses(user.user_id)
    


@course_reports_router.get(
    "/all_courses", 
    response_model = list[schemas.Course]
)
def get_all_courses(
    user: Annotated[
        schemas.TokenData,
        Security(get_current_user_from_cookie)
    ]
):
    return course_report_services.fetch_all_courses()


@course_reports_router.get(
    "/course_materials/{course_id}"
)
def get_course_materials(
    course_id: int,
    user: Annotated[
        schemas.TokenData,
        Security(get_current_user_from_cookie)
    ]
):
    
    try: 
        
        course_materials = course_report_services.fetch_course_materials(
            schemas.EnrollmentLookUp(
                user_id = user.user_id,
                course_id = course_id
            )
        ) 
        return course_materials
    
    except exceptions.CourseNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Course with id {course_id} does not exist"
        )
    
    except exceptions.UserNotEnrolledError:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "User is not enrolled in the course"
        )
        