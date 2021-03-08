/*
 * @Descripttion: Do not edit
 * @version: v0.1.0
 * @Author: ZosionLee
 * @Date: 2021-02-27 20:17:19
 * @LastEditors: ZosionLee
 * @LastEditTime: 2021-03-07 21:39:56
 * @Copyright: Copyright © 2021, ZosionLee. All Rights Reserved.
 */

package main

import (
	stdContext "context"
	"irisdemo/control"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/iris-contrib/middleware/cors"
	"github.com/kataras/iris/v12"
	"github.com/kataras/iris/v12/middleware/rate"
	"github.com/kataras/iris/v12/middleware/recover"
	"github.com/kataras/iris/v12/mvc"
)

func newLogFile(name string) *os.File {
	today := time.Now().Format("Jan 02 2006")
	filename := name + "-" + today + ".txt"

	f, err := os.OpenFile(filename, os.O_CREATE|os.O_WRONLY|os.O_APPEND, 0666)
	if err != nil {
		panic(err)
	}

	return f
}

// func allowFunc(ctx iris.Context) {
// 	if auth, _ := sessions.Get(ctx).GetBoolean("authenticated"); !auth {
// 		ctx.StatusCode(iris.StatusForbidden)
// 		return
// 	}
// }

func newApp() *iris.Application {
	app := iris.New()

	// config app
	app.Configure(iris.WithConfiguration(
		iris.Configuration{
			LogLevel:            "debug",
			EnableOptimizations: true,
			TimeFormat:          "Mon, 02 Jan 2006 15:04:05 GMT",
			Charset:             "utf-8",
		},
	))

	// use compression
	app.Use(iris.Compression)

	// use recover
	app.Use(recover.New())

	// use cors
	crs := cors.New(cors.Options{
		AllowedOrigins:   []string{"*"},
		AllowCredentials: true,
		AllowedMethods:   []string{"GET", "POST", "DELETE", "PUT"},
		MaxAge:           10,
		Debug:            true,
	})
	app.Use(crs)

	// user auto set-cookies
	// sess := sessions.New(
	// 	sessions.Config{
	// 		Cookie:                      "session_id",
	// 		AllowReclaim:                true,
	// 		Expires:                     -1,
	// 		DisableSubdomainPersistence: false,
	// 		SessionIDGenerator:          sessionId,
	// 	},
	// )
	// app.Use(sess.Handler())

	// use auth
	// opts := basicauth.Options{
	// 	Realm:        basicauth.DefaultRealm,
	// 	ErrorHandler: basicauth.DefaultErrorHandler,
	// 	Allow:        allowFunc(iris.Context),
	// }
	// auth := basicauth.New(opts)
	// app.Use(auth)

	// user rate
	api := app.Party("/api")
	{
		apiLimit := rate.Limit(1, 5, rate.PurgeEvery(time.Minute, 5*time.Minute))
		api.Use(apiLimit)
	}

	// use mvc
	mvc.New(api.Party("/teachers")).Handle(control.NewTeacherController())
	mvc.New(api.Party("/users")).Handle(control.NewUserController())
	mvc.New(api.Party("/classes")).Handle(control.NewClassController())
	mvc.New(api.Party("/students")).Handle(control.NewStudentController())
	return app

}

func main() {

	app := newApp()
	f1 := newLogFile("debug")
	f2 := newLogFile("error")
	app.Logger().SetLevelOutput("debug", f1).SetLevelOutput("error", f2)
	defer f1.Close()
	defer f2.Close()

	go func() {
		ch := make(chan os.Signal, 1)
		signal.Notify(ch,
			os.Interrupt,
			syscall.SIGINT,
			os.Kill,
			syscall.SIGKILL,
			syscall.SIGTERM,
		)
		select {
		case <-ch:
			println("shutdown...")

			timeout := 5 * time.Second
			ctx, cancel := stdContext.WithTimeout(stdContext.Background(), timeout)
			defer cancel()
			app.Shutdown(ctx)
		}
	}()

	if err := app.Run(iris.Addr(":8080"), iris.WithoutInterruptHandler); err != nil {
		app.Logger().Errorf("Shutdonw with error:%v\n", err)
	} else {
		app.Logger().Info("Server is running")
	}
}
