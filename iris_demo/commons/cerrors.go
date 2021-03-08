/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-1 21:06:36
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package commons

type errorResponse struct {
	Code    int
	Message string
}

// func (e errorResponse) Error() string {
// 	return e.Message
// }

// func (e errorResponse) Dispatch(ctx iris.Context) {

// }

var ErrorsMap map[string]errorResponse

func InitError() {
	ErrorsMap = make(map[string]errorResponse)
	ErrorsMap["JsonParseError"] = errorResponse{Code: 1, Message: "Json Parse Error"}
	ErrorsMap["NameDuplicated"] = errorResponse{Code: 2, Message: "Name Duplicated"}
	ErrorsMap["NeedParams"] = errorResponse{Code: 3, Message: "Need Params"}
	ErrorsMap["MissEntity"] = errorResponse{Code: 3, Message: "Miss Entity"}

	ErrorsMap["InsertError"] = errorResponse{Code: 11, Message: "Insert entity Error"}
	ErrorsMap["RetrieveError"] = errorResponse{Code: 12, Message: "Retrieve entity Error"}
	ErrorsMap["UpdateError"] = errorResponse{Code: 13, Message: "Update entity Error"}
	ErrorsMap["DeleteError"] = errorResponse{Code: 14, Message: "Delete entity Error"}
}

func init() {
	InitError()
}
