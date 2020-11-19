const Sequelize = require('sequelize');
const Redis = require('ioredis');
const connConfig = require('./baseconfig');
const logger = require('./logger');

const sequelize = new Sequelize(
    connConfig.mysql.name,
    connConfig.mysql.user,
    connConfig.mysql.password,
    {
        dialect: 'mysql',
        host: connConfig.mysql.host,
        port: connConfig.mysql.port,
        define: {
            underscored: false,
            freezeTableName: false,
            charset: 'utf8mb4',
            dialectOptions: {
                collate: 'utf8mb4_bin'
            },
            timestamps: true
        },
        pool: {
            max: 5,
            idle: 30000,
            acquire: 60000,
        },
    }
);
sequelize.authenticate().then(
    () => {
        logger.info('Mysql Connection has been established successfully.');
    }
).catch(
    err => {
        logger.error('Unable to connect to the mysql:', err);
    }
);


const redis = new Redis(
    connConfig.redis.port,
    connConfig.redis.host,
    {
        password:connConfig.redis.password,
        db:connConfig.redis.db,
        connectTimeout:10000
    }
)

module.exports = {
    sequelize,
    redis
}