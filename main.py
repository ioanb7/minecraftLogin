


"""
http://wiki.vg/Mojang_API#Username_-.3E_UUID_at_time
https://api.mojang.com/users/profiles/minecraft/Stunt3r?at=1476637224
"""

def minecraftLoginServiceLogin(username, password, clientToken):
	import requests
	import logging
	import json
	requestData = {
		"agent": {
			"name": "Minecraft",
			"version": 1
		},
		"username": username,
		"password": password,
		"clientToken": clientToken,
		"requestUser": True
	}
	r = requests.post('https://authserver.mojang.com/authenticate', json=requestData)
	r.status_code


	"""
	http://wiki.vg/Authentication:
	Method Not Allowed		The method specified in the request is not allowed for the resource identified by the request URI	Something other than a POST request was received.
	Not Found		The server has not found anything matching the request URI	Non-existing endpoint was called.
	ForbiddenOperationException	UserMigratedException	Invalid credentials. Account migrated, use e-mail as username.	
	ForbiddenOperationException		Invalid credentials. Invalid username or password.	
	ForbiddenOperationException		Invalid credentials.	Too many login attempts with this username recently (see /authenticate). Note that username and password may still be valid!
	ForbiddenOperationException		Invalid token.	accessToken was invalid.
	IllegalArgumentException		Access token already has a profile assigned.	Selecting profiles isn't implemented yet.
	IllegalArgumentException		credentials is null	Username/password was not submitted.
	Unsupported Media Type		The server is refusing to service the request because the entity of the request is in a format not supported by the requested resource for the requested method	Data was not submitted as application/json

	"""

	response = r.json()

	error = 0
	errorMessage = ""

	responseUsername = ""
	responseAccessToken = ""

	LOG_INFO_FILENAME = 'logs/minecraftLoginService.info.log'
	LOG_ERROR_FILENAME = 'logs/minecraftLoginService.error.log'
	logging.basicConfig(filename=LOG_INFO_FILENAME,level=logging.INFO)
	logging.basicConfig(filename=LOG_ERROR_FILENAME,level=logging.ERROR)
	logger = logging.getLogger("MinecraftLoginService")



	logger.info("New login request for: " +username)
	successful = False

	if 'error' in response:
		if response['error'] == "Method Not Allowed" or response['error'] == "Not Found":
			error = 505
			errorMessage = "Error on the server."
		elif response['error'] == "ForbiddenOperationException":
			if response['errorMessage'].find("UserMigratedException") != -1:
				errorMessage = "Account migrated, use e-mail as username"
			elif response['errorMessage'].find("accessToken") != -1:
				error = 505
				errorMessage = "Error on the server."
			else:
				errorMessage = "Invalid credentials"
		elif response['error'] == "IllegalArgumentException":
			if response['errorMessage'].find("selecting profiles") != -1:
				error = 505
				errorMessage = "Error on the server."
			else:
				error = 0
				errorMessage = "Please write a valid username & password"
		elif response['error'] == "Unsupported Media Type":
			error = 505
			errorMessage = "Error on the server."
		else:
			error = 505
			errorMessage = "Unknown error"
		
		
		logger.error('Something went wrong!')
		logger.error('Response json: ' + json.dumps(response, separators=(',', ':')))
	else:
		"""
		{'clientToken': '222', 'selectedProfile': {'name': 'Stunt3r', 'id': 'dc16023b81ac4fde8690402853435266'}, 'availableProfiles': [{'name': 'Stunt3r', 'id': 'dc16023b81ac4fde8690402853435266'}], 'user': {'id': '8fa21a4845064ca8a629fa1cda99cc37'}, 'accessToken': '8208579ec840413b995bcb6ab433f28c'}
		"""
		responseUsername = response['availableProfiles'][0]['name']
		#print("Logged in as:" + responseUsername)
		successful = True
		responseAccessToken = response['accessToken']

	logger.info("Login response for " +username + ": successful: " + str( successful ))
	logger.debug("Request: " + json.dumps(requestData, separators=(',', ':')))
	logger.debug("Response: " + json.dumps(response, separators=(',', ':')))
	
	return {
		'success' : successful,
		'error': errorMessage,
		'script_error': error != 0,
		'username' : responseUsername,
		'accessToken' : responseAccessToken
		
	}
		
if __name__ == "__main__":
	username = "im.stunt3r@yahoo.com"
	password = "#";
	clientToken = 222;
	#clientToken = "8Q0c17IZE$kd42AL";


	response = minecraftLoginServiceLogin(username, password, clientToken)

	if response['success'] == True:
		#success
		print("success")
	else:
		#error
		print("failure")



