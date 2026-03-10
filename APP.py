from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

app = Flask(__name__)

# Load dataset
df = pd.read_csv("retail_sales.csv")

# Remove missing values
df.dropna(inplace=True)

# Create plots folder if not exists
if not os.path.exists("static/plots"):
    os.makedirs("static/plots")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():

    # Basic statistics
    mean_calories = round(df['Calories'].mean(), 2)
    median_calories = round(df['Calories'].median(), 2)
    std_calories = round(df['Calories'].std(), 2)

    # Graph 1: Calories by Category
    plt.figure(figsize=(10,6))
    sns.barplot(x="Category", y="Calories", data=df, palette="Set2")
    plt.xticks(rotation=45)
    plt.title("Calories by Food Category")
    plt.tight_layout()
    plt.savefig("static/plots/category_calories.png")
    plt.close()

    # Graph 2: Fat vs Calories
    plt.figure(figsize=(10,6))
    sns.scatterplot(
        x="Total Fat",
        y="Calories",
        hue="Category",
        data=df,
        palette="bright",
        s=100
    )
    plt.title("Fat vs Calories Relationship")
    plt.tight_layout()
    plt.savefig("static/plots/fat_calories.png")
    plt.close()

    # Graph 3: Sugar vs Calories Bubble Chart
    plt.figure(figsize=(10,6))
    sns.scatterplot(
        x="Sugars",
        y="Calories",
        size="Protein",
        hue="Category",
        data=df,
        palette="cool",
        sizes=(20,300)
    )
    plt.title("Sugar vs Calories (Bubble size = Protein)")
    plt.tight_layout()
    plt.savefig("static/plots/sugar_calories.png")
    plt.close()

    # Graph 4: Correlation Heatmap
    plt.figure(figsize=(10,8))
    sns.heatmap(df.corr(numeric_only=True), annot=True, cmap="coolwarm")
    plt.title("Nutrition Correlation Heatmap")
    plt.tight_layout()
    plt.savefig("static/plots/heatmap.png")
    plt.close()

    return render_template(
        "dashboard.html",
        mean_calories=mean_calories,
        median_calories=median_calories,
        std_calories=std_calories
    )


if __name__ == "__main__":
    app.run(debug=True)