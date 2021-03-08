/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-02-27 21:22:20
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package commons

import (
	"log"
	"strings"
	"time"

	_ "github.com/go-sql-driver/mysql"
	"github.com/jinzhu/gorm"
	"gopkg.in/redis.v4"
)

var DbClient *gorm.DB
var CacheClient *redis.Client

func initMysql() {
	path := strings.Join([]string{
		ConConfig.Mysql.Username,
		":",
		ConConfig.Mysql.Password,
		"@(",
		ConConfig.Mysql.Host,
		":",
		ConConfig.Mysql.Port,
		")/",
		ConConfig.Mysql.Db,
		"?charset=utf8mb4&parseTime=true",
	}, "")

	var err error
	DbClient, err = gorm.Open("mysql", path)
	if err != nil {
		log.Fatalf("Connect to mysql error: %v", err)
		panic(err)
	} else {
		log.Println("Connect to mysql ok")
	}
	DbClient.SingularTable(false)
	DbClient.DB().SetConnMaxLifetime(1 * time.Second)
	DbClient.DB().SetMaxIdleConns(20)
	DbClient.DB().SetMaxOpenConns(2000)
	DbClient.LogMode(true)
}

func initRedis() {
	CacheClient = redis.NewClient(
		&redis.Options{
			Addr:     ConConfig.Redis.Host + ":" + ConConfig.Redis.Port,
			Password: ConConfig.Redis.Password,
			DB:       ConConfig.Redis.Db,
			PoolSize: 10,
		})
	pong, err := CacheClient.Ping().Result()
	if err != nil {
		log.Fatalf("Connect to redis error %v", err)
		panic(err)
	} else {
		log.Printf("Redis connection OK : %v", pong)
	}
}

func init() {
	initMysql()
	initRedis()
}
