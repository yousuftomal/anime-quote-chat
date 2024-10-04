from flask import Flask, render_template, request
import pandas as pd
import random

app = Flask(__name__)

# Read the CSV file with semicolon as the delimiter and ignore columns with no headers
file_path = 'lessreal-data.csv'
df = pd.read_csv(file_path, delimiter=';', index_col='ID', usecols=lambda column: not column.startswith('Unnamed'))

# Drop rows with NaN values in the 'Quote' column
df = df.dropna(subset=['Quote'])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    # Filter quotes based on user input (simple example)
    relevant_quotes = df[df['Quote'].str.contains(user_input, case=False, na=False)]
    
    if not relevant_quotes.empty:
        # Convert the generator to a list before using random.choice
        quote_list = list(relevant_quotes.iterrows())
        selected_quote_row = random.choice(quote_list)
        selected_character = selected_quote_row[1]['Character']
        selected_quote = selected_quote_row[1]['Quote']
    else:
        selected_character = "Bot"
        selected_quote = "I'm sorry, I couldn't find a relevant quote for that."

    return render_template('index.html', user_input=user_input, selected_character=selected_character, selected_quote=selected_quote)

if __name__ == '__main__':
    app.run(debug=True)
