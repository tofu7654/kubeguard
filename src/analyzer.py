from typing import Any

RESTART_THRESHOLD = 5

# this function takes a dictionary of pods_data and creates a dictionary with pods as keys and their issues as values
def find_unhealthy_pods(pods_data: dict[str, Any]) -> dict[str, list[str]]:

    # hold the statuses of the unhealthy pods
    unhealthy_pods = {}

    # loop through the list of pods
    for pod in pods_data["items"]: 
        pod_name = pod["metadata"]["name"] # get the name of the pod

        # analyze the pod and store the condition messages in a list
        issues = find_pod_issues(pod)

        # put this issue in the overall unhealthy_pods dictionary
        if issues:
            unhealthy_pods[pod_name] = issues

    # return the list of unhealthy pods and the reasons        
    return unhealthy_pods

# this function determines the issues a pod may have and returns a list, empty if healthy
def find_pod_issues(pod: dict[str, Any]) -> list[str]:
    issues = []

    total_restart_count = 0
    for container_status in pod["status"]["containerStatuses"]: # loop through the containerstatuses
        container_name = container_status["name"]

        # check if the container is ready
        if not container_status["ready"]:

            state = container_status["state"]

            # capture the reason if container is in a malfunctioning state
            if "waiting" in state:
                reason = state["waiting"]["reason"]
                # record the readiness issue with the state
                issues.append(f"Container {container_name} is not ready: waiting, {reason}")
            elif "terminated" in state:
                reason = state["terminated"]["reason"]
                # record the readiness issue with the state
                issues.append(f"Container {container_name} is not ready: terminated, {reason}")
            else:
                # record that container is running
                issues.append(f"Container {container_name} is running but not ready")

        # track the total restarts across all containers in this pod
        total_restart_count += container_status["restartCount"]

    # check if the containers have restarted more than 5 times across all containers
    if total_restart_count > RESTART_THRESHOLD:
        # record the excessive restart count
        issues.append(f"Total restart count: {total_restart_count}")

    return issues