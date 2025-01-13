const express = require('express');
const router = express.Router();
const sketchController = require('../controllers/text2image');

router.post('/text2image', sketchController.processSketch);

module.exports = router;