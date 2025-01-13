const express = require('express');
const router = express.Router();
const sketchController = require('../controllers/text2text');

router.post('/text2text', sketchController.processSketch);

module.exports = router;