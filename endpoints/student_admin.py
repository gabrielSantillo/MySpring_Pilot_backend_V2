from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation, send_email
import json
from dbhelpers import run_statement
import secrets

# this is the POST function that is responsible to post new student


def post():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):

        # in case the response from the function is "valid" will keep going with the processes of adding an appointment by calling a fuction that will verify if the user sent the correct key values
        is_valid = check_endpoint_info(request.json, ['email'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        student_token = secrets.token_hex(nbytes=None)
        # adding a new student
        results = run_statement('CALL add_student_info(?,?,?)', [request.json.get('email'), request.headers.get('token'), student_token])

        # if results is a list and at 0 at 'student_id" is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if (type(results) == list and results[0]['student_id'] != 0):
            send_email(request.json.get('email'), student_token)
            return make_response(json.dumps(results[0], default=str), 200)
        elif (type(results) == list and results[0]['student_id'] == 0):
            return make_response(json.dumps("Wrong token", default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)

# this is the GET function that is responsible to get all students


def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        
        if(request.args.get('student_id') != None):
            # in case the response from the function is "valid" will keep going with the processes of getting appointments
            results = run_statement('CALL get_student_by_id(?)', [request.args.get('student_id')])

            # if results is a list and his length is different than zero return 200
            if (type(results) == list and len(results) != 0):
                return make_response(json.dumps(results, default=str), 200)
            # else return 500, internal error
            elif (type(results) == list and len(results) == 0):
                return make_response(json.dumps("Wrong token", default=str), 400)
            elif(results.startswith('Incorrect integer value:')):
                return make_response(json.dumps(results, default=str), 400)
            else:
                return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
        elif(request.args.get('student_id') == None):
            # in case the response from the function is "valid" will keep going with the processes of getting students
            results = run_statement('CALL get_all_students()')

            # if results is a list and his length is different than zero return 200
            if (type(results) == list and len(results) != 0):
                return make_response(json.dumps(results, default=str), 200)
            # else return 500, internal error
            elif (type(results) == list and len(results) == 0):
                return make_response(json.dumps("Wrong token", default=str), 400)
            else:
                return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)
        else:
            make_response(json.dumps("Only integer numbers are accepted.", default=str), 400)
    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)


# this is the PATCH function that is responsible to update a student based on its id


def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation(request.headers.get('token'))
    if (valid_token == "valid"):
        # in case the response from the function is "valid" will keep going with the processes of patching student
        is_valid = check_endpoint_info(request.json, ['student_id'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        # getting the student by id
        student_info = run_statement('CALL get_student_by_id(?)', [request.json.get('student_id')])

        # checking to see if the response is valid to continue with the patching process
        if (type(student_info) == list and len(student_info) != 0):
            update_student_info = check_data_sent(request.json, student_info[0],
            ['student_id', 'first_name', 'last_name', 'email', 'cell_number', 'birth_date', 'marital_status', 'have_passport', 'contract_signed', 'contract_date', 'english_level', 'app_form', 'intake', 'program_id', 'consultant_id',])

            # calling the function that will edit a student
            results = run_statement('CALL edit_student(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', 
            [update_student_info['student_id'], update_student_info['first_name'],
            update_student_info['last_name'], update_student_info['email'],
             update_student_info['cell_number'], update_student_info['birth_date'], update_student_info['marital_status'], update_student_info['have_passport'],update_student_info['contract_signed'], update_student_info['contract_date'], update_student_info['english_level'], update_student_info['app_form'], update_student_info['intake'], update_student_info['program_id'], update_student_info['consultant_id']])

            # if the response is a list and the row_updated is equal than 1 send 200 as response
            if (type(results) == list and results[0]['row_updated'] != 0):
                return make_response(json.dumps(results[0], default=str), 200)
            # if the response is a list and the row_updated is equal than 0 send 400 as response
            elif (type(results) == list and results[0]['row_updated'] == 0):
                return make_response(json.dumps(results[0], default=str), 400)
            # else send 500 as an internal error
            else:
                return make_response(json.dumps("Sorry, an error has occurred", default=str), 500)
        else:
            return make_response(json.dumps("Wrong token or wrong student_id", default=str), 400)

    # if the response from the validation function is "invalid" means that the token expired
    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)
