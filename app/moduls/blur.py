from retinaface import RetinaFace
import cv2 
import numpy as np
import os
import time


# https://sefiks.com/2021/04/27/deep-face-detection-with-retinaface-in-python/


COMPRESSION_LEVEL=99
QUALITY=99

def blureFace_file(img,fd_threshold,LOGGER):
              
        t=time.time()        
        LOGGER.info(f'face detection started ')
        resp = RetinaFace.detect_faces(img,threshold=fd_threshold)
        LOGGER.info(f'detection ended in {time.time()-t}')
        t=time.time()
        serializable_result = {}
        for face_key, face_data in resp.items():
            serializable_result[face_key] = {
                'score': numpy_encoder(face_data['score']),
                'facial_area': [numpy_encoder(coord) for coord in face_data['facial_area']],
                'landmarks': {
                    landmark_key: [numpy_encoder(coord) for coord in coords]
                    for landmark_key, coords in face_data['landmarks'].items()
                }
            }
        LOGGER.info(f'finished serializing response in {time.time()-t}')
        LOGGER.info(f'face detection ended ')
    
        
        if serializable_result!={}:
            return serializable_result
        else:
            return None
        

def blureFace_dir(car_diretory,fd_threshold,LOGGER):

    faces=[]
    flvl=os.listdir(f'{car_diretory}')
    for dir in flvl:
        
        dir_path = os.path.join(car_diretory, f'{dir}/1')
        images=os.listdir(dir_path)
        i=1
        for img in images:
            blurred_images=[]
            img_path=os.path.join(dir_path,img)
            
            if os.path.isfile(f'{img_path}'):

                    image=cv2.imread(img_path)
                    LOGGER.info('face detection started')
                    resp = RetinaFace.detect_faces(image,threshold=fd_threshold)
                    LOGGER.info('face detection ended')
                    i+=1
                    for identity in resp:
                        LOGGER.info('image blurring started')
                        try:
                            facial_area = resp[identity]['facial_area']   
                            blurred=cv2.GaussianBlur(image,(71,71),500)
                            faces.append(facial_area)

                        except KeyError:
                            LOGGER.info(f"KeyError: The key '{identity}' or 'facial_area' is missing in the response.")
                           

                        except cv2.error as e:
                            LOGGER.info(f"OpenCV error occurred: {e}")
                            
                        except FileNotFoundError as e:
                            LOGGER.info(f"File not found error: {e}")
                            
                        except Exception as e:
                            LOGGER.info(f"An unexpected error occurred: {e}")
                            
                              
                        try:
                            # Get detected face area from retinaFace response and assign face region to face veriable
                            x1, y1, x2, y2 = facial_area
                        
                            face = image[y1:y2, x1:x2]

                            #blur the face region
                            
                            # Create circular mask of the same size as the blurred image
                            mask = np.zeros_like(blurred)
                            h, w = face.shape[:2]
                            center = ((x1+w//2), (y1+h//2))
                            
                            cv2.ellipse(mask,center,(w//2,h//2),0,0,360, (255, 255, 255), -1)
                            
                            #create a circular blurred section
                            blurred_circular = cv2.bitwise_and(blurred, mask)
                            
                            
                            #apply the blurred circular section into the detected face area
                            blurredFace=np.where(mask!=0,blurred_circular,image)

                            #apply the blured face into the sorce image
                            image[y1:y2, x1:x2]=blurredFace[y1:y2, x1:x2]
                            
                            # if not os.path.exists(f'{BLURRED_DIR}/{dir}'):
                            #     os.mkdir(f'{BLURRED_DIR}/{dir}')
                            # cv2.imwrite(f'{BLURRED_DIR}/{dir}/{img}', image)
                            blurred_images.append(image)
                            LOGGER.info('image blurring ended')
                       
                        except cv2.error as e:
                            LOGGER.error(f"OpenCV error occurred: {e}")
                            # Handle specific OpenCV errors

                        except IndexError as e:
                            LOGGER.error(f"IndexError: {e}")
                            # Handle IndexError if facial_area doesn't have expected values

                        except Exception as e:
                            LOGGER.error(f"An unexpected error occurred: {e}")
                            # Handle any other unexpected errors
                        
    if blurred_images !=[]:
            return blurred_images
    else:
            return None







            

def numpy_encoder(obj):
    if isinstance(obj, np.integer):
        return int(obj)
    elif isinstance(obj, np.floating):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")
#   return image_base64
# if __name__=='__main__':
  
#    blureFace_file()
   