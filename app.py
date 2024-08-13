from flask import Flask
from routes import mountRoutes
from data.mlb_data_handler import load_mlb_data

# Init app
app = Flask(__name__)

# Load MLB roster data
mlb_data = load_mlb_data()

# Mount routes
app = mountRoutes(app, mlb_data)

# Start app
if __name__ == '__main__':
    app.run(debug=True)