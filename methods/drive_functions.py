from utils.google_service import Create_Service, MediaFileUpload, errors
from utils.settings import *

class Drive_Service:
    def __init__(self, client_secret='secrets/keys.json', service='drive', version='v3', scopes='https://www.googleapis.com/auth/drive', dest_folder=BOUNCES_FOLDER, source_folder='upload'):
        if isinstance(scopes, str): scopes = [scopes]
        self.drive = Create_Service(client_secret, service, version, scopes)
        self.dest_folder = dest_folder
        self.source_folder = source_folder

    def upload_audio_file(self, file_path, upload_name, folder_id=None):
        file_extension = file_path.split('.')[1]
        file_metadata = {
            'name': upload_name,
            'mimeType': f'audio/{file_extension}'
        }
        if folder_id: file_metadata.update({'parents': [folder_id]})
        media = MediaFileUpload(file_path,
                                resumable=True)
        file = self.drive.files().create(body=file_metadata,
                                            media_body=media).execute()
        return file.get('id')

    def set_permission(self, file_id, perm_type='anyone', value='anyone', role='reader'):
        print(file_id)
        try:
            permission = {'type': perm_type,
                        'value': value,
                        'role': role}
            return self.drive.permissions().create(fileId=file_id,body=permission).execute()
        except errors.HttpError as error:
            return print('Error while setting permission:', error)

    def get_file_metadata(self, file_id):
        try: return self.drive.files().get(fileId=file_id, fields="*").execute()
        except errors.HttpError as error: return(f"Error {error} occurred.")