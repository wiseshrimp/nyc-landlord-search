const express = require('express')
const router = express.Router()
const db = require('../../db')
const Landlord = db.sequelize.models.landlords
const success = { response: 'success' }

router
  .get('/', (req, res, next) => {
    Landlord.findAll()
    .then(landlords => {
      res.status(200)
      res.send({
        data: landlords
      })
      next()
    })
    .catch(err => {
      console.error(err)
    })
  })

module.exports = router
