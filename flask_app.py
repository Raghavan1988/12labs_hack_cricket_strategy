### inspired by the hello world example
import sys
import os.path

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

directory = "dataset"

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
)

# check if index already exists
PERSIST_DIR = "dataset" + "_persisterd"
if not os.path.exists(PERSIST_DIR):
    # load the documents and create the index
    documents = SimpleDirectoryReader(directory).load_data()
    index = VectorStoreIndex.from_documents(documents)
    # store it for later
    index.storage_context.persist(persist_dir=PERSIST_DIR)
else:
    # load the existing index
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)



from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML template for the input form
FORM_HTML = """
<!doctype html>
<html>
<head>
    <title>Glenn Maxwell</title>
</head>
<body>
    <h3>We have extracted Glenn Maxwell's batting technique from a few Youtube videos and cricinfo commentary. Ask question about Maxwell's batting</h3>
    <form action="/submit" method="post">
        <input type="text" name="text_input" size=1000 placeholder="Enter your text here" required>
        <input type="submit" value="Submit">
    </form>
</body>
</html>
"""

maxwell_dataset = ""
with open("dataset/maxwell_cricinfo.txt", "r") as file:
    cricinfo = file.read().replace("\n", " ")
    maxwell_dataset += cricinfo

with open("dataset/maxwell_innings_video_analysis.txt","r") as file:
    labs12 = file.read().replace("\n", " ")
    maxwell_dataset += labs12


print(len(maxwell_dataset))
RESULT_HTML = """
<!doctype html>
<html>
<head>
    <title>Submitted Text</title>
</head>
<body>
    <p>{{ submitted_text }}</p>
    <a href="/">Back</a>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return FORM_HTML

@app.route('/submit', methods=['POST'])
def submit():
    text = request.form['text_input']
    query = text
    # Either way we can now query the index
    query_engine = index.as_query_engine()
    response = query_engine.query(query)
    print(response)
    return render_template_string(RESULT_HTML, submitted_text=response)

if __name__ == '__main__':
    app.run(debug=True)
