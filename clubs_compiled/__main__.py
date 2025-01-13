from . import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

# TODO: Get a better way to initialize the api and handle changes to the form