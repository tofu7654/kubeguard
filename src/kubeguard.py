import json
from typing import Any # import type definntions

def main() -> None:
    # load in the json file as a python dictionary
    pod_json_path = input("Please type the path to the pod json: ")
    # parse the json into dictionary
    pods_data = load_pods(pod_json_path)

    # obtain list of unhealthy pods
    unhealthy_pods = find_unhealthy_pods(pods_data)

    # print the results
    print_results(unhealthy_pods)

def load_pods(path: str) -> dict[str, Any]:
# load in the json file as a python dictionary
    with open(path, "r", encoding="utf-8") as file:
        pods_data = json.load(file)
    return pods_data

def find_unhealthy_pods(pods_data: dict[str, Any]) -> list[str]:
# initialize list to hold pod names
    unhealthy_pods = []
    # loop through the list of pods
    for pod in pods_data["items"]: 
        pod_name = pod["metadata"]["name"] # get the name of the pod
        pod_status = pod["status"] # get the statuses of the pod
        is_pod_unhealthy = False
        for container_status in pod_status["containerStatuses"]: # loop through the containerstatuses
            # set flag as true if any container is not ready
            if not container_status["ready"]:
                is_pod_unhealthy = True
                break
        
        # Report pod if any of the containers are not ready
        if is_pod_unhealthy:
            unhealthy_pods.append(pod_name)
    # return the list of unhealthy pods        
    return unhealthy_pods

def print_results(unhealthy_pods: list[str]) -> None:
    # if unhealthy_pods array is empty
    if not unhealthy_pods:
        print("All pods are healthy.")
    # otherwise print the unhealthy pods
    else:
        print("Unhealthy pods:")
        for pod_name in unhealthy_pods:
            print(pod_name)
     
if __name__ == "__main__":
    main()