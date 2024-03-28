import csv
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Define CSV header
csv_header = ["ID","Name","Case","Percentage","Remarks","Correct" "Parameters","False Parameters","Timestamp"]

@app.route('/fetch',methods=['GET'])
def fetch():
    id_to_find = request.args.get('id')
    if not id_to_find:
        return jsonify({'error': 'ID parameter is required'}), 400
    
    # Read the CSV file and search for the row with the given ID
    with open('Audit.csv', 'r', newline='') as file:
        reader = csv.DictReader(file, fieldnames=csv_header)
        for row in reader:
            if row['ID'] == id_to_find:
                return jsonify(row), 200

    return jsonify({'error': 'ID not found'}), 404

@app.route('/', methods=['POST'])
def write2csv():
    data = request.get_json()
    print(data)  # Debug: Print received JSON data
    
    # Extract data fields from the JSON object
    id_val = data.get('data', {}).get('id', '')
    name_val = data.get('data', {}).get('Name', '')
    case_val = data.get('data', {}).get('Case', '')
    correct_params = ', '.join(data.get('data', {}).get('Correct', []))
    false_params = ', '.join(data.get('data', {}).get('False', []))
    remarks_val = data.get('data', {}).get('Remarks', '')
    perce = (len(data.get('data', {}).get('Correct', [])) / 6) * 100
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # You can add logic to extract the timestamp if it's part of your data
    
    # Prepare data row for CSV
    csv_row = [id_val, name_val, case_val, round(perce), remarks_val, correct_params, false_params, timestamp]
    
    # Open CSV file in append mode and write the data
    with open('Audit.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        # Check if file is empty and write header if needed
        if file.tell() == 0:
            writer.writerow(csv_header)
        writer.writerow(csv_row)
    
    return "Inserted!"

if __name__ == '__main__':
    app.run(debug=True)
