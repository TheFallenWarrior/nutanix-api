from datetime import datetime
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

baseUrl = "https://172.17.200.70:9440/api/nutanix/v3"

listVmsUrl = baseUrl+"/vms/list"

# 'sort_attribute' parece não funcionar
listVmsPayload =  """{
	"kind": "vm",
	"length": 20,
	"sort_attribute": ".",
	"sort_order": "ASCENDING",
	"offset": 0
}"""

def getExportVmUrl(uuid: str):
	return f"{baseUrl}/vms/{uuid}/export"

def getExportVmPayload(vmName: str):
	now = datetime.now()
	today = now.strftime("%d-%m-%Y")
	return '{"name":'+vmName+today+',"disk_file_format":"vmdk"}'

def main():
	with open("api_basic_auth_token.txt", 'r') as f:
		token = f.read()
	
	headers = {
		"Accept": "application/json",
		"Authorization": f"Basic {token}",
		"Content-Type": "application/json"
	}

	response = requests.request("post", listVmsUrl, data=listVmsUrl, headers=headers, verify=False)
	if(response.status_code != 200):
		print(f"Error: API returned status code {response.status_code}")
		print(response.text)
		exit(1)
	
	vmlist = json.loads(response.text)

	for vm in vmlist["entities"]:
		print(f"{vm['metadata']['uuid']}:'{vm['status']['name']}'")

	#print(response.text)

if __name__ == "__main__":
	main()