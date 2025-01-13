# SketchAI

SketchAI is a powerful tool that converts hand-drawn sketches into professional images for marketplaces. This project leverages a custom diffusion model fine-tuned for this specific purpose, using advanced deep learning algorithms to automate marketplace integration.

## Technologies Used

- Python
- Node.js
- EJS
- Express
- LangChain
- NumPy
- PyTorch
- Transformers
- Diffusers
- HTML/CSS/JavaScript

## Installation

To install the dependencies, follow these steps:

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the required Node.js packages:
   ```bash
   npm install
   ```

## Running the Project Locally

1. Ensure you are in the virtual environment:

   ```bash
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Create a `.env` file in the root directory of the project and add your environment variables:

   ```plaintext
   PORT=3000
   ```

3. Start the Node.js server:

   ```bash
   npm start
   ```

4. Run the `app.py` script to start the backend server:

   ```bash
   python app.py
   ```

5. Use the `generate_image.py` script to generate images from sketches:

   ```bash
   python generate_image.py --input path/to/sketch --output path/to/output/image
   ```

6. Open your web browser and navigate to `http://localhost:3000` to use the application.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
