from website import app_instance

app = app_instance()

if __name__ == "__main__":
    app.run(debug=True)
