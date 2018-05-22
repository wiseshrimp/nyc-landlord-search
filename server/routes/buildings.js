const express = require('express')
const router = express.Router()
const db = require('../../db')
const Building = db.sequelize.models.buildings

const success = { response: 'success' }

router
  .get('/', function (req, res, next) {
    Building.findAll()
      .then(function (buildings) {
        res.status(200)
        res.send({
          data: buildings
        })
        next()
      })
      .catch(err => {
        console.error(err)
      })
  })
  .post('/', (req, res, next) => {
    // TO DO: Change db fields
    print(req)
    next()
    // let {
    //   building_id,
    //   building_number,
    //   street_name,
    //   zip_code,
    //   neighborhood,
    //   borough,
    //   block_number,
    //   year_built,
    //   sale_price,
    //   sale_date,
    //   num_of_complaints,
    //   num_of_dob_violations,
    //   num_of_ecb_violations,
    //   complaints_link,
    //   dob_violations_link,
    //   ecb_violations_link
    // } = req.body

    // Building.build({
    //   building_id,
    //   building_number,
    //   street_name,
    //   zip_code,
    //   neighborhood,
    //   borough,
    //   block_number,
    //   year_built,
    //   sale_price,
    //   sale_date,
    //   num_of_complaints,
    //   num_of_dob_violations,
    //   num_of_ecb_violations,
    //   complaints_link,
    //   dob_violations_link,
    //   ecb_violations_link
    // })
  })

module.exports = router
