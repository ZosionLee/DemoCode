const path = require('path')
const fs = require('fs')
const { createLogger, format, transports, addColors } = require('winston')
const logconfig = require('./baseconfig').log;
fs.existsSync(logconfig.dir) || fs.mkdirSync(logconfig.dir)

const options = {
    allLog: {
        level: 'http',
        filename: path.resolve(logconfig.dir, 'all.log')
    },
    errorLog: {
        level: 'error',
        filename: path.resolve(logconfig.dir, 'error.log')
    }
}

const logger = createLogger({
    level: 'http',
    // levels: config.levels,
    handleExceptions: true,
    json: true,
    maxsize: 5242880, // 5MB
    maxFiles: 5,
    format: format.combine(
        format.colorize(),
        format.timestamp({ format: 'YYYY-MM-DD HH:mm:ss' }),
        format.splat(),
        format.simple(),
        format.printf(
            info =>`[${info.timestamp}] [${info.level}]: ${info.message}`
        )
    ),
    transports: [new transports.File(options.allLog), new transports.File(options.errorLog), new transports.Console()],
    exitOnError: false
})

// morgan stream
logger.stream = {
    write: function(message, encoding) {
        logger.http(message)
    }
}

module.exports = logger
