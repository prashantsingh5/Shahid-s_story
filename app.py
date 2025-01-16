from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from fuzzywuzzy import process

app = Flask(__name__)

# Load and preprocess data
data = pd.read_csv("soldiers.csv")  # Ensure your dataset is saved as `soldiers.csv`
data = data.fillna("No information available at the moment. If you have details to contribute, please fill out the form to honor their legacy.")
available_stories = data[data["Story"] != "No information available at the moment. If you have details to contribute, please fill out the form to honor their legacy."]

# Route for the home page
@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    search_query = ""

    if request.method == "POST":
        search_query = request.form.get("search")
        if search_query:
            # Fuzzy matching for recommendations
            soldier_names = available_stories["Name"].tolist()
            recommendations = process.extract(search_query, soldier_names, limit=5)

    return render_template("home.html", names=available_stories["Name"].tolist(), recommendations=recommendations, search_query=search_query)

# Route for the story page
@app.route("/story/<name>")
def story(name):
    soldier = data[data["Name"] == name].iloc[0]  # Get the soldier's details
    return render_template("story.html", soldier=soldier)

if __name__ == "__main__":
    app.run(debug=True)
