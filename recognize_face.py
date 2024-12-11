import cv2
import face_recognition
import pickle
from datetime import datetime
import sqlite3

# Load the known faces and names
with open('face_encodings.pickle', 'rb') as f:
    known_face_encodings, known_face_names = pickle.load(f)

# Initialize webcam
video_capture = cv2.VideoCapture(0)

# Initialize attendance database
conn = sqlite3.connect('attendance.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS attendance (name TEXT, date TEXT)''')
conn.commit()

print("Starting face recognition...")

while True:
    ret, frame = video_capture.read()
    rgb_frame = frame[:, :, ::-1]

    # Find faces in the frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # Check if this face matches any known face
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match is found, get the corresponding name
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

            # Mark attendance if the person is recognized
            date_today = datetime.now().strftime("%Y-%m-%d")
            c.execute("INSERT INTO attendance (name, date) VALUES (?, ?)", (name, date_today))
            conn.commit()

        # Draw a rectangle around the face and label it with the name
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    cv2.imshow('Video', frame)

    # Break on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources and close the database connection
video_capture.release()
cv2.destroyAllWindows()
conn.close()
