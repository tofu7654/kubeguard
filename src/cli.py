from typing import Any
import sys
import input
import analyzer

def main() -> None:
    # get path of json file from command line arg
    if len(sys.argv) < 2:
        print("Usage: python kubeguard.py <pods.json>")
        sys.exit(1)

    # store path 
    pod_json_path = sys.argv[1]

    # parse the json into dictionary
    pods_data = input.load_pods(pod_json_path)

    # validate that the pod has the correct fields
    input.validate_pods_data(pods_data)

    # obtain dictionary of pods and their statuses
    unhealthy_pods = analyzer.find_unhealthy_pods(pods_data)

    # print the results
    print_results(unhealthy_pods)


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
     
if __name__ == "__main__":
    main()