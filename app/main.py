import os
import zipfile
from zipfile import ZipFile
import csv
from datetime import datetime
from pathlib import Path
from flask import Blueprint, request, url_for, jsonify, redirect, flash
from flask import render_template, redirect
from flask_login import login_required
from .img_gen import CardGenerator

main = Blueprint('main', __name__)
current_dir = os.path.dirname(__file__)
upload_path = os.path.join(current_dir, 'cards_images', 'person-image')
upload_csv_path = os.path.join(current_dir, 'cards_images', 'person-csv')
path_store_image = os.path.join(current_dir, 'static', 'images')

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return 'Profile'

@main.route('/card-duplicate')
@login_required
def card_duplicate():
    return render_template('card-duplicate.html')

@main.route('/card-request')
@login_required
def card_request():
    return render_template('card-duplicate.html')

@main.route('/one-card-generation')
@login_required
def one_card():
    return render_template('one-card.html')

@main.route('/report')
@login_required
def report():
    return render_template('card-duplicate.html')


@main.route('/create-image', methods=['POST'])
@login_required
def create_image():
    json_response = {"status": None, "img": None}
    if request.get_json():
        new_image = CardGenerator()
        data = request.get_json()
        if data['id'] != "":
            new_image.set_id(data['id'])
            new_image.set_person_image(data['id']+'.jpg')
        if data['first-name'] != "":
            new_image.set_first_name(data['first-name'])
        if data['last-name'] != "":
            new_image.set_last_name(data['last-name'])
        if data['study-field'] != "":
            new_image.set_study_field(data['study-field'])
        path_to_image = new_image.create_image()

        json_response["status"] = "success"
        json_response["img"] = url_for("static", filename="images/" + path_to_image + ".jpg")
        return jsonify(json_response)
    '''
    json_response = {"status": None, "img": None}
    if request.get_json():
        json_response["status"] = "success"
        json_response["img"] = '<img src=' + url_for("static", filename="images/ja.jpeg") + '>'
        return jsonify(json_response)
    json_response["status"] = "error"
    return "{'status': 'success', 'img': {}}".format("<img src=/static/images/ja.jpeg>")
    '''

@main.route('/upload-csv', methods=['POST'])
@login_required
def handleCsvFileUpload():
    if 'persons' not in request.files:
        flash('No persons file')
    if 'persons' in request.files:
        person_csv = request.files['persons']
        if person_csv.filename != '' and '.' in person_csv.filename:
            if person_csv.filename.split('.')[1] in ['txt']:
                person_csv.save(os.path.join(upload_csv_path, person_csv.filename))
                file = os.path.join(upload_csv_path, person_csv.filename)
                if validationCsvFile(file):
                    flash('Csv file is correnct')
                    photos_name = createImageFromCsv(file)

                    #Create zip file from photos
                    new_dir = 'photos' + str(datetime.timestamp(datetime.now())).replace('.', '') + '.zip'
                    new_dir = os.path.join(path_store_image, new_dir)
                    with ZipFile(new_dir, 'w') as zip:
                        for file in photos_name:
                            file = file + '.jpg'
                            zip.write(os.path.join(path_store_image, file), os.path.basename(file))
                else:
                    flash('Csv file is incorect')
            else:
                flash('File is not txt extension')
        else:
            flash('File is without extension')
    return redirect(url_for('main.manyCards'))

@main.route('/check-photo/<id>', methods=['GET'])
@login_required
def checkPhotoExist(id):
    files = [file for file in Path(upload_path).glob('*.jpg') if
             os.path.basename(file.with_suffix('')) == id]
    json_response = {"status": "success", "message": ""}
    if files:
        json_response['message'] = 'OK'
    else:
        json_response['message'] = 'ERROR'
    return jsonify(json_response)


@main.route('/upload-foto', methods=['POST'])
@login_required
def handleFileUpload():
    if 'photo' not in request.files:
        flash('No photo file')
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo.filename != '' and '.' in photo.filename:
            if photo.filename.split('.')[1] == 'zip':
                photo.save(os.path.join(upload_path, photo.filename))
                zip_file = os.path.join(upload_path, photo.filename)
                count = extractZipFile(zip_file, upload_path)
                flash('Upload {0} files from zip file'.format(str(count)))
            elif photo.filename.split('.')[1] == 'jpg':
                photo.save(os.path.join(upload_path, photo.filename))
                flash('File {0} was uploaded'.format(photo.filename))
            else:
                flash('File {0} was not uploaded'.format(photo.filename))
        else:
            flash('Not found extension in upload file')
    return render_template('image-admin.html')

@main.route('/image-admin', methods=['GET','POST'])
@login_required
def image_admin():
    if request.method == 'GET':
        return render_template('image-admin.html')

@main.route('/create-image-csv', methods=['GET'])
@login_required
def manyCards():
    return render_template('many-cards.html')

def extractZipFile(file, upload_path):
    count = 0
    if os.path.isfile(file):
        with zipfile.ZipFile(file, "r") as zip_ref:
            photo_list = zip_ref.filelist
            for photo in photo_list:
                if photo.filename.split('.')[1] == 'jpg':
                    zip_ref.extract(photo.filename, upload_path)
                    count = count + 1
    return count

def validationCsvFile(file):
    error = False
    message = []
    if os.path.isfile(file):
        with open(file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                print('error', row)
                if len(row) != 4:
                    message.append('Line {} : invalid number fields'.format(id))
                    error = True
    return not error

def createImageFromCsv(file):
    list_img = []
    if os.path.isfile(file):
        with open(file) as csv_file:
            new_image = CardGenerator()
            csv_reader = csv.reader(csv_file, delimiter=';')
            for row in csv_reader:
                l = new_image.set_id(row[0]).set_first_name(row[1]).set_last_name(row[2]).set_study_field(row[3]).create_image()
                list_img.append(l)
    return list_img


