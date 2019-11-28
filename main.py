from flaskblogmy import create_app # imports from __init__.py when working with packages

app = create_app()

if __name__ == "__main__":#only true if script run directly - using somewhere else main would be different
    app.run(debug=True)

# linode, digital ocean, auus
# nginx, gunicorn
