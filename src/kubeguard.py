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

    # validate that the pod has the correct fields
    validate_pods_data(pods_data)

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

def validate_pods_data(pods_data: dict[str, Any]) -> None:

    # first verify that the top level is a dictionary
    if not isinstance(pods_data, dict):
        print("ERROR: The given pods_data is not a dictionary", file=sys.stderr)
        sys.exit(1)

    # first we check if items is at the top level
    if "items" not in pods_data:
        print("ERROR: No items field in JSON", file=sys.stderr)
        sys.exit(1)

    # next we check to see if the items field is a list
    if not isinstance(pods_data["items"], list):
        print("ERROR: Items field is not a list", file=sys.stderr)
        sys.exit(1)

    # check if list is empty
    if not pods_data["items"]:
        return

    for pod_index, pod in enumerate(pods_data["items"]):

        # verify that the pod is a dictionary
        if not isinstance(pod, dict):
            print(f"ERROR: Pod at index {pod_index} is not a dictionary", file=sys.stderr)
            sys.exit(1)

        # check for metadata field in items field
        if "metadata" not in pod:
            print(f"ERROR: Pod at index {pod_index} is missing metadata field", file=sys.stderr)
            sys.exit(1)

        if not isinstance(pod["metadata"], dict):
            print(f"ERROR: Pod at index {pod_index} has metadata field that is not a dictionary", file=sys.stderr)
            sys.exit(1)

        # check if name field exists in metadata field
        if "name" not in pod["metadata"]:
            print(f"ERROR: Pod at index {pod_index} is missing metadata.name field", file=sys.stderr)
            sys.exit(1)

        pod_name = pod["metadata"]["name"]

        # check if status field exists in items field
        if "status" not in pod:
            print(f"ERROR: Pod {pod_name} is missing status field", file=sys.stderr)
            sys.exit(1)

        # validate that status field is a dictionary
        if not isinstance(pod["status"], dict):
            print(f"ERROR: Pod {pod_name} has status field which is not a dictionary", file=sys.stderr)
            sys.exit(1)

        # check if containerStatuses field exists in status field
        if "containerStatuses" not in pod["status"]:
            print(f"ERROR: Pod {pod_name} is missing status.containerStatuses field", file=sys.stderr)
            sys.exit(1)

        # check if containerStatuses is a list
        if not isinstance(pod["status"]["containerStatuses"], list):
            print(f"ERROR: Pod {pod_name} has ContainerStatuses field which is not a list", file=sys.stderr)
            sys.exit(1)

        # loop through container statuses to validate
        for container_index, container_status in enumerate(pod["status"]["containerStatuses"]):

            # verify if each entry in containerstatuses is a dictionary
            if not isinstance(container_status, dict):
                print(f"ERROR: Container at index {container_index} in pod {pod_name} is not a dictionary", file=sys.stderr)
                sys.exit(1)

            # check if name is in containerStatuses
            if "name" not in container_status:
                print(f"ERROR: Container at index {container_index} in pod {pod_name} is missing containerStatuses.name field", file=sys.stderr)
                sys.exit(1)

            # check if ready is in containerStatuses
            if "ready" not in container_status:
                print(f"ERROR: Container at index {container_index} in pod {pod_name} is missing containerStatuses.ready field", file=sys.stderr)
                sys.exit(1)

            # check if restartCount is in containerStatuses
            if "restartCount" not in container_status:
                print(f"ERROR: Container at index {container_index} in pod {pod_name} is missing containerStatuses.restartCount field", file=sys.stderr)
                sys.exit(1)

            # check if state is in containerStatuses
            if "state" not in container_status:
                print(f"ERROR: Container at index {container_index} in pod {pod_name} is missing containerStatuses.state field", file=sys.stderr)
                sys.exit(1)

            # check if state field is a dictionary
            if not isinstance(container_status["state"], dict):
                print(f"ERROR: Container at index {container_index} in pod {pod_name} has status field which is not a dictionary", file=sys.stderr)
                sys.exit(1)

            # check if the types of states exist and are in correct format
            if "waiting" in container_status["state"]:

                if not isinstance(container_status["state"]["waiting"], dict):
                    print(f"ERROR: Container at index {container_index} in pod {pod_name} has status.waiting field which is not a dictionary", file=sys.stderr)
                    sys.exit(1)
            # account for every state 
            if "waiting" in container_status["state"]:
                if not isinstance(container_status["state"]["waiting"], dict):
                    print(f"ERROR: Container at index {container_index} in pod {pod_name} has status.waiting field which is not a dictionary", file=sys.stderr)
                    sys.exit(1)
                if "reason" in state["waiting"]:
                    reason = container_status["state"]["waiting"]["reason"]
            elif "terminated" in state:
                if "reason" in state["waiting"]:
                    reason = container_status["state"]["waiting"]["reason"]
            else:
            

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

            state = container_status["state"]
            reason = container_status["state"]["waiting"]["reason"]

            # record the readiness issue with the state
            issues.append(f"Container {container_name} is not ready: {reason}")

        # track the total restarts across all containers in this pod
        total_restart_count += container_status["restartCount"]

    # check if the containers have restarted more than 5 times across all containers
    if total_restart_count > RESTART_THRESHOLD:
        # record the excessive restart count
        issues.append(f"Total restart count: {total_restart_count}")

    return issues
     
if __name__ == "__main__":
    main()