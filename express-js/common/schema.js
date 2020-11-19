
var sanitySchema={
    author:{
        type:'object',
        properties:{
            'name':{
                type:'string',
                required: true,
            },
            'age':{
                type: 'integer',
                required: true,
            },
            'description':{
                type: 'string',
            },
            'qualification':{
                type: 'object',
                required: true,
            },
            'country':{
                type: 'string',
            }
        }
    },
    login:{
        type:'object',
        properties: {
            name:{
                type:'string',
                required:true
            },
            password:{
                type:'string',
                required:true
            }
        }
    },
    user:{
        type:'object',
        properties: {
            name:{
                type:'string',
                required:true
            },
            password:{
                type:'string',
                required:true
            }
        }
    }
}

module.exports = sanitySchema