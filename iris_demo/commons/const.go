/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 19:11:20
 */
package commons

const TokenPrefix string = "ABCD"
const TokenDelimiter string = "&&"

type schemaPath struct {
	TeacherSchemaPath string
}

var SchemaPath = &schemaPath{}

func init() {
	SchemaPath.TeacherSchemaPath = "file:///iris_demo/schema/teacher.json"
}
