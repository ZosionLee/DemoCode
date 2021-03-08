/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 19:5:20
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package control

import (
	"irisdemo/commons"
	"irisdemo/models"
	"irisdemo/service"
	"log"

	"github.com/kataras/iris/v12"
	"github.com/kataras/iris/v12/mvc"
)

type UserController struct {
	Ctx     iris.Context
	Service service.UserService
}

func NewUserController() *UserController {
	return &UserController{Service: service.NewUserService()}
}

func (t UserController) PostLogin() (result mvc.Result) {
	var user models.Users
	if err := t.Ctx.ReadJSON(&user); err != nil {
		log.Printf("Json Parse Error:%v", err)
		result = mvc.Response{Code: 400, Object: commons.ErrorsMap["JsonParseError"]}
		return
	}
	res := t.Service.Login(user.Name, user.Password)
	if res.Flag {
		sessionEntity := commons.NewSessionEntity()
		if user, ok := res.Data.(models.Users); ok {
			session := commons.Sessions{User_id: user.Id, Token: ""}
			token := sessionEntity.GetToken(session)
			t.Ctx.SetCookieKV("_token", token)
		}
		result = mvc.Response{Code: 200, Object: res.Data}
	} else {
		result = mvc.Response{Code: 401}
	}
	return
}

func (t UserController) PostLogout() (result mvc.Result) {
	token := t.Ctx.GetCookie("_token")
	result = mvc.Response{Code: 200}
	if token == "" {
		return
	} else {
		sessionEntity := commons.NewSessionEntity()
		session := commons.Sessions{User_id: "", Token: token}
		sessionEntity.ClearToken(session)
		t.Ctx.RemoveCookie("_token")
	}
	return
}
