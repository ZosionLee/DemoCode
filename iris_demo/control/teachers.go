/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 19:22:10
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
	"github.com/lithammer/shortuuid/v3"
	"github.com/spf13/cast"
)

type TeacherController struct {
	Ctx     iris.Context
	Service service.TeacherService
}

func NewTeacherController() *TeacherController {
	return &TeacherController{Service: service.NewTeacherService()}
}

func (t TeacherController) Get() (result mvc.Result) {
	if auth := commons.Auth(t.Ctx); !auth {
		t.Ctx.StatusCode(iris.StatusUnauthorized)
		return
	}

	if !t.Ctx.URLParamExists("limit") || !t.Ctx.URLParamExists("offset") {
		result = mvc.Response{Code: 400, Object: commons.ErrorsMap["NeedParams"]}
		return
	}

	limit := t.Ctx.URLParamEscape("limit")
	offset := t.Ctx.URLParamEscape("offset")
	res := t.Service.List(cast.ToUint(limit), cast.ToUint(offset))
	result = mvc.Response{Code: 200, Object: res.Data}
	return
}

func (t TeacherController) Post() (result mvc.Result) {
	if auth := commons.Auth(t.Ctx); !auth {
		t.Ctx.StatusCode(iris.StatusUnauthorized)
		return
	}

	var teacher models.Teachers
	if err := t.Ctx.ReadJSON(&teacher); err != nil {
		log.Printf("Json Parse Error:%v", err)
		result = mvc.Response{Code: 400, Object: commons.ErrorsMap["JsonParseError"]}
		return
	}
	teacher.Id = shortuuid.New()
	res := t.Service.Create(teacher)
	if res.Flag {
		result = mvc.Response{Code: 200, Object: res.Data}
	} else {
		result = mvc.Response{Code: 400, Object: res.Data}
	}
	return
}

func (t TeacherController) GetBy(id string) (result mvc.Result) {
	if auth := commons.Auth(t.Ctx); !auth {
		t.Ctx.StatusCode(iris.StatusUnauthorized)
		return
	}
	res := t.Service.Retrieve(id)
	if res.Flag {
		result = mvc.Response{Code: 200, Object: res.Data}
	} else {
		result = mvc.Response{Code: 400, Object: res.Data}
	}
	return
}

func (t TeacherController) PutBy(id string) (result mvc.Result) {
	if auth := commons.Auth(t.Ctx); !auth {
		t.Ctx.StatusCode(iris.StatusUnauthorized)
		return
	}
	var teacher models.Teachers
	if err := t.Ctx.ReadJSON(&teacher); err != nil {
		log.Printf("Json Parse Error:%v", err)
		result = mvc.Response{Code: 400, Object: commons.ErrorsMap["JsonParseError"]}
		return
	}
	res := t.Service.Update(id, teacher)
	if res.Flag {
		result = mvc.Response{Code: 200, Object: res.Data}
	} else {
		result = mvc.Response{Code: 400, Object: res.Data}
	}
	return
}

func (t TeacherController) DeleteBy(id string) (result mvc.Result) {
	if auth := commons.Auth(t.Ctx); !auth {
		t.Ctx.StatusCode(iris.StatusUnauthorized)
		return
	}
	res := t.Service.Destory(id)
	if res.Flag {
		result = mvc.Response{Code: 200, Object: res.Data}
	} else {
		result = mvc.Response{Code: 400, Object: res.Data}
	}
	return
}
