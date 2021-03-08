/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 21:33:19
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package service

import (
	"irisdemo/commons"
	"irisdemo/models"

	"github.com/prometheus/common/log"
)

type TeacherService interface {
	List(limit uint, offset uint) (result models.ResBody)
	Create(teacher models.Teachers) (result models.ResBody)
	Update(id string, teacher models.Teachers) (result models.ResBody)
	Retrieve(id string) (result models.ResBody)
	Destory(id string) (result models.ResBody)
}

type teacherService struct{}

func NewTeacherService() *teacherService {
	return &teacherService{}
}

var teacherEntity = models.NewTeacherEntity()

func (t *teacherService) List(limit uint, offset uint) (result models.ResBody) {
	total, teachers := teacherEntity.TeacherList(limit, offset)
	maps := make(map[string]interface{}, 10)
	maps["Total"] = total
	maps["List"] = teachers
	result.Data = maps
	result.Flag = true
	return
}

func (t *teacherService) Create(teacher models.Teachers) (result models.ResBody) {
	res := teacherEntity.NameDuplicated("", teacher.Name)
	if res {
		result.Flag = false
		result.Data = commons.ErrorsMap["NameDuplicated"]
		return
	}
	err := teacherEntity.AddTeacher(teacher)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["InsertError"]
	} else {
		result.Flag = true
		result.Data = teacher
	}
	return
}

func (t *teacherService) Update(id string, teacher models.Teachers) (result models.ResBody) {
	res := teacherEntity.NameDuplicated(id, teacher.Name)
	if res {
		result.Flag = false
		result.Data = commons.ErrorsMap["NameDuplicated"]
		return
	}
	err := teacherEntity.UpdateTeacher(id, teacher)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["UpdateError"]
		log.Errorf("Update Teacher Error:%v", err)
	} else {
		result.Flag = true
		teacher.Id = id
		result.Data = teacher
	}
	return
}

func (n *teacherService) Retrieve(id string) (result models.ResBody) {
	var teacher models.Teachers
	var err error
	teacher, err = teacherEntity.GetTeacher(id)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["RetrieveError"]
	} else {
		result.Flag = true
		result.Data = teacher
	}
	return
}

func (t *teacherService) Destory(id string) (result models.ResBody) {
	err := teacherEntity.DelTeacher(id)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["DeleteError"]
	} else {
		result.Flag = true
		result.Data = models.Teachers{}
	}
	return
}
