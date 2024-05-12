from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
from app.schemas.chat import (ChatSchema, 
                                   CreateChatResponse, 
                                   CreateMessageResponse, 
                                   GetChatResponse, 
                                   GetMessagesResponse, 
                                   MessageSchema
                                   )
from app.services.chat_service import create_chat, create_message, get_all_chats, get_messages_by_chat_id
from app.utils.validators import custom_response, valiate_request_body, validate_api_key 
import logging
import os



# swagger initialization
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
swagger_dir = "/".join(str(basedir).split("/")[0:-1])+"/assets/swagger.json"


SWAGGER_URL = '/apidocs'  
API_URL =  "/static/swagger.json" # "https://petstore.swagger.io/v2/swagger.json" # 
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  
    API_URL,
    config={  
        'app_name': "Abdel Chat application"
    },
)

# api initialization
chat_router_pb = Blueprint("ChatRouter",__name__)
message_router_pb = Blueprint("MessageRouter",__name__)

chat_router_pb_api = Api(chat_router_pb)
message_router_pb_api =Api(message_router_pb)

# Register Swagger UI blueprint
chat_router_pb.register_blueprint(swaggerui_blueprint)
message_router_pb.register_blueprint(swaggerui_blueprint)


class ChatRouterGet(Resource):
    """ Main chat Router to handle Chat GET ops """
   
    @validate_api_key
    def get(self):
        """ return all chats """
        try:
            chats = get_all_chats()
            response_data = GetChatResponse(error=False, chats=chats).model_dump_json()
            return custom_response(response_data, 200)
        except Exception as e:
            logging.error(f"Get chats error: {e}")
            return custom_response({"error": "Internal Server Error"}, 500)
    

class ChatRouterPost(Resource):
    """ Main chat Router to handle Chat POST ops """  
    @validate_api_key
    @valiate_request_body(ChatSchema)
    def post(self):
        """ create new chat """
        try:
            data = ChatSchema(**request.json)
            new_chat = create_chat(data.name)
            if new_chat:
                response_data = CreateChatResponse(id=new_chat.id, name=new_chat.name).model_dump_json()
                return custom_response(response_data, 201)
            return custom_response({"error": "Failed to create new chat"}, 400)
        except Exception as e:
            logging.error(f"Create Chat error: {e}")
            return custom_response({"error": "Internal Server Error"}, 500)
    
        
class MessageRouterGet(Resource):
    """ Main Message Router to handle Message GET ops """
    
    @validate_api_key
    def get(self,chat_id:int):
        """ get messages of specific chat """
        try:
            messages = get_messages_by_chat_id(chat_id)
            response_data = GetMessagesResponse(error=False, messages=messages).model_dump_json()
            return custom_response(response_data, 200)
        except Exception as e:
            logging.error(f"Get messages error: {e}")
            return custom_response({"error": "Internal Server Error"}, 500)


class MessageRouterPost(Resource):
    """ Main Message Router to handle Message POST ops """
    @validate_api_key
    @valiate_request_body(MessageSchema)
    def post(self):
        """ add message to a specific chat """
        try:
            data = MessageSchema(**request.json)
            new_message = create_message(senderName=data.senderName,chat_id=data.chat_id,content=data.content)
            if not new_message:
                return custom_response({"error": "Failed to add Message to this chat, Please check your chat_id"}, 400) 
            logging.info(f"New Message created: \n {new_message}")
            response_data = CreateMessageResponse(error=False, description="Message created successfully").model_dump_json()
            return custom_response(response_data, 201)
        except Exception as e:
            logging.error(f"Get messages error: {e}")
            return custom_response({"error": "Internal Server Error"}, 500)
      

# routing

chat_router_pb_api.add_resource(ChatRouterGet, '/chat/all', methods=['GET'])
chat_router_pb_api.add_resource(ChatRouterPost, '/chat/add-chat', methods=['POST'])

message_router_pb_api.add_resource(MessageRouterGet, '/message/<int:chat_id>')
message_router_pb_api.add_resource(MessageRouterPost, '/message/add-message')

# Register Swagger documentation
# swagger.docs(chat_router_pb_api, apiVersion='0.1')
# swagger.docs(message_router_pb_api, apiVersion='0.1')

# AQ_Transcript_API.add_resource(QuestionAnswerBot, "/qa") # <int:chunk_id>QuestionAnswerBot
# AQ_Transcript_API.add_resource(Test, "/") # <int:chunk_id>QuestionAnswerBot