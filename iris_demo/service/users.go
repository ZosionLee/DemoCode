/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 21:05:12
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package service

import (
	"irisdemo/commons"
	"irisdemo/models"
)

type UserService interface {
	Login(name string, password string) (result models.ResBody)
	// Logout(id string) (err error)
}

type userService struct{}

func NewUserService() *userService {
	return &userService{}
}

var userEntity = models.NewUserEntity()

func (n *userService) Login(name string, password string) (result models.ResBody) {
	user, err := userEntity.Login(name, password)
	if err != nil {
		result.Flag = false
		result.Data = commons.ErrorsMap["RetrieveError"]
	} else {
		result.Flag = true
		result.Data = user
	}
	return
}
