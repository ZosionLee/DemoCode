var express = require('express');
var router = express.Router();
var {uuidTool,wrap} = require('../common/utils')
const validate = require('express-jsonschema').validate;
const sanitySchema = require('../common/schema');
const {UserEntity} = require('../common/entity')
const {schemaErrorHandle,authHandle} = require('../common/middleware')
const Session= require('../common/session')


router.post(
    '/',
    validate({body:sanitySchema.user}),
    wrap(async (req,res,next)=>{
        let obj = req.body
        obj.id = uuidTool.genUuid()
        let user = new UserEntity();
        let value = await user.addOne(obj)
        res.status(200).json(value)
    })
)

router.post(
    '/login',
    validate({body:sanitySchema.login}),
    wrap(async (req,res,next)=>{
        let user = new UserEntity()
        let userId = await user.login(req.body)
        let session = new Session(userId)
        res.cookie('_cookie', session.getSession());
        res.status(200).json({status:true})
    })
)

router.post(
    '/logout',
    wrap(authHandle),
    wrap(async (req,res,next)=>{
            let userId=req.cookies._cookie.split('@@')[1]
            let session = new Session(userId)
            session.clear()
            res.status(200).json({status:true})
    })
)


module.exports = router;