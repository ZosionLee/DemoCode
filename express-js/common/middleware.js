const logger =require('./logger');
const errors = require('./errors')
const Session = require('./session')
const {InternalError} = require("./exceptions");

function errorHandle(err,req,res,next){
    if(err.name === 'InternalError'){
        logger.error(err.info())
        res.status(500).json(err.info())
    } else if (err.name === 'BadRequestError') {
        logger.error(err.info())
        res.status(400).json(err.info())
    } else {
        logger.error(err.message)
        res.status(500).json({'status':false})
    }
}

function schemaErrorHandle(err, req, res, next){
    if (err.name === 'JsonSchemaValidation'){
        next(
            new InternalError(
                errors.schemaError.code,
                {
                    jsonSchemaValidation: true,
                    validations: err.validations
                }
            )
        )
    } else {
        next(err)
    }
}


async function authHandle(req, res, next) {
    let msg = {
        code: 401,
        message:'UnAuthenticated'
    }
    if (req.cookies._cookie){
        let session = new Session(null,req.cookies._cookie)
        let userId = await session.getUserId()
        if (!userId){
            res.status(401).json(msg)
        } else {
            next()
        }
    } else {
        res.status(401).json(msg)
    }
}

module.exports = {
    errorHandle,
    authHandle,
    schemaErrorHandle
}