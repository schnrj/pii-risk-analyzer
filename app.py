import re
from flask import Flask, render_template, request
import plotly.io as pio
import plotly.graph_objects as go
import pandas as pd

app = Flask(__name__)

def detect_pii(text):
    categories = {
        'Financial Information': {
            'Credit Card Number': r'\b(?:\d[ -]*?){13,16}\b',
            'Bank Account Number': r'\b[0-9]{9,18}\b',
            'Credit/Debit Card CVV': r'\b\d{3}\b',
            'IFSC Code': r'\b[A-Z]{4}0[A-Z0-9]{6}\b',
            'PAN Number': r'\b[A-Z]{5}[0-9]{4}[A-Z]\b',
            
            'IBAN': r'\b[A-Z]{2}[0-9]{2}[A-Z0-9]{1,30}\b',
            'SWIFT Code': r'\b[A-Z]{4}[A-Z]{2}[A-Z0-9]{2}([A-Z0-9]{3})?\b'
        },
        'Medical Information': {
            'Medical Report': r'\b(Medical|Report|History|Diagnosis|Treatment|Prescription|Record)\b'
        },
        'Personal Information': {
            'Name': r'\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*\b',  # Updated to allow multiple word names
            'Email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b',
            'Phone': r'\b(\+91|0)?[6-9]\d{9}\b',
            'Address': r'\b\d{1,5}\s\w+\s(?:Street|St|Rd|Road|Ave|Avenue|Blvd|Boulevard|Lane|Ln|Dr|Drive)\b',
            'Birth Date': r'\b\d{1,2}/\d{1,2}/\d{2,4}\b',
            'Date of Birth': r'\b(0[1-9]|[12][0-9]|3[01])[-\/](0[1-9]|1[0-2])[-\/](19|20)\d{2}\b'
        },
        'Identification Information': {
            'Aadhaar Number': r'\b\d{4}\s?\d{4}\s?\d{4}\b',
            'Social Security Number': r'\b\d{3}-\d{2}-\d{4}\b',
            'Passport Number': r'\b[A-Z][0-9]{7}\b',
            'Driving License Number': r'\b[A-Z]{2}[0-9]{13}\b',
            'Driver License': r'\b([A-Z]{1,2}\d{1,7})\b',
            'Vehicle Registration Number': r'\b[A-Z]{2}[0-9]{2}[A-Z]{0,2}\d{4}\b'
        }
    }

    pii_detected_by_category = {}

    for category, patterns in categories.items():
        category_matches = {}
        for pii_type, pattern in patterns.items():
            matches = [match for match in re.findall(pattern, text) if match.strip()]  # Remove empty matches
            if matches:
                category_matches[pii_type] = matches
        if category_matches:
            pii_detected_by_category[category] = category_matches

    return pii_detected_by_category


def calculate_risk_score(pii_detected):
    sensitivity_scores = {
        'Credit Card Number': 8,
        'Bank Account Number': 7,
        'Credit/Debit Card CVV': 9,
        'IFSC Code': 6,
        'PAN Number': 7,
        
        'IBAN': 9,
        'SWIFT Code': 8,
        'Medical Report': 5,
        'Name': 4,
        'Email': 2,
        'Phone': 3,
        'Address': 5,
        'Birth Date': 4,
        'Date of Birth': 4,
        'Aadhaar Number': 8,
        'Social Security Number': 10,
        'Passport Number': 8,
        'Driving License Number': 7,
        'Driver License': 7,
        'Vehicle Registration Number': 6
    }

    risk_score = 0
    for category, pii_types in pii_detected.items():
        for pii_type, instances in pii_types.items():
            risk_score += sensitivity_scores.get(pii_type, 0) * len(instances)

    return risk_score

def visualize_pii_distribution_and_categories(pii_detected):
    try:
        # Prepare data for category-level plotting
        categories = []
        counts = []
        pii_types = []
        pii_counts = []

        for category, pii_dict in pii_detected.items():
            categories.append(category)
            counts.append(sum(len(instances) for instances in pii_dict.values()))

            for pii_type, instances in pii_dict.items():
                pii_types.append(f'{category} - {pii_type}')
                pii_counts.append(len(instances))

        # Custom color gradient
        colors = ['#77A1D3', '#79CBCA', '#E684AE']  # Smooth gradient colors

        # Create a Plotly figure for category-level distribution
        fig_category = go.Figure()
        fig_category.add_trace(go.Bar(
            x=categories,
            y=counts,
            name='Category Distribution',
            marker=dict(
                color=colors,
                line=dict(color='rgba(58, 71, 80, 1.0)', width=1.5)
            ),
            hoverinfo='x+y',
            text=counts,
            textposition='auto',
            width=0.6  # Increase bar width for clarity
        ))

        fig_category.update_layout(
            title='PII Distribution by Category',
            xaxis_title='Category',
            yaxis_title='Count',
            font=dict(family='Arial, sans-serif', size=14, color='#2a3f5f'),
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0)',
            template='plotly_white',
            margin=dict(l=30, r=30, t=50, b=50),
            showlegend=False,
            xaxis_tickangle= 0,
            bargap=0.2,  # Add slight spacing between bars
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Arial"
            )
        )

        category_distribution_html = pio.to_html(fig_category, full_html=False)

        # Create a Plotly figure for type-level distribution
        fig_type = go.Figure()
        fig_type.add_trace(go.Bar(
            x=pii_types,
            y=pii_counts,
            name='PII Type Distribution',
            marker=dict(
                color=colors[::-1],  # Reverse gradient for variety
                line=dict(color='rgba(58, 71, 80, 1.0)', width=1.5)
            ),
            hoverinfo='x+y',
            text=pii_counts,
            textposition='auto',
            width=0.6
        ))

        fig_type.update_layout(
            title='PII Distribution by Type within Each Category',
            xaxis_title='PII Type',
            yaxis_title='Count',
            font=dict(family='Arial, sans-serif', size=14, color='#2a3f5f'),
            plot_bgcolor='rgba(255,255,255,0.9)',
            paper_bgcolor='rgba(255,255,255,0)',
            template='plotly_white',
            margin=dict(l=30, r=30, t=50, b=50),
            showlegend=False,
            xaxis_tickangle= 0,
            bargap=0.2,
            hoverlabel=dict(
                bgcolor="white",
                font_size=13,
                font_family="Arial"
            )
        )

        pii_type_distribution_html = pio.to_html(fig_type, full_html=False)

    except Exception as e:
        print(f"An error occurred: {e}")
        category_distribution_html = None
        pii_type_distribution_html = None

    return category_distribution_html, pii_type_distribution_html


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/classify', methods=['POST'])
def classify():
    text = request.form['text']
    # Detect PII
    pii_detected = detect_pii(text)
    print(f"Detected PII: {pii_detected}")  # Debugging print

    # Calculate Risk Score
    risk_score = calculate_risk_score(pii_detected)
    print(f"Risk Score: {risk_score}")  # Debugging print

    # Visualize PII Distribution
    category_distribution_html, pii_type_distribution_html = visualize_pii_distribution_and_categories(pii_detected)

    # Ensure the data is passed to the template correctly
    return render_template('result.html', 
                           pii_detected=pii_detected, 
                           risk_score=risk_score,
                           category_distribution_html=category_distribution_html,
                           pii_type_distribution_html=pii_type_distribution_html)



if __name__ == '__main__':
    app.run(debug=True)

#For SQL DATABASE INTEGRATION
# from flask import Flask, request, jsonify, render_template
# import pandas as pd
# from sqlalchemy import create_engine
# import boto3

# app = Flask(__name__)

# # Database connection parameters
# db_user = 'your_username'
# db_password = 'your_password'
# db_host = 'localhost'
# db_name = 'your_database_name'

# # S3 connection parameters
# aws_access_key_id = 'your_access_key_id'
# aws_secret_access_key = 'your_secret_access_key'
# bucket_name = 'your_bucket_name'

# # Create a SQLAlchemy engine
# connection_string = f'mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}'
# engine = create_engine(connection_string)

# # Initialize an S3 client
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=aws_access_key_id,
#     aws_secret_access_key=aws_secret_access_key
# )

# # Define sensitivity levels for PII
# sensitivity = {
#     'Name': 'Low',
#     'Email': 'Medium',
#     'SSN': 'High',
#     'Credit Card Number': 'High',
#     'IP Address': 'Medium'
# }

# tef = {'Low': 0.1, 'Medium': 0.3, 'High': 0.7}
# vulnerability = {'Low': 0.1, 'Medium': 0.5, 'High': 0.9}
# loss_magnitude = {'Low': 10, 'Medium': 50, 'High': 200}

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/api/v1/data/ingest', methods=['POST'])
# def ingest_data():
#     source = request.json['source']
#     if source == 'csv':
#         data = request.json['data']
#         df = pd.DataFrame(data)
#     elif source == 'sql':
#         query = request.json['query']
#         df = pd.read_sql(query, engine)
#     elif source == 's3':
#         file_key = request.json['file_key']
#         s3_client.download_file(bucket_name, file_key, 'downloaded_file.csv')
#         df = pd.read_csv('downloaded_file.csv')
#     else:
#         return jsonify({'status': 'failure', 'message': 'Invalid data source'}), 400

#     return jsonify({
#         'status': 'success',
#         'data': df.to_dict(orient='records')
#     })

# @app.route('/api/v1/pii/classify', methods=['POST'])
# def classify_pii():
#     data = request.json['data']
#     df = pd.DataFrame(data)

#     df_classified = df.copy()
#     df_classified['Sensitivity'] = df.columns.map(sensitivity)

#     return jsonify({
#         'status': 'success',
#         'classified_data': df_classified.to_dict(orient='records')
#     })

# @app.route('/api/v1/risk/calculate', methods=['POST'])
# def calculate_risk():
#     classified_data = request.json['classified_data']
#     df_classified = pd.DataFrame(classified_data)

#     df_classified['TEF'] = df_classified['Sensitivity'].map(tef)
#     df_classified['Vulnerability'] = df_classified['Sensitivity'].map(vulnerability)
#     df_classified['Loss Magnitude'] = df_classified['Sensitivity'].map(loss_magnitude)
#     df_classified['Risk'] = df_classified['TEF'] * df_classified['Vulnerability'] * df_classified['Loss Magnitude']

#     return jsonify({
#         'status': 'success',
#         'risk_scores': df_classified[['Risk']].to_dict(orient='records')
#     })

# if __name__ == '__main__':
#     app.run(debug=True)


