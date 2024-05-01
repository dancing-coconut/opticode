# Opticode

## About

Opticode is a revolutionary platform that combines cutting-edge machine learning algorithms with a deep understanding of software engineering best practices. It empowers developers to write more optimized, energy-efficient code by providing real-time feedback and recommendations during the coding process.

## Features

- **Code Optimization**: Opticode analyzes the input code and identifies areas for optimization, generating alternative code snippets that significantly reduce power consumption and CO2 emissions.
- **Sustainability Metrics**: The application tracks and reports on the environmental impact of the code, including estimated power consumption and CO2 emissions, empowering developers to make informed decisions about the sustainability of their projects.

## Installation

To get started with Opticode, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/dancing-coconut/opticode.git
   ```

2. Install Poetry, a Python project management tool:

   ```
   pip install poetry
   ```

3. Use Poetry to install the required dependencies:

   ```
   poetry add
   ```

   The required dependencies are:

   - `google-generativeai = "^0.5.2"`
   - `eco2ai = "^0.3.9"`
   - `streamlit = "^1.33.0"`
   - `pandas = "^1.4.1"`

4. Go to the Google AI Studio and generate an API key.

5. Create an `.env` file in the repository clone and add the `GOOGLE_API_KEY` environment variable with your API key:

   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

6. To run the application, use the following command:

   ```
   poetry run python -m streamlit run app.py
   ```

7. Open your web browser and navigate to `http://localhost:8501` to access the Opticode application.

## Usage

1. In the Opticode application, enter the coding language, the area to optimize, and the code you want to optimize.
2. Click the "Process" button to generate alternative code snippets with reduced power consumption and CO2 emissions.
3. Review the recommended alternative and compare the sustainability metrics to make an informed decision.

## Contributing

We welcome contributions from the community! If you'd like to contribute to Opticode, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.
