# Deliverables

## Source Code

The project source is available on [GitHub](https://github.com/mimlowe/bodyport-ecg)

## Instructions

### Running the Application

The application is a Flask app that can be run using the following steps:
1. Navigate to the project root.
2. Create a virtual environment using `python -m venv <name>`.
3. Activate the virtual environment.
   1. On Windows: `<name>\Scripts\activate`
   2. On Linux/Mac: `source <name>/bin/activate`
4. Install the dependencies using `pip install -r requirements.txt`.
5. Run the app using `flask --app server run`.
6. Open a browser and navigate to [`http://127.0.0.1:5000/ecg`](http://127.0.0.1:5000/ecg)
7. Enter a username for the session and select a file to upload:
   1. The file should be a binary file containing 4095 samples of Signed Int 24 bit values (3 bytes each).
   2. Click the `Upload` button to initiate file upload. 
8. Upon successful upload, click `Compress` to compress the uploaded file.
9. The app will display the original file size, compressed file size, and compression ratio along with a download button.

## Design Considerations and Key Decisions

### App Structure

The main app is in `server.py`, which uses Flask's factory pattern to create the app instance.

The app contains one root endpoint `/` which contains a link to the `/ecg` features.

The app uses blueprints to separate feature functionality:
1. `/ecg` - Blueprint which handles the ECG file upload, compression, and download

---
#### ECG Controller (url-prefix: `/ecg`)
The ECG controller contains the following routes:
1. `/` [GET/POST] - handles the ECG file upload
2. `/compress/<filename>` [POST] - compresses the uploaded ECG file
3. `/download/<filename>` [GET]  - downloads the compressed ECG file
---

### User Sessions & File Upload Destinations

The application uses sessions to associate the user with their uploaded file. 
This allows the application to store the uploaded file in a directory specific to the user which minimizes the risk of file collisions.

On the frontend, the user enters a username along with the ECG file upload. 
The username is stored as a session variable, which can then be utilized by the `compress` and `download` endpoints to find the user's file.

ECG files are stored in the `/uploads` directory, which will contain a subdirectory for each user.
The application will check if these directories exist and create them if they don't.

Subdirectories are named using `session['username']` as provided by the user.

For example, a file uploaded by username `michael` exists at `/uploads/michael/uploaded_file.bin`.

---

#### Filename security
The filenames and usernames are sanitized to prevent directory traversal attacks.

This is accomplished with the `secure_filename` function from the `werkzeug.utils` module.

For example, a user uploads a file named `../../etc/passwd`, the file is saved as `uploads/<username>/etc_passwd`.

---

## Compression Algorithm Specifications

The compression functionality is located in the `/ecg/compression` directory.

The application uses an implementation of Huffman coding to compress the ECG data.

#### Validating the Compression Algorithm

The results of the compression algorithm are validated by comparing the original and decompressed files.
These files should be identical if the compression algorithm is lossless.

There is a test script located in the `/tests/compression.test.py` which does the following:
1. Decompresses `/tests/compressed.bin` as `decompressed.bin`
2. Compares the original file `/tests/sample_ecg_raw.bin` with the `decopressed.bin`
3. Prints the result of the comparison

