const express = require('express');
const router = express.Router();
const sketchController = require('../controllers/image2text');
const { render } = require('ejs');

router.get('/amazos', async (req, res) => {
    return res.render('amazos');
});

module.exports = router;