from datetime import datetime
import json
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

baseUrl = "https://172.17.200.70:9440/api/nutanix/v3"

listVmsUrl = baseUrl+"/vms/list"

listVmsPayload =  """{
	"kind": "vm",
	"length": 200,
	"offset": 0
}"""

# Usado para ordenar a lista de VMs por nome
def vmListSort(n):
	return str.lower(n['name'])

def getExportVmUrl(uuid: str):
	return f"{baseUrl}/vms/{uuid}/export"

def getExportVmPayload(vmName: str):
	now = datetime.now()
	today = now.strftime("%d-%m-%Y")
	return json.dumps({"name": vmName + today, "disk_file_format": "vmdk"})

# Retorna um header de requisição HTTP para usar nas chamadas de API 
def getHeader(token: str, reqType="POST"):
	hdr = {
		"Accept": "application/json",
		"Authorization": f"Basic {token}"
	}
	if(reqType == "POST"): hdr.update({"Content-Type": "application/json"})

	return hdr

# Retorna uma lista das VMs com o uuid e o nome da VM 
def getVmList():
	with open("api_basic_auth_token.txt", 'r') as f:
		token = f.read()

	response = requests.request("post", listVmsUrl, data=listVmsPayload, headers=getHeader(token), verify=False)
	if(response.status_code != 200):
		print(f"Error: API returned status code {response.status_code}")
		print(response.text)
		exit(1)
	
	vmListRaw = json.loads(response.text)
	vmList = []

	for vm in vmListRaw["entities"]:
		vmList.append({"uuid": vm['metadata']['uuid'], "name": vm['status']['name']})
	
	del vmListRaw
	vmList.sort(key = vmListSort)

	return vmList

def main():
	vmList = getVmList()

	for vm in vmList:
		print(str(vm))

	#print(response.text)

if __name__ == "__main__":
	main()