import base64
from flask import Flask, render_template, request, jsonify, redirect, current_app
from elasticsearch import Elasticsearch, exceptions


app = Flask(__name__)
db = Elasticsearch('http://localhost:9200')


# *************** define the site routes ***********************
@app.route('/')
def index():
    try:
        index_exists = db.indices.exists(index="offres_emploi")
        if (index_exists == True):
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


@app.route('/offer', methods=['GET', 'POST'])
def offer():
    try:
        response = db.search(index="offres_emploi", body={"query": {"match_all": {}}})
        offres = [hit['_source'] for hit in response['hits']['hits']]
    except exceptions.ElasticsearchException as e:
        offres = []
    return render_template('offer_client_side.html', offres=offres)


# *************** define the API routes ***********************
@app.route('/create-index', methods=['POST'])
def create_index_offres_emploi():
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
                "date_fin": {"type": "date"},
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
@app.route('/create_postuler', methods=['POST'])
def create_postuler():
    # Ensure Elasticsearch index exists for 'postuler'
    index_name = "postuler"
    mappings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "offer_id": {"type": "text"},
                "first_name": {"type": "text"},
                "last_name": {"type": "text"},
                "file": {"type": "text"}  # Change to text to store base64 string
            }
        }
    }
    try:
        if not db.indices.exists(index=index_name):
            db.indices.create(index=index_name, body=mappings)
            return redirect('/')
        else:
            return jsonify({"message": f"Index {index_name} already exists."}), 200
    except exceptions.ElasticsearchException as e:
        return jsonify({"error": f"Error creating index {index_name}: {e}"}), 500
# ***************define the crud routes ***********************

@app.route('/submit-offre', methods=['POST'])
def submit_offre():
    if (not db.indices.exists(index="offres_emploi")):
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
    index_name = "postuler"
    try:
        if db.indices.exists(index=index_name):
            db.indices.delete(index=index_name)
            return redirect('/')
        else:
            return jsonify({"message": f"Index {index_name} does not exist."}), 404
    except exceptions.ElasticsearchException as e:
        return jsonify({"error": f"Error deleting index {index_name}: {e}"}), 500


@app.route('/offer-details/<offer_id>')
def offer_details(offer_id):
    current_app.logger.info(f"Fetching details for offer ID: {offer_id}")
    try:
        response = db.get(index="offres_emploi", id=offer_id)
        current_app.logger.debug(f"Elasticsearch response: {response}")
        if response.get('found', False):
            return jsonify(response['_source'])
        else:
            current_app.logger.error(f"Offer not found for ID {offer_id}")
            return jsonify({"error": "Offer not found"}), 404
    except exceptions.NotFoundError as e:
        current_app.logger.error(f"Offer not found for ID {offer_id}: {e}")
        return jsonify({"error": "Offer not found"}), 404
    except exceptions.ElasticsearchException as e:
        current_app.logger.error(f"Elasticsearch exception for offer ID {offer_id}: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/apply-for-job/<offer_id>', methods=['POST'])
def apply_for_job(offer_id):
    # Ensure Elasticsearch index exists for 'postuler'
    index_name = "postuler"
    mappings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "offer_id": {"type": "text"},
                "first_name": {"type": "text"},
                "last_name": {"type": "text"},
                "file": {"type": "text"}  # Change to text to store base64 string
            }
        }
    }
    if not db.indices.exists(index=index_name):
        db.indices.create(index=index_name, body=mappings)

    # Extracting data from the form
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    if 'file' in request.files:
        file_content = request.files['file'].read()
        file_base64 = base64.b64encode(file_content).decode('utf-8')  # Encode file content to base64
    else:
        file_base64 = None

    # Constructing document to be indexed
    document = {
        "offer_id": offer_id,
        "first_name": first_name,
        "last_name": last_name,
        "file": file_base64
    }

    # Indexing the document
    try:
        db.index(index=index_name, document=document)
        return jsonify({"message": "Application submitted successfully"}), 200
    except exceptions.ElasticsearchException as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
