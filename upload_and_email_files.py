from methods.drive_functions import *
from methods.client_interactions import *
from utils.settings import *

source_folder = 'upload'
for source_file in os.listdir(source_folder):
    additional_points = None
    client, source_name = source_file.split(" - ")
    source_name, source_type = source_name.split(".") 
    client_name = CLIENTS[client]['name']
    client_email = CLIENTS[client]['email']
    dest_folder = CLIENTS[client]['drive_folder_id']
    drive_service = Drive_Service(dest_folder=dest_folder)
    file_id = drive_service.upload_audio_file(os.path.join(source_folder, source_file), source_name, folder_id=CLIENTS[client]['drive_folder_id'])
    drive_service.set_permission(file_id)
    file_data = drive_service.get_file_metadata(file_id)
    file_url = file_data['webContentLink']
    file_name = file_data['name'].split(".")[0]
    mail_service = Gmail_Service()
    mail_service.send_email(recipients=client_email, subject=file_name, body=create_email_string(client_name, file_url, file_name, additional_points=additional_points))
    os.remove(os.path.join(os.getcwd(), source_folder, source_file))