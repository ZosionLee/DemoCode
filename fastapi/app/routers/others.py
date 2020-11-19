# * coding:utf-8 *
# Author: ZosionLee


from starlette.responses import Response
from app.depends import ClassDepends, CourseDepends, TeacherDepends
from common.orms import ClassORM, CourseORM, TeacherORM
from common.schema import ClassModel, CourseModel, TeacherModel
from fastapi import APIRouter, Depends, status

router = APIRouter()


@router.post(
    '/classes',
    dependencies=[Depends(ClassDepends.name_duplicated)]
)
async def create_class(cla: ClassModel):
    ClassORM.create_class(cla)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    '/teachers',
    dependencies=[Depends(TeacherDepends.name_duplicated)]
)
async def create_teacher(tea: TeacherModel):
    TeacherORM.create_teacher(tea)
    return Response(status_code=status.HTTP_200_OK)


@router.post(
    '/courses',
    dependencies=[Depends(CourseDepends.name_duplicated)]
)
async def create_course(cou: CourseModel):
    CourseORM.create_course(cou)
    return Response(status_code=status.HTTP_200_OK)
