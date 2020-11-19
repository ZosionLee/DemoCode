var validate = require('express-jsonschema').validate;
const { internalError } = require('./exceptions');
const logger = require('./logger')

module.exports = function (schema,query=false,body=false) {
    try {
        if (query){
            validate({query:schema})
        }

    }
    catch(err){
        if (err.name === 'JsonSchemaValidation'){
            logger.error(err.message)
            throw internalError(
                100201,
                'json shema error'
            )
        } else {
            throw Error(err.message)
        }
    }
}