/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 21:06:33
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package service

import (
	"irisdemo/commons"
	"irisdemo/models"

	"github.com/prometheus/common/log"
)

type ClassService interface {
	List(limit uint, offset uint) (result models.ResBody)
	Create(class models.Classes) (result models.ResBody)
	Update(id string, class models.Classes) (result models.ResBody)
	Retrieve(id string) (result models.ResBody)
	Destory(id string) (result models.ResBody)
}

type classService struct{}

func NewClassService() *classService {
	return &classService{}
}

var classEntity = models.NewClassEntity()

func (t *classService) List(limit uint, offset uint) (result models.ResBody) {
	total, class := classEntity.ClassList(limit, offset)
	maps := make(map[string]interface{}, 10)
	maps["Total"] = total
	maps["List"] = class
	result.Data = maps
	result.Flag = true
	return
}

func (t *classService) Create(class models.Classes) (result models.ResBody) {
	res := classEntity.NameDuplicated("", class.Name)
	if res {
		result.Flag = false
		result.Data = commons.ErrorsMap["NameDuplicated"]
		return
	}
	err := classEntity.AddClass(class)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["InsertError"]
	} else {
		result.Flag = true
		result.Data = class
	}
	return
}

func (t *classService) Update(id string, class models.Classes) (result models.ResBody) {
	res := classEntity.NameDuplicated(id, class.Name)
	if res {
		result.Flag = false
		result.Data = commons.ErrorsMap["NameDuplicated"]
		return
	}
	err := classEntity.UpdateClass(id, class)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["UpdateError"]
		log.Errorf("Update class Error:%v", err)
	} else {
		result.Flag = true
		class.Id = id
		result.Data = class
	}
	return
}

func (n *classService) Retrieve(id string) (result models.ResBody) {
	var class models.Classes
	var err error
	class, err = classEntity.GetClass(id)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["RetrieveError"]
	} else {
		result.Flag = true
		result.Data = class
	}
	return
}

func (t *classService) Destory(id string) (result models.ResBody) {
	err := classEntity.DelClass(id)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["DeleteError"]
	} else {
		result.Flag = true
		result.Data = models.Classes{}
	}
	return
}
