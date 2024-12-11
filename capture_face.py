import cv2
import face_recognition
import os
import pickle

# Create directories for saving images if they don't exist
if not os.path.exists('dataset'):
    os.makedirs('dataset')

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Store student names and corresponding face encodings
known_face_encodings = []
known_face_names = []

print("Starting face capture...")

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

    # Find faces in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Ask for the name if it's a new person
        name = input("Enter student name: ")

        # Save face encoding and name for future recognition
        known_face_encodings.append(face_encoding)
        known_face_names.append(name)

    cv2.imshow('Video', frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Save known faces data to a file
with open('face_encodings.pickle', 'wb') as f:
    pickle.dump((known_face_encodings, known_face_names), f)

# Release resources
video_capture.release()
cv2.destroyAllWindows()
