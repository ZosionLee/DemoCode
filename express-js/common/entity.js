const util = require('util')
const bcrypt = require('bcrypt');
const saltRounds = 12;
const logger = require('./logger')
const {Transaction} = require('sequelize');
const {InternalError,BadRequestError} = require('./exceptions')
const errors = require('./errors')
const {Users,Authors, Books, Categories, Publishers, Stories, StoreBookRelations} = require('./models')
const {redis,sequelize} = require('./connections')
const {uuidTool} = require('./utils')


class AuthorValidator{

    async qualificationCheck(value){
        try{
            value = await Authors.findAll({where:{qualification:value}})
        }catch (err) {
            throw new BadRequestError(
                errors.DataBaseError.code,
                errors.DataBaseError.msg
            )
        }
        if (value.length){
            throw new BadRequestError(
                errors.AuthorDuplicatedError.code,
                errors.AuthorDuplicatedError.msg
            )
        }
    }

    ageCheck(value){
        if ( 0<value && value <150){
            return true
        } else {
            throw new BadRequestError(
                errors.AuthorAgeInvalid.code,
                errors.AuthorAgeInvalid.msg
            )
        }
    }

    uuidCheck(id){
        if (!uuidTool.checkUuid(id)){
            throw new BadRequestError(
                errors.AuthorIdInvalid.code,
                errors.AuthorIdInvalid.msg
            )
        }
    }

    async addAuthorCheck(qulia,age){
        await this.qualificationCheck(qulia)
        this.ageCheck(age)
    }

}


class AuthorEntity {
    constructor() {
        this.cacheKey= 'author:%s'
        this.model = Authors
        this.validator = new AuthorValidator()
        this.cacheTtl =10*60
    }

    async addOne(obj){
        // validate
        await this.validator.addAuthorCheck(obj.qualification,obj.age)
        // insert to database
        try{
            await this.model.create(obj)
        } catch (err) {
            logger.error(`Insert Author error reason:${err}`);
            throw new InternalError(
                errors.DataBaseError.code,
                errors.DataBaseError.msg
            )
        }
        // caching to redis
        try{
            await redis.set(util.format(this.cacheKey,obj.id),JSON.stringify(obj),'EX',this.cacheTtl)
        } catch (err) {
            logger.error(`Caching Author error reason:${err}`)
            throw new InternalError(
                errors.RedisError.code,
                errors.RedisError.msg
            )
        }

        return obj
    }

    async getOne(id){
        this.validator.uuidCheck(id) //validate
        let value = await redis.get(util.format(this.cacheKey,id)) // get from redis
        if (!value) {
            const obj = await Authors.findByPk(id)  // get from database and refresh redis
            if (obj) {
                redis.set(util.format(this.cacheKey, id), JSON.stringify(obj), 'EX', this.cacheTtl)
                return obj
            } else {
                return obj
            }
        } else {
            return JSON.parse(value)
        }
    }

    async putOne(id,obj){
        this.validator.uuidCheck(id) // validator
        await Authors.update(obj,{where:{id:id},lock:Transaction.LOCK.UPDATE})
        const instance = await Authors.findByPk(id)
        if (instance){
            redis.set(util.format(this.cacheKey, id), JSON.stringify(instance), 'EX', this.cacheTtl)
        }
        return instance
    }

    async delOne(id){
        this.validator.uuidCheck(id)
        await sequelize.transaction(async (t)=>{
            const instance = await Authors.findByPk(id)
            if (instance){
                await instance.destroy({transaction:t})
                redis.del(util.format(this.cacheKey, id))
            }
        })
    }
}

class UserValidator{
    async login(obj){
        let instance = await Users.findOne({where:{name:obj.name}})
        if (!instance){
            throw new BadRequestError(
                errors.UserLogin.code,
                errors.UserLogin.msg
            )
        }
        let value = await bcrypt.compare(obj.password,instance.password)
        if (!value){
            throw new BadRequestError(
                errors.UserLogin.code,
                errors.UserLogin.msg
            )
        }
        return instance.id
    }

    async addUserCheck(obj){
        let instance = await Users.findOne({where:{name:obj.name}})
        if (instance){
            throw new BadRequestError(
                errors.UserDuplicated.code,
                errors.UserDuplicated.msg
            )
        }
    }

}

class UserEntity{
    constructor() {
        this.validator = new UserValidator()
    }


    async login(obj){
        return await this.validator.login(obj)   // validate
    }

    async addOne(obj){
        await this.validator.addUserCheck(obj)   // validate
        try{
            obj.password = await bcrypt.hash(obj.password,saltRounds)
            await Users.create(obj)    // insert to database
        } catch (err) {
            logger.error(`Insert User error reason:${err}`);
            throw new InternalError(
                errors.DataBaseError.code,
                errors.DataBaseError.msg
            )
        }
        return obj
    }
}

module.exports = {
    UserEntity,
    AuthorEntity
}