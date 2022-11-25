from flask import Flask
from dbcreds import production_mode
import endpoints.consultant, endpoints.consultant_login, endpoints.college, endpoints.student_admin, endpoints.application_status, endpoints.programs, endpoints.visa, endpoints.image, endpoints.student_side, endpoints.student_file_name
from flask_cors import CORS

# calling the Flask function which will return a value that will be used in my API
app = Flask(__name__)
CORS(app)

##############################################################################
# CONSULTANT #
##############################################################################

@app.post('/api/consultant')
def post_consultant():
    return endpoints.consultant.post()

@app.get('/api/consultant')
def get_consultant():
    return endpoints.consultant.get()

@app.patch('/api/consultant')
def patch_consultant():
    return endpoints.consultant.patch()

##############################################################################
# CONSULTANT-LOGIN #
##############################################################################

@app.post('/api/consultant-login')
def log_in_consultant():
    return endpoints.consultant_login.post()

@app.delete('/api/consultant-login')
def delete_consultant_token():
    return endpoints.consultant_login.delete()


##############################################################################
# COLLEGE #
##############################################################################

@app.post('/api/college')
def post_college():
    return endpoints.college.post()

@app.get('/api/college')
def get_all_colleges():
    return endpoints.college.get()

@app.patch('/api/college')
def patch_college():
    return endpoints.college.patch()

##############################################################################
# STUDENT ADMIN #
##############################################################################

@app.post('/api/student-admin')
def post_student():
    return endpoints.student_admin.post()

@app.get('/api/student-admin')
def get_all_students():
    return endpoints.student_admin.get()


@app.patch('/api/student-admin')
def patch_student():
    return endpoints.student_admin.patch()

##############################################################################
# STUDENT #
##############################################################################

@app.get('/api/student')
def validate_student_token():
    return endpoints.student_side.get()

@app.patch('/api/student')
def patch_student_personal_info():
    return endpoints.student_side.patch()


##############################################################################
# IMAGES #
##############################################################################

@app.post('/api/image')
def post_image():
    return endpoints.image.post()

@app.get('/api/image')
def get_image():
    return endpoints.image.get()

@app.get('/api/image-name')
def get_image_length():
    return endpoints.student_file_name.get()

@app.delete('/api/image')
def delete_image():
    return endpoints.image.delete()


##############################################################################
# APPLICATION_STATUS #
##############################################################################

@app.post('/api/application-status')
def post_application():
    return endpoints.application_status.post()

@app.get('/api/application-status')
def get_all_application_status():
    return endpoints.application_status.get()

@app.patch('/api/application-status')
def patch_application_status():
    return endpoints.application_status.patch()

##############################################################################
# PROGRAMS #
##############################################################################
 
@app.post('/api/program')
def post_program():
    return endpoints.programs.post()

@app.get('/api/program')
def get_all_programs():
    return endpoints.programs.get()

@app.patch('/api/program')
def patch_program():
    return endpoints.programs.patch()

##############################################################################
# VISA #
##############################################################################

@app.post('/api/visa')
def post_visa():
    return endpoints.visa.post()

@app.get('/api/visa')
def get_visa():
    return endpoints.visa.get()

@app.patch('/api/visa')
def patch_visa():
    return endpoints.visa.patch()


# if statement to check if the production_mode variable is true, if yes, run in production mode, if not, run in testing mode
if (production_mode):
    print("Running in Production Mode")
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5010)
else:
    from flask_cors import CORS
    CORS(app)
    print("Running in Testing Mode")
    app.run(debug=True)