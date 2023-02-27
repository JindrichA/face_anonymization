import cv2
from mtcnn import MTCNN
import os
import glob
from tqdm import tqdm
import io
from contextlib import redirect_stdout






folder_path = r'G:\My Drive\FTVS_PhyEx_2023\Mereni_24022023\Originalni_videa'
output_path = r'C:\Users\adolfjin\Videos\Anonymizovana'

mp4_files = glob.glob(os.path.join(folder_path, "*.mp4"))


for mp4_file in tqdm(mp4_files):
    cap = cv2.VideoCapture(mp4_file)

    # Get the frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # Get the codec of the video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Define the output video file

    name_of_the_file = mp4_file.split("\\")[-1]
    save_video_as = output_path+'\\'+name_of_the_file[:-4]+'_an.mp4'
    save_video_as = save_video_as.replace("\\", "/")
    out = cv2.VideoWriter(output_path+'/'+name_of_the_file[:-4]+'_an.mp4', fourcc, fps, (int(cap.get(3)), int(cap.get(4))))
    detector = MTCNN()

    # Loop through each frame of the video
    i = 0


    while True:
        # Read the frame
        ret, frame = cap.read()
        if not ret:
            break
        with redirect_stdout(io.StringIO()):
            faces = detector.detect_faces(frame, )
        # Blur the faces
        list_of_not_detected = []
        if len(faces) > 0:
            for face in faces:
                # Select the area of the face
                #face = frame[y:y+h, x:x+w]
                x, y, w, h = face['box']
                # Apply Gaussian blur to the face
                h = int(1.2*h)
                w = int(1.2*w)
                face_frame = frame[y:int(y + h), x:int(x +w)]
                blur = cv2.GaussianBlur(face_frame, (23, 23), 30)

                # Replace the face with the blurred face
                frame[y:y+h, x:x+w] = blur

            # Write the frame to the output video file
            out.write(frame)
            i = i+1
            if i % 50 ==0:
                print("Frame {} of {}".format(i, frame_count))
        else:
            try:
                list_of_not_detected.append(i)
                frame[y:y + h, x:x + w] = blur
            except:
                print("Does not exist for frame no. {}".format(i))

    # Release the video capture and writer objects
    cap.release()
    out.release()
    print("Not working are: ".format(str(list_of_not_detected)))

    # Destroy all windows
    cv2.destroyAllWindows()