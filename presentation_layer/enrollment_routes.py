from fastapi import APIRouter, HTTPException, status
import service_layer.enrollments as enrollment_services
import schemas
import exceptions


enrollment_router = APIRouter(
    prefix = "/enrollments",
    tags = ["Enrollments"]
)


@enrollment_router.get("/")
async def enrollments():
    return enrollment_services.list_all_enrollments()



@enrollment_router.get("/{enrollment_id}")
async def get_enrollment(enrollment_id: int):

    try:
        
        enrollment = enrollment_services.fetch_enrollment_by_id(
            schemas.EnrollmentId(id = enrollment_id)
        )
        return enrollment
    
    except exceptions.EnrollmentNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No enrollment found with this Id: {enrollment_id}."
        )
        



@enrollment_router.delete("/")
async def delete_enrollment(enrollment: schemas.EnrollmentId):
    try:
        
        deleted_enrollment = enrollment_services.remove_enrollment(enrollment)
        
        return deleted_enrollment
    
    except exceptions.EnrollmentNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No enrollment found with this Id: {enrollment.id}."
        )
    
@enrollment_router.post("/")
async def create_enrollment(enrollment: schemas.EnrollmentCreate):

    try:
    
        new_enrollment = enrollment_services.add_enrollment(enrollment)
        return new_enrollment

    except exceptions.UserNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No user found with this Id: {enrollment}"
        )
    
    except exceptions.CourseNotFoundError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"No course found with this Id: {enrollment.course_id}"
        )
    

    except exceptions.UserAlreadyEnrolledError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "Already enrolled in this course."
        )