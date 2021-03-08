/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 19:39:11
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package models

import (
	"irisdemo/commons"
	"log"
)

type Teachers struct {
	Id   string `gorm:"primaryKey"`
	Name string
}

type TeacherEntity struct{}

func NewTeacherEntity() *TeacherEntity {
	return &TeacherEntity{}
}

type ITeacherEntity interface {
	TeacherList(limit uint, offset uint) (total int, teachers []Teachers)
	AddTeacher(teachers Teachers) (err error)
	UpdateTeacher(id, string, teachers Teachers) (err error)
	GetTeacher(id string) (teachers Teachers, err error)
	DelTeacher(id string) (err error)

	NameDuplicated(id, string, name string) (result bool)
}

func (t *TeacherEntity) TeacherList(limit uint, offset uint) (total int, teachers []Teachers) {
	commons.DbClient.Model(Teachers{}).Count(&total)
	err := commons.DbClient.Limit(limit).Offset(offset).Find(&teachers).Error
	if err != nil {
		log.Fatalf("List Teachers error:%v\n", err)
		panic("select Error")
	}
	return
}

func (t *TeacherEntity) AddTeacher(teacher Teachers) (err error) {
	return commons.DbClient.Create(&teacher).Error
}

func (t *TeacherEntity) UpdateTeacher(id string, teacher Teachers) (err error) {
	return commons.DbClient.Model(Teachers{}).Where("id=?", id).Update(&teacher).Error
}

func (t *TeacherEntity) GetTeacher(id string) (teacher Teachers, err error) {
	err = commons.DbClient.Find(&teacher, "id=?", id).Error
	return
}

func (t *TeacherEntity) NameDuplicated(id string, name string) (result bool) {
	var count int32
	if id == "" {
		commons.DbClient.Model(Teachers{}).Where("name=?", name).Count(&count)
	} else {
		commons.DbClient.Model(Teachers{}).Where("id <>? and name=? ", id, name).Count(&count)
	}
	if count > 0 {
		result = true
	} else {
		result = false
	}
	return
}

func (t TeacherEntity) DelTeacher(id string) (err error) {
	var teacher Teachers
	teacher.Id = id
	err = commons.DbClient.Delete(&teacher).Error
	return
}
