from flask import Flask, render_template, request, jsonify, redirect, current_app, Response
from elasticsearch import Elasticsearch, exceptions
from werkzeug.utils import secure_filename
import os
import base64

app = Flask(__name__)
db = Elasticsearch('http://localhost:9200')
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# *************** Ensure the upload folder exists  ***************
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# *************** Ensure the upload folder exists  ***************
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# *************** define the site routes ***********************
@app.route('/')
def index():
    try:
        index_exists = db.indices.exists(index="offres_emploi")
        postuler_index_exists = db.indices.exists(index="postuler")
        if (index_exists == True):
            response = db.search(index="offres_emploi", body={"size":10000, "query": {"match_all": {}}})
            offres = [hit['_source'] for hit in response['hits']['hits']]
        else:
            offres = []
    except exceptions.ElasticsearchException as e:
        offres = []
    n = len(offres)
    return render_template('index.html', offres=offres, n=n, index_exists=index_exists, postuler_index_exists=postuler_index_exists)
@app.route('/offer/<offer_id>')
def offer_detail(offer_id):
    # Fetch the offer details from the database
    request = db.search(index="offres_emploi", body={"query": {"match": {"id": offer_id}}})
    offer = request['hits']['hits'][0]['_source']
    return render_template('details.html', offer=offer)
@app.route('/update/<offer_id>', methods=['GET', 'POST'])
def update_offer(offer_id):
    if request.method == 'POST':
        # Handle form submission for updating the offer
        offer_data = {
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
            db.update(index="offres_emploi", id=offer_id, body={"doc": offer_data})
            return redirect('/')
        except exceptions.ElasticsearchException as e:
            return jsonify({"error": f"Error updating offre d'emploi: {e}"}), 500
    else:
        # Fetch the offer details to pre-fill the form
        offer = db.get(index="offres_emploi", id=offer_id)['_source']
        return render_template('offre_emploi_form.html', offer=offer)

@app.route('/delete/<offer_id>', methods=['GET', 'POST'])
def delete_offer(offer_id):
    try:
        db.delete(index="offres_emploi", id=offer_id)
        return redirect('/')
    except exceptions.ElasticsearchException as e:
        return jsonify({"error": f"Error deleting offre d'emploi: {e}"}), 500

@app.route('/add-offre')
def add_offre():
    return render_template('offre_emploi_form.html')


@app.route('/offer', methods=['GET', 'POST'])
def offer():
    try:
        # Extract the 'lang' parameter from the query string
        lang = request.args.get('lang', 'en').lower()

        # Validate the 'lang' parameter
        if lang not in ['en', 'fr', '']:
            lang = 'en'
        page = request.args.get('page', 1, type=int)
        per_page = 10
        start = (page - 1) * per_page

        # Retrieve filter values from query parameters
        location_filter = request.args.get('locationFilter')
        company_filter = request.args.get('companyFilter')
        employment_type_filter = request.args.get('employmentTypeFilter')
        date_filter = request.args.get('dateFilter')
        sort_by = request.args.get('sort_by', 'date')  # Default sort by date

        print(
            f"Filters - Location: {location_filter}, Company: {company_filter}, Employment Type: {employment_type_filter}, Date: {date_filter}, Sort By: {sort_by}")

        # Construct a dynamic query based on filters
        query_filters = [{"range": {"date_publication": {"lte": "now"}}},  # Publication date is today or before
                         {"range": {"date_fin": {"gte": "now"}}}]  # End date is today or after

        if location_filter:
            query_filters.append({"match": {"location": location_filter}})
        if company_filter:
            query_filters.append({"match": {"company_name": company_filter}})
        if employment_type_filter:
            query_filters.append({"term": {"employment_type.keyword": employment_type_filter}})

        # Date filter logic
        if date_filter == "last_week":
            query_filters.append({"range": {"date_publication": {"gte": "now-1w/d"}}})
        elif date_filter == "last_2_weeks":
            query_filters.append({"range": {"date_publication": {"gte": "now-2w/d"}}})
        elif date_filter == "last_month":
            query_filters.append({"range": {"date_publication": {"gte": "now-1M/d"}}})

        # Construct the final query
        final_query = {"bool": {"must": query_filters}}

        # Sort logic
        if sort_by == 'date':
            sort_criteria = [{"date_publication": {"order": "desc"}}]
        elif sort_by == 'title':
            sort_criteria = [{"job_title": {"order": "asc"}}]

        # Fetch offers from Elasticsearch using the constructed query
        response = db.search(index="offres_emploi",
                             body={"from": start, "size": per_page, "query": final_query, "sort": sort_criteria})
        total_offers_response = db.count(index="offres_emploi", body={"query": final_query})
        total_offers = total_offers_response['count']
        responseforFilters = db.search(index="offres_emploi", body={"query": {"match_all": {}}}, size=100)

        companies = set()
        locations = set()
        employment_types = set()
        for hit in responseforFilters['hits']['hits']:
            source = hit['_source']
            location = source.get('location')
            company = source.get('company_name')
            employment_type = source.get('employment_type')
            if location:
                locations.add(location)
            if company:
                companies.add(company)
            if employment_type:
                employment_types.add(employment_type)

        list_companies = list(companies)
        list_locations = list(locations)
        list_employment_types = list(employment_types)

        offres = [hit['_source'] for hit in response['hits']['hits']]
        total_offers_response = db.count(index="offres_emploi", body={"query": final_query})
        total_offers = total_offers_response['count']
        total_pages = (total_offers + per_page - 1) // per_page

    except exceptions.ElasticsearchException as e:
        list_companies = []
        list_locations = []
        list_employment_types = []
        offres = []
        total_pages = 0
        page = 1
    return render_template('offer_client_side.html', total_pages=total_pages, page=page, offres=offres,
                           list_locations=list_locations, list_companies=list_companies,
                           list_employment_types=list_employment_types, location_filter=location_filter,
                           company_filter=company_filter, employment_type_filter=employment_type_filter,
                           date_filter=date_filter, offerNumber=total_offers, sort_by=sort_by, lang=lang)
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
            return jsonify({"message": f"Index {index_name} created successfully."}), 200
        else:
            return jsonify({"message": f"Index {index_name} already exists."}), 200
    except exceptions.RequestError as e:
        return jsonify({"error": f"Error creating index {index_name}: {e.info}"}), 500


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
                "email": {"type": "text"},
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
    index_name = "offres_emploi"
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


@app.route('/apply-for-job', methods=['POST'])
def apply_for_job():
    # Extracting data from the form
    t = True
    offer_id = request.form.get('offer_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    file = request.files['resume']
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
        t = False
    if file and allowed_file(file.filename.lower()):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        with open(filepath, "rb") as f:
            file_base64 = base64.b64encode(f.read()).decode('utf-8')
    else:
        return jsonify({"error": "Invalid file format. Please upload a PDF or DOC/DOCX file"}), 400
        t = False
    # Constructing document to be indexed
    document = {
        "offer_id": offer_id,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "file": file_base64
    }
    if (t == True):
        # Indexing the document
        try:
            db.index(index="postuler", document=document)
            return Response('1', status=200)
        except exceptions.ElasticsearchException as e:
            return Response('0', status=500)


if __name__ == '__main__':
    app.run(debug=True)
