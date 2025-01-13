const multer = require('multer');
const axios = require('axios');
const fs = require('fs');
const path = require('path');
const FormData = require('form-data');

// Multer setup for file uploads
const upload = multer({ dest: 'public/uploads/' });

exports.upload = upload.single('image');


exports.processSketch =  async (req, res) => {
    const uploadedImagePath = req.file.path;
    const renamedImagePath = path.join(path.dirname(uploadedImagePath), 'uploaded_image.png');
    
    try {

        fs.renameSync(uploadedImagePath, renamedImagePath);

        const formData = new FormData();
        formData.append('image', fs.createReadStream(renamedImagePath));

        const response = await axios.post('http://0.0.0.0:5100/caption', formData, {
            headers: {
                'Content-Type': `multipart/form-data`
            }
        });

        const caption = response.data.caption;
        res.render('result', { caption });
    } catch (error) {
        console.error(error);
        res.status(500).send('Error generating caption');
    }
};

