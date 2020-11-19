const config= require('config-lite')(__dirname);

module.exports = {
	application: {
		name: config['application/name'],
		port: config['application/port']
	},
	redis:{
		db:config['cache/redis/database'],
		host: config['cache/redis/host'],
		port: config['cache/redis/port'],
		password: config['cache/redis/password'],
		user: config['cache/redis/user'],
		ttl: config['ttl/cache/session']
	},
	mysql:{
		name: config['db/mysql/database'],
		host: config['db/mysql/host'],
		port: config['db/mysql/port'],
		password: config['db/mysql/password'],
		user: config['db/mysql/user'],
		debug: config['db/debug']
	},
	log:{
		dir: config['log/dir'],
		level: config['log/level']
	}
}