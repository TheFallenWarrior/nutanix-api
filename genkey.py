
from base64 import b64encode

if __name__ == "__main__":
	username = input("Username: ")
	password = input("Password: ")

	encoded_credentials = b64encode(bytes(f'{username}:{password}',encoding='ascii')).decode('ascii')

	# The following file stores the base64-encoded username and password for API authentication.
	with open("api_basic_auth_token.txt", 'w') as f:
		f.write(encoded_credentials)
