from cli import find_pod_issues, find_unhealthy_pods, validate_pods_data
import pytest

# Tests for find_pod_issues

def test_healthy_pod_has_no_issues():
    
    pod = {
        "metadata": {"name": "api"},
        "status": {
            "containerStatuses": [
                {
                    "name": "api",
                    "ready": True,
                    "restartCount": 0
                }
            ]
        }
    }

    issues = find_pod_issues(pod)

    assert issues == []

def test_unready_pod_has_issues():

    pod = {
        "metadata": {"name": "api"},
        "status": {
            "containerStatuses": [
                {
                    "name": "api",
                    "ready": False,
                    "restartCount": 0
                }
            ]
        }
    }

    issues = find_pod_issues(pod)

    assert issues == ["Container api is not ready"]


def test_restart_count_above_threshold_has_issues():

    pod = {
        "metadata": {"name": "api"},
        "status": {
            "containerStatuses": [
                {
                    "name": "api",
                    "ready": True,
                    "restartCount": 6
                }
            ]
        }
    }

    issues = find_pod_issues(pod)

    assert issues == ["Total restart count: 6"]

def test_unread_and_above_restart_threshold_has_issues():

    pod = {
        "metadata": {"name": "api"},
        "status": {
            "containerStatuses": [
                {
                    "name": "api",
                    "ready": False,
                    "restartCount": 6
                }
            ]
        }
    }

    issues = find_pod_issues(pod)

    assert issues == ["Container api is not ready", "Total restart count: 6"]

def test_multiple_containers_restart_count():

    pod = {
            "metadata": {"name": "api"},
            "status": {
                "containerStatuses": [
                    {
                        "name": "api",
                        "ready": True,
                        "restartCount": 6
                    },
                    {
                        "name": "postgres",
                        "ready": True,
                        "restartCount": 5
                    }
                ]
            }
        }
    
    issues = find_pod_issues(pod)
    
    assert issues == ["Total restart count: 11"]

def test_five_total_restarts_no_issues():

    pod = {
            "metadata": {"name": "api"},
            "status": {
                "containerStatuses": [
                    {
                        "name": "api",
                        "ready": True,
                        "restartCount": 5
                    }
                ]
            }
        }
        
    issues = find_pod_issues(pod)
        
    assert issues == []

# Tests for find_unhealthy_pods()

def test_all_healthy_pods_empty_list():
    pods_data = {
        "items": [
            {
            "metadata": {"name": "api"},
            "status": {
                "containerStatuses": [
                {
                    "name": "api",
                    "ready": True,
                    "restartCount": 0
                },
                {
                    "name": "sidecar",
                    "ready": True,
                    "restartCount": 0
                }
                ]
            }
            }
        ]
    }

    unhealthy_pods = find_unhealthy_pods(pods_data)
            
    assert unhealthy_pods == {}

# Tests for validate_pods_data()

def test_missing_items_exit_code():

    pods_data = { "stuff":
                    {
                    "metadata": {"name": "api"},
                    "status": {
                        "containerStatuses": [
                        {
                            "name": "api",
                            "ready": True,
                            "restartCount": 0
                        },
                        {
                            "name": "sidecar",
                            "ready": True,
                            "restartCount": 0
                        }
                        ]
                    }
                }
        }

    with pytest.raises(SystemExit): 
        validate_pods_data(pods_data)

def test_valid_pods_data_no_errors():

    pods_data = {
        "items": [
            {
            "metadata": {"name": "api"},
            "status": {
                "containerStatuses": [
                {
                    "name": "api",
                    "ready": True,
                    "restartCount": 0
                },
                {
                    "name": "sidecar",
                    "ready": True,
                    "restartCount": 0
                }
                ]
            }
            }
        ]
    }

    validate_pods_data(pods_data)


    

    



