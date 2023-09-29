from __init__ import init_app

app = init_app()

Development = True

if Development == False:
    if __name__ == "__main__":
        app.run(debug=False)
else:
    if __name__ == "__main__":
        app.run(debug=True)

