const debug = require('debug')('sql')
const chalk = require('chalk')
const Sequelize = require('sequelize')
const Promise = require('bluebird')
const { Client } = require('pg')
const dbName = 'landlord-dev'

let sequelize
const BOROUGHS = ['Brooklyn', 'Queens', 'Manhattan', 'Bronx', 'Staten Island']

if (process.env.HEROKU_POSTGRESQL_COBALT_URL) {
  sequelize = new Sequelize(process.env.HEROKU_POSTGRESQL_COBALT_URL, {
    dialect: 'postgres',
    protocol: 'postgres',
    logging: true
  })
} else {
  sequelize = new Sequelize(`postgres://localhost:5432/${dbName}`, {
    logging: debug,
    define: {
      underscored: true,
      freezeTableName: true,
      timestamps: true
    }
  })
}

const Landlord = sequelize.define('landlords', {
  first_name: {
    type: Sequelize.STRING,
    allowNull: false
  },
  second_name: {
    type: Sequelize.STRING,
    allowNull: false
  },
  phone_number: Sequelize.STRING,
  updated_at: {
    type: Sequelize.DATE
  }
})

const Building = sequelize.define('buildings', {
  building_number: {
    type: Sequelize.INTEGER,
    allowNull: false
  },
  street_number: {
    type: Sequelize.INTEGER,
    allowNull: false
  },
  street_name: {
    type: Sequelize.STRING,
    allowNull: false
  },
  borough: {
    type: Sequelize.ENUM(...BOROUGHS),
    allowNull: false
  },
  zip_code: Sequelize.INTEGER,
  neighborhood: Sequelize.STRING,
  block: Sequelize.INTEGER,
  year_built: Sequelize.INTEGER,
  sale_price: Sequelize.STRING,
  sale_date: Sequelize.STRING,
  total_units: Sequelize.INTEGER,
  complaints: Sequelize.ARRAY(Sequelize.TEXT),
  violations: Sequelize.ARRAY(Sequelize.TEXT)
})

Landlord.sync()
Building.sync()

const db = global.db = {
  Sequelize,
  sequelize
}

module.exports = db
