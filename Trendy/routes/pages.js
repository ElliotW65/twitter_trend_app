//include express module 
const express = require('express');
const router = express.Router();

//route to the homepage
//request retrieves
//response send to the front end
router.get('/', (req, res) => {
    res.render('index');
});

router.get('/map', (req, res) => {
    res.render('map');
});


//export router
module.exports = router;
