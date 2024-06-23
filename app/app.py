from flask import Flask, request, jsonify
from app.moduls import blureFace_dir,blureFace_file,blureFace_bytes_file
import time
import cv2 as cv
import numpy as np
from app.logger import create_logger



app = Flask(__name__)


@app.route('/blur-file', methods=['POST'])
def blur_file_bytes():
  st=time.time()
  try:
    LOGGER = create_logger("blur_log")
    LOGGER.info(f"blur-file request received")
    print(f"blur-file request received")

    # Access request data
    t=time.time()
    image = request.files["image"]
    byte_image=image.read()
    fd_threshold=float(request.form.get("fd_threshold"))
    print(f'finished reading data in {time.time()-t}')
    t=time.time()
    np_images=cv.imdecode(np.frombuffer(byte_image, np.uint8), cv.IMREAD_COLOR)
    print(f'finished encoding image in - {time.time()-t}')
    t=time.time()
    detections= blureFace_bytes_file(np_images,fd_threshold,LOGGER)  # Pass fd_threshold and logger
    print(f'finished detection in {time.time()-t}')
    if detections is not None:
      print(f'request handled in {time.time()-st}')
      return jsonify(detections), 200  # Return JSON with processed images
      
    else:
      print('no faces detected')
      print(f'request handled in {time.time()-st}')
      return '', 204  # No data to process
   
   
  except Exception as e:
    LOGGER.error(f"Error processing images: {e}")
    print(f"Error processing images: {e}")
    return jsonify({'error': str(e)}), 500



@app.route('/blur-dir', methods=['POST'])
def blur():
    LOGGER = create_logger("blur_log")
    LOGGER.info(f"blur-dir-path request recived")
    if request.is_json:
        fd_threshold=request.data["df_threshold"]
        data = request.get_json()
        print(f'Received data: {data}')
        car_directory = data.get('car directory')
        LOGGER.info(f"{car_directory} is  being sent or blurring")
        blurred_images = blureFace_dir(car_directory,fd_threshold,LOGGER)
        LOGGER.info(f"{car_directory} has done blurring proccess")
        #blur_status options - blurred, no_detections, 
        return blurred_images.tolist(),200



@app.route('/blur-test-local')
def blur_test_local():
        LOGGER = create_logger("blur_log")
        images=[]
        LOGGER.info(f"blurring test request recived")
        print(f'blur request recived')
        car_directory = "images_to_blur"
        images=[f'{car_directory}/1.jpg',f'{car_directory}/2.jpg']
        for img in images:
             images.append(cv.imread(f'{car_directory}/{img}'))
        LOGGER.info(f"proccess started")
        blurred_images = blureFace_file(images,0.4,LOGGER)
        LOGGER.info(f"proccess ended")
        print(f'detected faces in {len(blurred_images)} images' )
        LOGGER.info(f'blur proccess ended blurred {len(blurred_images)} images')
        return  f'blur proccess ended blurred {len(blurred_images)} images'



@app.route('/isAlive',methods=['GET','POST'])
def is_alive():
    if request.method=="GET":
        return 'server is alive, "GET" request recived'
    if request.method=="POST":
        return 'server is alive, "POST" request recived'
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)