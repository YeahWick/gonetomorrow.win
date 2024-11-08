from fasthtml.common import FastHTML, serve

app = FastHTML()

@app.get("/home")
def home():
    return "<h1>Hello, hello</h1>"

serve()
