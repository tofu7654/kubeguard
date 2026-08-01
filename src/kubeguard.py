import json
from typing import Any
import sys

RESTART_THRESHOLD = 5

def main() -> None:
    # get path of json file from command line arg
    if len(sys.argv) < 2:
        print("Usage: python kubeguard.py <pods.json>")
        sys.exit(1)

    # store path 
    pod_json_path = sys.argv[1]

    # parse the json into dictionary
    pods_data = load_pods(pod_json_path)

    # obtain dictionary of pods and their statuses
    unhealthy_pods = find_unhealthy_pods(pods_data)

    # print the results
    print_results(unhealthy_pods)

def load_pods(path: str) -> dict[str, Any]:
    # load in the json file as a python dictionary
    try:
        with open(path, "r", encoding="utf-8") as file:
            pods_data = json.load(file)
    except FileNotFoundError:
        print(f"ERROR: File not found: {path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"ERROR: Failed to parse JSON", file=sys.stderr)
        sys.exit(1)

    return pods_data

def find_unhealthy_pods(pods_data: dict[str, Any]) -> dict[str, list[str]]:

    # hold the statuses of the unhealthy pods
    unhealthy_pods = {}

    # loop through the list of pods
    for pod in pods_data["items"]: 
        pod_name = pod["metadata"]["name"] # get the name of the pod

        # analyze the pod and store the condition messages in a list
        issues = find_pod_issues(pod)

        # put this issue in the overall unhealthy_pods
        if issues:
            unhealthy_pods[pod_name] = issues

    # return the list of unhealthy pods and the reasons        
    return unhealthy_pods

def print_results(unhealthy_pods: dict[str, list[str]]) -> None:
    if not unhealthy_pods:
        print("All pods are healthy.")
        return

    print("Unhealthy pods:")
    # loop through the dictionary
    for pod, issues in unhealthy_pods.items():
        # print pod name
        print(pod)

        # for each status message for a pod, print it
        for issue in issues:
            print("- " + issue)

# this function determines the issues a pod may have and returns a list, empty if healthy
def find_pod_issues(pod: dict[str, Any]) -> list[str]:
    issues = []

    total_restart_count = 0
    for container_status in pod["status"]["containerStatuses"]: # loop through the containerstatuses
        container_name = container_status["name"]

        # check if the container is ready
        if not container_status["ready"]:
            # record the readiness issue
            issues.append(f"Container {container_name} is not ready")

        # track the total restarts across all containers in this pod
        total_restart_count += container_status["restartCount"]

    # check if the containers have restarted more than 5 times across all containers
    if total_restart_count > RESTART_THRESHOLD:
        # record the excessive restart count
        issues.append(f"Total restart count: {total_restart_count}")

    return issues
     
if __name__ == "__main__":
    main()