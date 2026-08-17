import sys
import json
from typing import Any

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
                print(f"ERROR: Container at index {container_index} in pod {pod_name} has state field which is not a dictionary", file=sys.stderr)
                sys.exit(1)

            # account for every state 
            if "waiting" in container_status["state"]:
                if not isinstance(container_status["state"]["waiting"], dict):
                    print(f"ERROR: Container at index {container_index} in pod {pod_name} has state.waiting field which is not a dictionary", file=sys.stderr)
                    sys.exit(1)
                if "reason" not in container_status["state"]["waiting"]:
                    print(f"ERROR: Container at index {container_index} in pod {pod_name} does not have a state.waiting.reason field", file=sys.stderr)
                    sys.exit(1)
            # check for terminated state
            elif "terminated" in container_status["state"]:
                if not isinstance(container_status["state"]["terminated"], dict):
                    print(f"ERROR: Container at index {container_index} in pod {pod_name} has state.terminated field which is not a dictionary", file=sys.stderr)
                    sys.exit(1)
                if "reason" not in container_status["state"]["terminated"]:
                    print(f"ERROR: Container at index {container_index} in pod {pod_name} does not have a state.terminated.reason field", file=sys.stderr)
                    sys.exit(1)
            elif "running" in container_status["state"]:
                if not isinstance(container_status["state"]["running"], dict):
                    print(f"ERROR: Container at index {container_index} in pod {pod_name} has state.running field which is not a dictionary", file=sys.stderr)
                    sys.exit(1)
                # note there is not reason field for a ready container
            else:
                print(f"ERROR: Container at index {container_index} in pod {pod_name} has an invalid state field", file=sys.stderr)
                sys.exit(1)