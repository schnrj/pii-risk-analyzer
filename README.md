# PII Detection and Risk Analysis Application

## Overview

This application is designed to detect Personally Identifiable Information (PII) in text, classify the detected PII, calculate a risk score, and visualize the results. It uses a combination of regular expressions and potential NLP techniques for accurate PII detection and classification.

## Features

- Detects various types of PII (e.g., names, email addresses, phone numbers, financial information)
- Classifies detected PII into categories
- Calculates a risk score based on the type and amount of PII detected
- Visualizes PII distribution by category and type
- Provides a user-friendly web interface for input and result display
- Extensible architecture allowing for future enhancements

## Tech Stack

- Backend: Python, Flask
- Frontend: HTML, CSS (Bootstrap), JavaScript
- Data Visualization: Plotly
- Database: SQL (optional, for future implementation)
- NLP: Potential integration with BERT or similar models

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/Smruti0603/IDFY_HACKATHON.git
   cd pii-detection-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`

3. Enter the text you want to analyze in the provided text area

4. Click the "Classify PII" button to process the text

5. View the results, including detected PII, risk score, and visualizations

## Project Structure

```
pii-detection-app/
│
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html         # Home page template
│   └── result.html        # Results page template
├── static/
│   └── css/
│       └── style.css      # Custom CSS styles
├── pii_detector.py        # PII detection logic
├── pii_classifier.py      # PII classification logic
├── risk_calculator.py     # Risk score calculation
├── visualizer.py          # Data visualization functions
├── requirements.txt       # Python dependencies
└── README.md              # This file
```

## Future Enhancements

- Integration of BERT or other NLP models for improved PII detection and classification
- Database integration for storing and analyzing historical data
- Support for additional document types (PDF, DOC, etc.)
- API expansion for integration with other systems
- Enhanced security features (encryption, access control)
- Customizable PII detection and classification rules
- Machine learning models for continuous improvement of accuracy

## Contributing

Contributions to improve the PII Detection and Risk Analysis Application are welcome. Please feel free to submit a Pull Request.

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contact

For any queries or suggestions, please open an issue in the GitHub repository.
