from flask import Flask, request, jsonify, render_template, url_for, make_response
from model_prediction import swap_gender
import re
import imghdr
from waitress import serve


app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


@app.route('/predict', methods=['POST'])
def predict():
    img = request.files['img']
    if imghdr.what(img) not in ALLOWED_EXTENSIONS:
        return make_response(
            jsonify({"error_message": "Allowed extensions of file for upload - png, jpg, jpeg."}), 400)

    img_bytes = img.read()
    results = swap_gender(img_bytes)
    res_images = [m.group(0) for m in (re.search(r'\S{0}\w+.\w+$', r) for r in results)]
    res_images = '+'.join(res_images)
    predict_url = url_for('show_result', res_images=res_images)
    return make_response(jsonify({'result of swap': predict_url}), 200)


@app.route('/result/<res_images>')
def show_result(res_images):
    res_im_split = res_images.split('+')
    img_male, img_female = res_im_split[0], res_im_split[1]
    return render_template('show_results.html', img_male=img_male, img_female=img_female)


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    serve(app, host='0.0.0.0', port=5000)
