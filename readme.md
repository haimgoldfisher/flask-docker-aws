# Flask-SQLite-App with AWS

## Description

This project is a Flask web application that allows users to enter their name and email, which are then stored in an SQLite database. Users can also view the stored names and emails by accessing a specific route.

## Installation Instructions

### Prerequisites

Ensure you have the following installed on your system:
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Install Requirements
- Install the required Python packages using pip (if running locally):
  ```sh
  pip install -r requirements.txt 
    ```

## Usage Instructions

### 1. Run Flask App
- Execute the Flask application:
- The application will start running on a local server. Access the provided IP address (e.g., http://127.0.0.1:8000/) in a web browser.

![name&email](snaps/name&email.png)

### 2. Add Name and Email
- Upon accessing the application, you will see a form where you can enter your name and email.
- Fill in the required fields and click the "Submit" button to add your information to the database.

![welcome](snaps/welcome.png)

### 3. View Names and Emails
- To view the stored names and emails, append `/db` to the application URL in the address bar of your browser (e.g., http://127.0.0.1:8000/db).
- This will display a table with the names and emails stored in the database.

![db](snaps/db.png)

### AWS Integration

This Flask application assumes that it is running on an EC2 instance within an AWS environment. The application utilizes an Amazon S3 bucket to store images, which are accessed by the Flask app to display content to users. However, the images stored in the S3 bucket are kept private, and access to them is restricted.

To ensure that the Flask application can access the images stored in the S3 bucket, the EC2 instance hosting the application is assigned an IAM role with appropriate permissions. In this case, the role should have the `AmazonS3ReadOnlyAccess` policy attached, allowing the instance to read objects from the specified S3 bucket.

When the Flask application runs on an EC2 instance with the necessary IAM role, it can successfully retrieve and display the images from the S3 bucket. However, if the instance does not have the required permissions or if the IAM role is not properly configured, the application will encounter errors when attempting to access the S3 bucket.

### Screenshots

1. **AWS Console with S3 Bucket:**
   ![AWS Console S3 Bucket](snaps/s3_bucket_pic_url.png)

2. **Updated Code with S3 Image URL:**
   ![Updated Code with S3 Image URL](snaps/show_img_s3.png)

3. **Deploy The App on EC2:**
   ![Deployment](snaps/ec2-running.png)

4. **Updated Code to Get S3 Img URL if Permitted:**
   ![Code](snaps/private_access_code.png)

5. **EC2 with S3 Reader IAM Role:**
   ![S3 Reader](snaps/s3_reader_ec2_access.png)
   ![IAM Role](snaps/ec2_has_access.png)

6. **Welcome HTML When EC2 Has no IAM Role:**
   ![HTML No Credentials](snaps/no_access.png)

   

## Project Architecture

This project follows a client-server architecture using Flask as the web framework, HTML for front-end rendering, and SQLite for database management. The project directory structure is as follows:
 
```
flask-docker-aws/
│
├── app/
│   ├── flask-app.py        # Flask app file
│   ├── templates/          # HTML templates dir
│   │   ├── db.html         # Template for displaying names and emails
│   │   ├── index.html      # Template for entering name and email
│   │   └── welcome.html    # Template for welcoming user
├── instance/
│   └── users.db            # SQLite db
├── .venv/                  # Virtual env. directory (if running locally)
├── requirements.txt        # File for dependencies
├── Dockerfile              # Dockerfile for containerizing the app
└── docker-compose.yml      # Docker Compose file for defining services
```

The Flask application (`flask-app.py`) handles routing and interactions with the database. HTML templates (`templates/`) are used for rendering front-end views. SQLite is used to store user information in the database.

## Author

[Haim Goldfisher](https://github.com/haimgoldfisher)

## License

This project is licensed under the [MIT License](LICENSE).
