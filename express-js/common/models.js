const {sequelize} = require('./connections')
const {Model,DataTypes} = require('sequelize')


class Users extends Model {}
Users.init(
    {
        id: { type: DataTypes.STRING, primaryKey: true },
        name: { type: DataTypes.STRING, allowNull: false},
        password: { type: DataTypes.STRING, allowNull: false},
        createdTime: {type:DataTypes.DATE,field:'created_time',defaultValue:DataTypes.Now},
        updatedTime: {type:DataTypes.DATE,field:'updated_time',defaultValue:DataTypes.Now}
    },
    {
        sequelize,
        modelName:'Users',
        timestamps:false,
        freezeTableName:false,
        tableName:'users'
    }
)

class Authors extends Model {

    get authorInfo(){
        return JSON.stringify(
            {
                'name':this.name,
                'age': this.age,
                'coutry':this.country,
                'description': this.description
            }
        )
    }

}
Authors.init(
    {
        id: { type: DataTypes.STRING, primaryKey: true },
        name: { type: DataTypes.STRING, unique: false,allowNull: false},
        age: { type: DataTypes.INTEGER, allowNull: false},
        qualification: { type: DataTypes.JSON, allowNull: false,unique:true},
        country: { type: DataTypes.STRING },
        description:  { type: DataTypes.STRING },
        createdTime: {type:DataTypes.DATE,field:'created_time',defaultValue:DataTypes.Now},
        updatedTime: {type:DataTypes.DATE,field:'updated_time',defaultValue:DataTypes.Now}
    },
    {
        sequelize,
        modelName:'Authors',
        timestamps:false,
        freezeTableName:false,
        tableName:'authors'
    }
)



class Categories extends Model {}
Categories.init(
    {
        id: { type: DataTypes.STRING, primaryKey: true },
        name: { type: DataTypes.STRING, unique: true,allowNull: false},
        createdTime: {type:DataTypes.DATE,field:'created_time',defaultValue:DataTypes.Now},
        updatedTime: {type:DataTypes.DATE,field:'updated_time',defaultValue:DataTypes.Now}
    },
    {
        sequelize,
        modelName:'Categories',
        timestamps:false,
        freezeTableName:false,
        tableName:'categories'
    }
)

class Publishers extends Model {}
Publishers.init(
    {
        id: { type: DataTypes.STRING, primaryKey: true },
        name: { type: DataTypes.STRING, unique: true,allowNull: false},
        address: { type: DataTypes.STRING, unique: true,allowNull: false},
        createdTime: {type:DataTypes.DATE,field:'created_time',defaultValue:DataTypes.Now},
        updatedTime: {type:DataTypes.DATE,field:'updated_time',defaultValue:DataTypes.Now}
    },
    {
        sequelize,
        modelName:'Publishers',
        timestamps:false,
        freezeTableName:false,
        tableName:'publishers'
    }
)

class Books extends Model {}
Books.init(
    {
        id: { type: DataTypes.STRING, primaryKey: true },
        title: { type: DataTypes.STRING, unique: true,allowNull: false},
        price: { type: DataTypes.FLOAT, allowNull: false,validate:{min:0,max:1000}},
        rank: { type: DataTypes.INTEGER,validate:{min:0}},
        description:  { type: DataTypes.STRING },
        category:{
            type: DataTypes.STRING,
            references:{
                model: Categories,
                key: 'id',
            }
        },
        author:{
            type: DataTypes.STRING,
            references:{
                model:Authors,
                key: 'id',
            }
        },
        publisher:{
            type: DataTypes.STRING,
            references:{
                model:Publishers,
                key: 'id',
            }
        },
        createdTime: {type:DataTypes.DATE,field:'created_time',defaultValue:DataTypes.Now},
        updatedTime: {type:DataTypes.DATE,field:'updated_time',defaultValue:DataTypes.Now}
    },
    {
        sequelize,
        modelName:'Books',
        timestamps:false,
        freezeTableName:false,
        tableName:'books'
    }
)

class Stories extends Model {}
Stories.init(
    {
        id: { type: DataTypes.STRING, primaryKey: true },
        name: { type: DataTypes.STRING, unique: false,allowNull: false},
        address: { type: DataTypes.STRING, unique: true,allowNull: false},
        createdTime: {type:DataTypes.DATE,field:'created_time',defaultValue:DataTypes.Now},
        updatedTime: {type:DataTypes.DATE,field:'updated_time',defaultValue:DataTypes.Now}
    },
    {
        sequelize,
        modelName:'Stories',
        timestamps:false,
        freezeTableName:false,
        tableName:'stories'
    }
)

class StoreBookRelations extends Model {}
StoreBookRelations.init(
    {
        id: { type: DataTypes.STRING, primaryKey: true,autoIncrement:true },
        bookId: {
            type: DataTypes.STRING,
            references:{
                model:Books,
                key: 'id',
            }
        },
        storeId:{
            type: DataTypes.STRING,
            references:{
                model:Stories,
                key: 'id',
            }
        },
        createdTime: {type:DataTypes.DATE,field:'created_time',defaultValue:DataTypes.Now},
        updatedTime: {type:DataTypes.DATE,field:'updated_time',defaultValue:DataTypes.Now}
    },
    {
        sequelize,
        modelName:'StoreBookRelations',
        timestamps:false,
        freezeTableName:false,
        tableName:'book_store_relation'
    }
)

module.exports = {
    Users,
    Authors,
    Books,
    Categories,
    Publishers,
    Stories,
    StoreBookRelations
}

