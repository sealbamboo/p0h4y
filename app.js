const express = require('express');
const morgan = require('morgan');
const bodyParser = require('body-parser');
const app = express();


// -----------------------------------
// Load All JS files
// -----------------------------------
const navigationRoutes = require('./api/navigation');
const productRoutes = require('./api/products');


// -----------------------------------
// Load Middleware support by ExpressJS
// -----------------------------------
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


// -----------------------------------
// CORS: Cross-Origin Resource Sharing
// *: is used for every http request
// -----------------------------------
app.use((req, res, next) => {
    res.header('Access-Control-Allow-Origin', '*');
    res.header(
        'Access-Control-Allow-Headers',
        'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    );
    if (req.method === 'OPTIONS') {
        res.header(
            'Access-Control-Allow-Methods',
            'PUT, POST, PATCH, DELETE, GET'
        )
        return res.status(200).json({});
    }
});


// -----------------------------------
// Granted URL to reference JS files
// OR
// Routes which should handle requests
// -----------------------------------
app.use('/', navigationRoutes);
app.use('/product', productRoutes);


// -----------------------------------
// ALWAYS KEEP LAST Router
// The 404 & 500 Route
// -----------------------------------
app.get('*', function(req, res, next) {
    res.status(404).json({
        message: 'Not found'
    });
});

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.json({
        error: {
            message: error.message
        }
    });
})

module.exports = app;