from flask import Flask, render_template, request, jsonify, redirect
from elasticsearch import Elasticsearch, exceptions

app = Flask(__name__)
db = Elasticsearch('http://localhost:9200')


# *************** define the site routes ***********************
@app.route('/')
def index():
    try:
        index_exists = db.indices.exists(index="offres_emploi")
        if(index_exists==True):
            response = db.search(index="offres_emploi", body={"query": {"match_all": {}}})
            offres = [hit['_source'] for hit in response['hits']['hits']]
        else:
            offres = []
    except exceptions.ElasticsearchException as e:
        offres = []
    return render_template('index.html', offres=offres, index_exists=index_exists)


@app.route('/add-offre')
def add_offre():
    return render_template('offre_emploi_form.html')


# *************** define the API routes ***********************
@app.route('/create-index', methods=['POST'])
def create_index():
    # Extract index name from the request's JSON body
    index_name = "offres_emploi"
    # Define the new mappings structure
    mappings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "employment_type": {"type": "text"},
                "referent": {"type": "text"},
                "end_service": {"type": "date"},
                "origin": {"type": "text"},
                "date_update": {"type": "date"},
                "skills": {"type": "text"},
                "start_service": {"type": "date"},
                "job_title": {"type": "text"},
                "date_publication": {"type": "date"},
                "job_description": {"type": "text"},
                "id": {"type": "text"},
                "company_name": {"type": "text"},
                "industries": {"type": "text"},
                "location": {"type": "text"},
                "internal_reference": {"type": "text"},
                "seniority": {"type": "integer"},
                "status": {"type": "text"}
            }
        }
    }
    # Create the index if it doesn't exist
    try:
        if not db.indices.exists(index=index_name):
            db.indices.create(index=index_name, body=mappings)
            return redirect('/')
        else:
            return jsonify({"message": f"Index {index_name} already exists."}), 200
    except exceptions.ElasticsearchException as e:
        return jsonify({"error": f"Error creating index {index_name}: {e}"}), 500


@app.route('/submit-offre', methods=['POST'])
def submit_offre():
    if(not db.indices.exists(index="offres_emploi")):
        return jsonify({"error": "Index 'offres_emploi' does not exist. Please create it first."}), 500
    # Extracting form data
    offre_data = {
        "employment_type": request.form.get('employment_type'),
        "referent": request.form.get('referent'),
        "end_service": request.form.get('end_service'),
        "origin": request.form.get('origin'),
        "date_publication": request.form.get('date_publication'),
        "skills": request.form.get('skills'),
        "start_service": request.form.get('start_service'),
        "date_fin": request.form.get('date_fin'),
        "job_title": request.form.get('job_title'),
        "job_description": request.form.get('job_description'),
        "id": request.form.get('id'),
        "company_name": request.form.get('company_name'),
        "industries": request.form.get('industries'),
        "location": request.form.get('location'),
        "internal_reference": request.form.get('internal_reference'),
        "seniority": request.form.get('seniority'),
        "experience": request.form.get('experience'),
        "status": request.form.get('status')
    }
    try:
        db.index(index="offres_emploi", document=offre_data)
        return redirect('/')
    except exceptions.ElasticsearchException as e:
        return jsonify({"error": f"Error adding offre d'emploi: {e}"}), 500

@app.route('/delete-index', methods=['GET', 'POST'])
def delete_index():
    index_name = "offres_emploi"
    try:
        if db.indices.exists(index=index_name):
            db.indices.delete(index=index_name)
            return redirect('/')
        else:
            return jsonify({"message": f"Index {index_name} does not exist."}), 404
    except exceptions.ElasticsearchException as e:
        return jsonify({"error": f"Error deleting index {index_name}: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
