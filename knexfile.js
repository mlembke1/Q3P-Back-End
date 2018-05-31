module.exports = {
  development: {
    client: 'pg',
    connection: 'postgres://localhost/Q3P_dev'
  },
  test: {
    client: 'pg',
    connection: 'postgres://localhost/Q3P_test'
  },
  production: {
    client: 'pg',
    connection: process.env.DATABASE_URL
  }
}

//comment
