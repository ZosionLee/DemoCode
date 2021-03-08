/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-1 20:01:16
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */
package commons

import (
	"log"
	"time"

	"github.com/kataras/iris/v12"
)

type Sessions struct {
	User_id string
	Token   string
}

type ISessions interface {
	GetUserId(session Sessions) (user_id string)
	GetToken(session Sessions) (token string)
	ClearToken(session Sessions)
}

type sessionEntity struct{}

func NewSessionEntity() *sessionEntity {
	return &sessionEntity{}
}

func (s *sessionEntity) GetUserId(session Sessions) (user_id string) {
	if session.User_id != "" {
		user_id = session.User_id
		return
	} else {
		start := len(TokenPrefix + TokenDelimiter)
		user_id = session.Token[start:]
		value, err := CacheClient.Get("token:" + user_id).Result()
		if err != nil {
			log.Fatalf("[Session] Get token error:%v", err)
			panic(err)
		}
		if session.Token == value {
			if err = CacheClient.Expire("token:"+user_id, 24*time.Hour).Err(); err != nil {
				log.Fatalf("[Session] Set token TTL error:%v", err)
				panic(err)
			}
			return
		} else {
			user_id = ""
			return
		}
	}
}

func (s *sessionEntity) GetToken(session Sessions) (token string) {
	if session.Token != "" {
		token = session.Token
		return
	} else {
		token = TokenPrefix + TokenDelimiter + session.User_id
		if err := CacheClient.Set(
			"token:"+session.User_id,
			token,
			24*time.Hour,
		).Err(); err != nil {
			log.Fatalf("[Session] Store token error:%v", err)
			panic(err)
		}
		return
	}
}

func (s *sessionEntity) ClearToken(session Sessions) {
	user_id := s.GetUserId(session)
	if user_id != "" {
		if err := CacheClient.Del("token:" + string(user_id)).Err(); err != nil {
			log.Fatalf("[Session] Del token error:%v", err)
			panic(err)
		}
	}
}

func Auth(ctx iris.Context) bool {
	token := ctx.GetCookie("_token")
	if token == "" {
		return false
	} else {
		sessionEntity := NewSessionEntity()
		session := Sessions{User_id: "", Token: token}
		user_id := sessionEntity.GetUserId(session)
		if user_id == "" {
			return false
		} else {
			return true
		}
	}
}
