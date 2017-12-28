const express = require('express');
const router = express.Router();

router.get('/', (req, res, next) => {
    // res.send('GET products details');
    res.status(200).json({
        message: 'Handling GET requests to /products'
    });
});

router.post('/', (req, res, next) => {
    // res.send('POST new product to server');
    const product = {
        name: req.body.name,
        price: req.body.price
    };
    res.status(200).json({
        message: 'Handling POST request to /products',
        product: product
    });
});

router.get('/:productId', (req, res, next) => {
    // GET specific ID from Server
    const id = req.params.productId;
    if (id === 'special') {
        res.status(200).json({
            message: 'You just discover the special ID'
        });
    } else {
        res.status(200).json({
            message: 'you passed an ID',
            id: id
        })
    }
});

router.patch('/:productId', (req, res, next) => {
    res.status(200).json({
        message: 'Updated product !',
        id: req.params.productId
    });
});

router.delete('/:productId', (req, res, next) => {
    res.status(200).json({
        message: 'DELETED product !',
        id: req.params.productId
    });
});

module.exports = router;