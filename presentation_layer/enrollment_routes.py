from fastapi import APIRouter, HTTPException, status, Security
import service_layer.enrollments as enrollment_services
import schemas
import exceptions
from presentation_layer.auth import get_current_admin_from_cookie



enrollment_router = APIRouter(
    prefix = "/enrollments",
    tags = ["Enrollments"],
    dependencies = [Security(get_current_admin_from_cookie)]
)


@enrollment_router.get(
    "/",
    response_model = list[schemas.Enrollment]
)
async def enrollments():
    return enrollment_services.list_all_enrollments()



@enrollment_router.get(
    "/{enrollment_id}",
    response_model = schemas.Enrollment
)
async def get_enrollment(enrollment_id: int):

    try:
        
        enrollment = enrollment_services.fetch_enrollment_by_id(enrollment_id)
        return enrollment
    
    except exceptions.EnrollmentNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Enrollment with Id {enrollment_id} does not exist."
        )
        



@enrollment_router.delete(
    "/{enrollment_id}",
    status_code = status.HTTP_204_NO_CONTENT
)
async def delete_enrollment(
    enrollment_id: int
):
    try:
        
        deleted_enrollment = enrollment_services.remove_enrollment(enrollment_id)
        
        return
    
    except exceptions.EnrollmentNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Enrollment with Id {enrollment_id} does not exist"
        )

    
@enrollment_router.post(
    "/",
    response_model = schemas.Enrollment,
    status_code = status.HTTP_201_CREATED
)
async def create_enrollment(enrollment: schemas.EnrollmentCreate):

    try:
    
        new_enrollment = enrollment_services.add_enrollment(enrollment)
        return new_enrollment

    except exceptions.UserNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"User with Id {enrollment.user_id} does not exist"
        )
    
    except exceptions.CourseNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Course with Id {enrollment.course_id} does not exist"
        )
    

    except exceptions.UserAlreadyEnrolledError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User is already enrolled in this course"
        )
    
    except exceptions.AdminEnrollmentNotAllowdedError:
        raise HTTPException(
            status_code = status.HTTP_403_FORBIDDEN,
            detail = "Admin users cannot be enrolled in courses"
        )