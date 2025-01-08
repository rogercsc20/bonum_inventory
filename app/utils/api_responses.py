

def create_response(message=None, data=None, status_code=200):
    response = {"message" : message}
    if data is not None:
        response["data"] = data
    return response, status_code