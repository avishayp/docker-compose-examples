const express = require('express')
const app = express()
const port = process.env.PORT || 9000

app.get('/', (req, res) => res.send('api ok'))

app.get('/echo', (req, res) => res.json(req.query))

const server = app.listen(port, '0.0.0.0', () => {
    console.log('server listening on port', port)
})

server.on('close', () => {
    console.log('server shuting down...')
})
