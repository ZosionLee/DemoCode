const express= require('express');
const app=express();
const compression = require('compression');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const logHandle = require('./common/morgan-patch');
var users = require('./routes/users');
var authors = require('./routes/authors');
const {errorHandle} = require('./common/middleware')



// third components register
app.use(compression())
app.use(cookieParser())
app.use(bodyParser.json())
app.use(logHandle)


// router register
app.use('/users',users)
app.use('/authors',authors)

// exeception middleware
app.use(errorHandle);


app.get('/',(req, res) =>{
	res.send("API server is running");
});


app.listen(9000,()=>{
	console.log('Listening on port 9000')
});