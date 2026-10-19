from app import create_app

app = create_app()

if __name__ == "__main__":
    # debug dimatikan agar aman (Bandit menandai debug=True sebagai temuan)
    app.run(host="127.0.0.1", port=5000, debug=False)