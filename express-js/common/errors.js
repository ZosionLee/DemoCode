
module.exports = {
    schemaError:{
        code:'0001',
        msg:'Data schema validation error'
    },
    RedisError:{
        code:'0002',
        msg:'Operating redis error'
    },
    DataBaseError:{
        code:'0003',
        msg:'Operating redis error'
    },


    AuthorDuplicatedError:{
        code:'1001',
        msg:'Author duplicated, please check your params'
    },
    AuthorIdInvalid:{
        code:'1002',
        msg:'Author id invalid, please check your params'
    },
    AuthorAgeInvalid:{
        code:'1003',
        msg:'Author age invalid, please check your params'
    },

    UserDuplicated:{
        code:'2001',
        msg:'User name duplicated, please check your params'
    },
    UserLogin:{
        code:'2002',
        msg:'User name or password error, please check your params'
    }
}
