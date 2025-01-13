const multer = require('multer');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');


exports.processSketch = async (req, res) => {
    const prompt = req.body.caption;
    console.log(prompt);
    
    if (!prompt) {
        return res.status(400).send('Prompt is required');
    }

    try {
        // Send the POST request with the prompt in the request body
        const response = await axios.post('http://127.0.0.1:3001/enhance-description', 
            { caption: prompt }, 
            {
                headers: {
                    'Content-Type': 'application/json',
                }
            }
        );

        console.log(response.data); // Check the image buffer
        

        // Save the image
        const description = response.data.enhanced_description;

        res.render('result2', { description });


        // const imageUrl = response.data.image_url;
        // res.render('result', { imageUrl });
    } catch (error) {
        console.error(error);
        res.status(500).send('Error generating image');
    }
};
