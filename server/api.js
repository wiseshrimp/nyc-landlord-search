'use strict'

const api = require('express').Router();

api.use('/buildings', require('./routes/buildings'))
api.use('/landlords', require('./routes/landlords'))

// Send along any errors
api.use((err, req, res, next) => {
  res.status(err.status || 500).send(err.message || err)
})

// No routes matched? 404.
api.use((req, res) => res.status(404).end())

module.exports = api
