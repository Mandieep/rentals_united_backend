
class Responsehandler():
    def success_response(self, response, status):
        response_dict = {}
        response_dict['response_data'] = response
        response_dict['status'] = status

        return response_dict

    def msg_response(self, msg, status):
        response_dict = {}
        response_dict['message'] = msg
        response_dict['status'] = status

        return response_dict

    def response_with_msg(self, response, msg, status):
        response_dict = {}
        response_dict['response_data'] = response
        response_dict['message'] = msg
        response_dict['status'] = status

        return response_dict

    def msg_with_token(self, msg, token, status):
        response_dict = {}
        response_dict['message'] = msg
        response_dict['access_token'] = token
        response_dict['status'] = status

        return response_dict
