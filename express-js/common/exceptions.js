

class InternalError extends Error {
    constructor (code,message) {
        super(message)

        this.name = this.constructor.name
        this.code = code
        this.message = message

    }

    info(){
        return {
            code: this.code,
            message: this.message
        }
    }

}


class BadRequestError extends  Error {
    constructor (code,message) {
        super(message)

        this.name = this.constructor.name
        this.code = code
        this.message = message

        Error.captureStackTrace(this, this.constructor); // prevent showing up in the stack trace
    }

    info(){
        return {
            code: this.code,
            message: this.message
        }
    }

}

module.exports = {
    InternalError,
    BadRequestError
}