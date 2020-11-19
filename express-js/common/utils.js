const uuid = require('uuid');
const uuidToHex = require('uuid-to-hex');

class UuidTool {
    constructor() {
        this.regex = '^[a-f0-9]{32}$'
    }

    genUuid(){
        return uuidToHex(uuid.v4())
    }

    checkUuid(id){
        return new RegExp(this.regex).test(id)
    }

}

const uuidTool = new UuidTool()

let wrap = fn => (...args) => fn(...args).catch(args[2])

module.exports = {
    uuidTool,
    wrap
}