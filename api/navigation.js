const express = require('express')
const router = express.Router()

// define home page route
router.get('/', (req, res, next) => {
    res.send('This is Homepage')
})

// define "About Us" route
router.get('/about', (req, res, next) => {
    res.send('This is \"About Us\" page')
})

// define "Contact Me" route
router.get('/contact', function(req, res, next) {
    res.send('This is \"Contact Me\" page')
})

module.exports = router