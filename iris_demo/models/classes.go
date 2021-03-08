/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 20:01:36
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package models

import (
	"irisdemo/commons"
	"log"
)

type Classes struct {
	Id   string `gorm:"primaryKey"`
	Name string
}

type classEntity struct{}

func NewClassEntity() *classEntity {
	return &classEntity{}
}

type IClassEntity interface {
	ClassList(limit uint, offset uint) (total int, classs []Classes)
	AddClass(Classs Classes) (err error)
	UpdateClass(id, string, classs Classes) (err error)
	GetClass(id string) (classs Classes, err error)
	DelClass(id string) (err error)

	NameDuplicated(id, string, name string) (result bool)
}

func (t *classEntity) ClassList(limit uint, offset uint) (total int, class []Classes) {
	commons.DbClient.Model(Classes{}).Count(&total)
	err := commons.DbClient.Limit(limit).Offset(offset).Find(&class).Error
	if err != nil {
		log.Fatalf("List Classes error:%v\n", err)
		panic("select Error")
	}
	return
}

func (t *classEntity) AddClass(class Classes) (err error) {
	return commons.DbClient.Create(&class).Error
}

func (t *classEntity) UpdateClass(id string, class Classes) (err error) {
	return commons.DbClient.Model(Classes{}).Where("id=?", id).Update(&class).Error
}

func (t *classEntity) GetClass(id string) (class Classes, err error) {
	err = commons.DbClient.Find(&class, "id=?", id).Error
	return
}

func (t *classEntity) NameDuplicated(id string, name string) (result bool) {
	var count int32
	if id == "" {
		commons.DbClient.Model(Classes{}).Where("name=?", name).Count(&count)
	} else {
		commons.DbClient.Model(Classes{}).Where("id <>? and name=? ", id, name).Count(&count)
	}
	if count > 0 {
		result = true
	} else {
		result = false
	}
	return
}

func (t classEntity) DelClass(id string) (err error) {
	var Class Classes
	Class.Id = id
	err = commons.DbClient.Delete(&Class).Error
	return
}
