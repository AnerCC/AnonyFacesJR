from flask import Flask, request, jsonify
from moduls.blur import blureFace_dir,blureFace_file
import time
import cv2 as cv
import numpy as np
from logger import logger as LOGGER



app = Flask(__name__)


@app.route('/blur-file', methods=['POST'])
def blur_file_bytes():
  st=time.time()
  try:
    # LOGGER = create_logger("blur_log")
    LOGGER.info(f"blur-file request received")
    # Access request data
    t=time.time()
    image = request.files["image"]
    byte_image=image.read()
    fd_threshold=float(request.form.get("fd_threshold"))
    LOGGER.info(f'finished reading data in {time.time()-t}')
    t=time.time()
    np_images=cv.imdecode(np.frombuffer(byte_image, np.uint8), cv.IMREAD_COLOR)
    LOGGER.info(f'finished encoding image in - {time.time()-t}')
    t=time.time()
    detections= blureFace_file(np_images,fd_threshold,LOGGER)  # Pass fd_threshold and logger
    LOGGER.info(f'finished detection in {time.time()-t}')
    if detections is not None:
      LOGGER.info(f'request handled in {time.time()-st}')
      return jsonify(detections), 200  # Return JSON with processed images
      
    else:
      LOGGER.info('no faces detected')
      LOGGER.info(f'request handled in {time.time()-st}')
      return '', 204  # No data to process
   
   
  except KeyError as e:
      LOGGER.error(f"Missing required form data: {e}")
      return jsonify({'error': 'Missing required form data'}), 400
  except ValueError as e:
      LOGGER.error(f"Invalid fd_threshold value: {e}")
      return jsonify({'error': 'Invalid fd_threshold value'}), 400
  except cv.error as e:
      LOGGER.error(f"Error decoding image: {e}")
      return jsonify({'error': 'Error decoding image'}), 400
  except Exception as e:
      LOGGER.error(f"Unexpected error: {e}")
      return jsonify({'error': 'Internal server error'}), 500


#To be used when integrating with S3

# @app.route('/blur-dir', methods=['POST'])
# def blur():
#     # LOGGER = create_logger("blur_log")
#     LOGGER.info(f"blur-dir-path request recived")
#     if request.is_json:
#         fd_threshold=request.data["df_threshold"]
#         data = request.get_json()
#         LOGGER.info(f'Received data: {data}')
#         car_directory = data.get('car directory')
#         LOGGER.info(f"{car_directory} is  being sent or blurring")
#         blurred_images = blureFace_dir(car_directory,fd_threshold,LOGGER)
#         LOGGER.info(f"{car_directory} has done blurring proccess")
#         #blur_status options - blurred, no_detections, 
#         return blurred_images.tolist(),200



@app.route('/blur-test-local')
def blur_test_local():
    st=time.time()
    try:
        # LOGGER = create_logger("blur_log")
        LOGGER.info(f"blur-file request received")
        # Access request data
        t=time.time()
        images=[f'app/images_to_blur/1.jpg',f'app/images_to_blur/1.jpg']
        for img in images:
            with open(img, 'rb') as image_file:
                LOGGER.info(f'opned image :{img}')
                bytes_image=image_file.read()
                fd_threshold=0.4
                np_image=cv.imdecode(np.frombuffer(bytes_image, np.uint8), cv.IMREAD_COLOR)
                LOGGER.info(f'finished encoding image in - {time.time()-t}')
                t=time.time()
                detections= blureFace_file(np_image,fd_threshold,LOGGER)  # Pass fd_threshold and logger
                LOGGER.info(f'finished detection in {time.time()-t}')
                if detections is not None:
                    LOGGER.info(f'request handled in {time.time()-st}')
                    LOGGER.info(f'detections found:{detections}')
                    return jsonify(f'detections found, first detection is:{detections["face_1"]}'), 200  # Return JSON with processed images
                
                else:
                    LOGGER.info('no faces detected')
                    LOGGER.info(f'request handled in {time.time()-st}')
                    return '', 204  # No data to process
    
    
    except KeyError as e:
        LOGGER.error(f"Missing required form data: {e}")
        return jsonify({'error': 'Missing required form data'}), 400
    except ValueError as e:
        LOGGER.error(f"Invalid fd_threshold value: {e}")
        return jsonify({'error': 'Invalid fd_threshold value'}), 400
    except cv.error as e:
        LOGGER.error(f"Error decoding image: {e}")
        return jsonify({'error': 'Error decoding image'}), 400
    except Exception as e:
        LOGGER.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500




@app.route('/isAlive',methods=['GET','POST'])
def is_alive():
    if request.method=="GET":
        return 'server is alive, "GET" request recived'
    if request.method=="POST":
        return 'server is alive, "POST" request recived'
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)