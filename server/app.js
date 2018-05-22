const bodyParser = require('body-parser')
const express = require('express')
const fs = require('fs')
const spawn = require('child_process').spawn

const app = express()
const router = express.Router()
const port = process.env.PORT || 3000

app.use(express.static(`scripts`))
app.use(express.static('views'))
app.use(express.static(`public`))
app.use(bodyParser.urlencoded({ extended: true }))
app.use(bodyParser.json())
app.engine('html', require('ejs').renderFile)
app.set('view engine', 'html')

router.get('/', function (req, res, next) {
  res.render('index.html')
})

app.use('/api', require('./api'))

app.use('/', router)

app.listen(port, function () {
  console.log(`Listening on port: ${port}`)
})
