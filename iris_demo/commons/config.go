/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-02-27 21:03:20
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */

package commons

import (
	"fmt"
	"io/ioutil"
	"log"

	jsoniter "github.com/json-iterator/go"
	"gopkg.in/yaml.v3"
)

type conRedis struct {
	Host     string `yaml:"redis/host"`
	Port     string `yaml:"redis/port"`
	Db       int    `yaml:"redis/database"`
	Password string `yaml:"redis/password"`
}

type conMysql struct {
	Host     string `yaml:"mysql/host"`
	Port     string `yaml:"mysql/port"`
	Db       string `yaml:"mysql/database"`
	Username string `yaml:"mysql/username"`
	Password string `yaml:"mysql/password"`
}

type conConfig struct {
	Redis conRedis
	Mysql conMysql
}

var ConConfig = &conConfig{}

func InitConnectionConfig() {
	b, err := ioutil.ReadFile("./conf/config.yaml")
	if err != nil {
		log.Fatalln("Con config read error")
		panic(err)
	}
	err = yaml.Unmarshal(b, ConConfig)
	if err != nil {
		log.Fatalln("Con unmarshal error")
		panic(err)
	}
	log.Printf("Connection config is %+v\n", ConConfig)
}

// config file also can be json
func DummyInitConfig() {

	config := conConfig{
		conRedis{
			"connect-redis.com",
			"6379",
			1,
			"",
		},
		conMysql{
			"connect-mysql.com",
			"3306",
			"dummy-database",
			"root",
			"123456",
		},
	}

	b, err := jsoniter.Marshal(config)
	if err != nil {
		panic("Dummy loading error")
	}

	DummyConfig := &conConfig{}
	err = jsoniter.Unmarshal(b, DummyConfig)
	if err != nil {
		panic(err)
	}
	fmt.Printf("Dummy config is %+v\n", DummyConfig)

}

func init() {
	InitConnectionConfig()
}
