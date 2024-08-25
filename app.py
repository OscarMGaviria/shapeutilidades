from flask import Flask, request, jsonify, send_file, render_template
import geopandas as gpd
import os
import tempfile
import zipfile
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            # Create a temporary in-memory buffer for the ZIP file
            zip_buffer = io.BytesIO(file.read())
            with zipfile.ZipFile(zip_buffer, 'r') as zip_ref:
                temp_dir = tempfile.TemporaryDirectory()
                zip_ref.extractall(temp_dir.name)

                # Find the Shapefile components
                shp_file = [f for f in os.listdir(temp_dir.name) if f.endswith('.shp')]
                shx_file = [f for f in os.listdir(temp_dir.name) if f.endswith('.shx')]
                dbf_file = [f for f in os.listdir(temp_dir.name) if f.endswith('.dbf')]

                # Print the found files and their paths
                print("Shapefile components found:")
                for f in shp_file:
                    print(f"SHAPE: {os.path.join(temp_dir.name, f)}")
                for f in shx_file:
                    print(f"SHX: {os.path.join(temp_dir.name, f)}")
                for f in dbf_file:
                    print(f"DBF: {os.path.join(temp_dir.name, f)}")

                if not shp_file or not shx_file or not dbf_file:
                    return jsonify({'error': 'Missing required Shapefile components'}), 400

                shp_path = os.path.join(temp_dir.name, shp_file[0])
                geojson_buffer = io.BytesIO()

                # Convert Shapefile to GeoJSON
                gdf = gpd.read_file(shp_path)
                gdf.to_file(geojson_buffer, driver='GeoJSON')
                geojson_buffer.seek(0)  # Go to the beginning of the BytesIO buffer

                return send_file(
                    geojson_buffer,
                    as_attachment=True,
                    download_name='output.geojson',
                    mimetype='application/geo+json'
                )

        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
