
var express = require('express');
var router = express.Router();
var {uuidTool,wrap} = require('../common/utils')
const validate = require('express-jsonschema').validate;
const sanitySchema = require('../common/schema');
const { AuthorEntity} = require('../common/entity')
const {schemaErrorHandle,authHandle} = require('../common/middleware')

router.use(wrap(authHandle))

router.post(
    '/',
    validate({body:sanitySchema.author}),
    wrap(async (req,res,next)=>{
        const obj = req.body
        obj.id=uuidTool.genUuid()
        const author = new AuthorEntity();
        const value = await author.addOne(obj)
        res.status(200).json(value)
    })
)


router.get(
    '/:authorId',
    wrap(async (req,res,next)=>{
        const author = new AuthorEntity();
        const value = await author.getOne(req.params.authorId)
        res.status(200).json(value)
    })
)

router.put(
    '/:authorId',
    validate({body:sanitySchema.author}),
    wrap(async (req,res,next)=>{
        const author = new AuthorEntity();
        const value = await author.putOne(req.params.authorId,req.body)
        res.status(200).json(value)
    })
)

router.delete(
    '/:authorId',
    wrap(async (req,res,next)=>{
        const author = new AuthorEntity();
        await author.delOne(req.params.authorId)
        res.status(200).json({status:true})
    })
)

router.use(schemaErrorHandle);

module.exports = router