/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 19:56:20
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package models

import "irisdemo/commons"

type Users struct {
	Id       string `gorm:"primaryKey"`
	Name     string
	Password string
}

type UserEntity struct{}

func NewUserEntity() *UserEntity {
	return &UserEntity{}
}

type IUserEntity interface {
	Login(name string, password string) (user Users, err error)
	// Logout(id string) (err error)
}

func (t *UserEntity) Login(name string, password string) (user Users, err error) {
	err = commons.DbClient.Find(&user, "name = ? and password = ?", name, password).Error
	return
}
