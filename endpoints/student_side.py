from flask import request, make_response
from apihelpers import check_endpoint_info, check_data_sent, token_validation, token_validation_student
import json
from dbhelpers import run_statement
import secrets
from uuid import uuid4

def patch():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation_student(request.headers.get('token'))
    if (valid_token == "valid"):

        # in case the response from the function is "valid" will keep going with the processes of adding an appointment by calling a fuction that will verify if the user sent the correct key values

        is_valid = check_endpoint_info(request.json, ['student_id'])
        if (is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)

        student_info = run_statement('CALL get_student_by_id(?)', [
                                  request.json.get('student_id')])
        # verifying if the response is different than a list and its length is different than 1 to send a 400 as response
        if (type(student_info) != list or len(student_info) != 1):
            return make_response(json.dumps(student_info, default=str), 400)

        # s = student info to be updated
        s = check_data_sent(request.json, student_info[0], [
                                           'student_id', 'first_name', 'last_name', 'email', 'password', 'salt', 'cell_number', 'birth_date', 'marital_status', 'have_passport', 'contract_signed', 'contract_date', 'english_level', 'app_form', 'intake', 'program_id', 'consultant_id'])

        token = secrets.token_hex(nbytes=None)
        salt = uuid4().hex

        # adding a new student
        results = run_statement('CALL add_student_personal_info(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', [s['student_id'], s['first_name'], 
        s['last_name'], s['email'], s['password'], salt, s['cell_number'], s['birth_date'], s['marital_status'], 
        s['have_passport'], s['contract_signed'], s['contract_date'], s['english_level'], s['app_form'], s['intake'],
        s['program_id'], s['consultant_id'], token])

        # if results is a list and at 0 at 'student_id" is different than zero, send back a 200 response. If it is equal to zero, send back the response showing that none row was updated and else, send back that an internal error has occurred
        if (type(results) == list and results[0]['student_id'] != 0):
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


def get():
    # verifying if some value was sent as header
    is_valid_header = check_endpoint_info(request.headers, ['token'])
    if (is_valid_header != None):
        return make_response(json.dumps(is_valid_header, default=str), 400)

    # calling the function that will verify if this token is valid
    valid_token = token_validation_student(request.headers.get('token'))
    if (valid_token == "valid"):

        is_valid = check_endpoint_info(request.args, ['email'])
        if(is_valid != None):
            return make_response(json.dumps(is_valid, default=str), 400)
        
        results = run_statement('CALL validate_student_token(?,?)', [request.args.get('email'), request.headers.get('token')])

        # if results is a list and his length is different than zero return 200
        if (type(results) == list and len(results) != 0):
            return make_response(json.dumps(results[0], default=str), 200)
        # else return 500, internal error
        elif (type(results) == list and len(results) == 0):
            return make_response(json.dumps("Wrong token or wrong email", default=str), 400)
        else:
            return make_response(json.dumps("Sorry, an error has occurred.", default=str), 500)

    elif (valid_token == "invalid"):
        return make_response(json.dumps("TOKEN EXPIRED", default=str), 403)
    # if the response from the validation function is 0 means that the token is invalid
    elif (len(valid_token) == 0):
        return make_response(json.dumps("WRONG TOKEN", default=str), 400)
    else:
        return make_response(json.dumps(valid_token, default=str), 500)