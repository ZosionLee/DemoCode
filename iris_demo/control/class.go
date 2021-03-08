/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 17:17:20
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

type ClassController struct {
	Ctx     iris.Context
	Service service.ClassService
}

func NewClassController() *ClassController {
	return &ClassController{Service: service.NewClassService()}
}

func (t ClassController) Get() (result mvc.Result) {
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

func (t ClassController) Post() (result mvc.Result) {
	if auth := commons.Auth(t.Ctx); !auth {
		t.Ctx.StatusCode(iris.StatusUnauthorized)
		return
	}

	var Class models.Classes
	if err := t.Ctx.ReadJSON(&Class); err != nil {
		log.Printf("Json Parse Error:%v", err)
		result = mvc.Response{Code: 400, Object: commons.ErrorsMap["JsonParseError"]}
		return
	}
	Class.Id = shortuuid.New()
	res := t.Service.Create(Class)
	if res.Flag {
		result = mvc.Response{Code: 200, Object: res.Data}
	} else {
		result = mvc.Response{Code: 400, Object: res.Data}
	}
	return
}

func (t ClassController) GetBy(id string) (result mvc.Result) {
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

func (t ClassController) PutBy(id string) (result mvc.Result) {
	if auth := commons.Auth(t.Ctx); !auth {
		t.Ctx.StatusCode(iris.StatusUnauthorized)
		return
	}
	var Class models.Classes
	if err := t.Ctx.ReadJSON(&Class); err != nil {
		log.Printf("Json Parse Error:%v", err)
		result = mvc.Response{Code: 400, Object: commons.ErrorsMap["JsonParseError"]}
		return
	}
	res := t.Service.Update(id, Class)
	if res.Flag {
		result = mvc.Response{Code: 200, Object: res.Data}
	} else {
		result = mvc.Response{Code: 400, Object: res.Data}
	}
	return
}

func (t ClassController) DeleteBy(id string) (result mvc.Result) {
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
