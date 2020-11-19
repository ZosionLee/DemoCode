const {uuidTool} = require('./utils')
const {redis} = require('./connections')


class Session{
    constructor(userId=null,token=null) {
        if(!userId && !token){
            throw Error('user id and token must has one')
        }
        this.userId=userId
        this.token= token
    }

    getSession(){
        if(this.token){
            return this.token
        }
        this.token = uuidTool.genUuid()+'@@'+this.userId
        let key = `cookies:${this.userId}`
        redis.set(key,this.token,'EX',60*60*24)
        return this.token
    }

    async getUserId(){
        if(this.userId){
            return this.userId
        }
        let userId = this.token.split('@@')[1]
        let value = await redis.get(`cookies:${userId}`)
        if (value === this.token){
            this.userId=userId
            redis.expireat(
                `cookies:${userId}`, parseInt((+new Date)/1000) + 60*60*24
            );
        }
        return this.userId
    }

    clear(){
        if(typeof this.userId  === 'string'){
            redis.del(`cookies:${this.userId}`)
        }
    }
}

module.exports = Session