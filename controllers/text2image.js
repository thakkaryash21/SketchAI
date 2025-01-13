const multer = require('multer');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

// Multer setup for file uploads
const upload = multer({ dest: 'public/uploads/' });

exports.upload = upload.single('image');


// exports.processSketch =  async (req, res) => {
//     const imagePath = req.file.path;
    
//     try {
//         const formData = new FormData();
//         formData.append('image', fs.createReadStream(imagePath));

//         const response = await axios.post('http://0.0.0.0:5000/', formData, {
//             headers: {
//                 'Content-Type': `multipart/form-data`
//             }
//         });

//         const caption = response.data.caption;
//         fs.unlinkSync(imagePath); // Clean up the uploaded file
//         res.render('result', { caption });
//     } catch (error) {
//         console.error(error);
//         res.status(500).send('Error generating caption');
//     }
// };


exports.processSketch = async (req, res) => {
    const prompt = req.body.prompt; // Assuming the prompt is sent in the request body
    
    if (!prompt) {
        return res.status(400).send('Prompt is required');
    }

    try {
        // Send the POST request with the prompt in the request body
        const response = await axios.post('http://127.0.0.1:3002/generate', 
            { prompt: prompt }, 
            {
                headers: {
                    'Content-Type': 'application/json',
                },
                responseType: 'arraybuffer' // Make sure the response is an image
            }
        );

        console.log(response.data); // Check the image buffer

        // Save the image
        const imageBuffer = response.data; // Image data as buffer
        const imageFileName = 'generated_image.png';
        const outputPath = path.join(__dirname, '..', 'public', imageFileName);

        // Save the image to disk
        fs.writeFileSync(outputPath, imageBuffer);

        // Send back the URL of the saved image
        res.render('result3', { imageUrl: `${imageFileName}` });


        // const imageUrl = response.data.image_url;
        // res.render('result', { imageUrl });
    } catch (error) {
        console.error(error);
        res.status(500).send('Error generating image');
    }
};


// exports.processSketch = async (req, res) => {
//     try {

//         // Convert uploaded image to base64
//         const filePath = path.join(__dirname, '../', req.file.path);
//         const imageData = fs.readFileSync(filePath).toString('base64');

//         // Call OpenAI API with a prompt describing the image data
//         const openaiResponse = await axios.post(
//             'https://api.openai.com/v1/chat/completions',
//             {
//                 model: 'gpt-3.5-turbo',
//                 messages: [
//                     {
//                         role: 'system',
//                         content: 'You are an assistant that describes sketches based on image data.'
//                     },
//                     {
//                         role: 'user',
//                         content: `Here is an image encoded in base64: ${imageData}. Describe what the sketch might depict.`
//                     }
//                 ],
//                 max_tokens: 200,
//                 temperature: 0.7,
//             },
//             {
//                 headers: {
//                     'Authorization': `Bearer ${process.env.OPENAI_API_KEY}`,
//                     'Content-Type': 'application/json',
//                 }
//             }
//         );

//         const description = openaiResponse.data.choices[0].message.content;

//         // Render result page with the sketch description
//         res.render('result', { description, imagePath: req.file.filename });
//     } catch (error) {
//         console.error(error.response?.data || error.message);
//         res.status(500).send('Error processing sketch.');
//     }
// };