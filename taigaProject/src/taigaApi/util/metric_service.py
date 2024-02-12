from ..task.getTaskHistory import get_task_lead_time, get_task_cycle_time
from ..userStory.getUserStory import get_us_lead_time, get_us_cycle_time


def get_lead_time_details(project_details, auth_token):
    us_lead_time, avg_us_lt = get_us_lead_time(project_details["id"], auth_token)
    task_lead_time, avg_task_lt = get_task_lead_time(project_details["id"], auth_token)
    
    us_lead_time.sort(key=lambda l: l["endDate"])
    task_lead_time.sort(key=lambda l: l["endDate"])

    #get objects created that store the details for task and user story lead times
    task_lead_time = get_lead_time_object("task", task_lead_time, avg_task_lt)
    us_lead_time = get_lead_time_object("userStory", us_lead_time, avg_us_lt)

    lead_time = {
        "storiesLeadTime": us_lead_time,
        "tasksLeadTime": task_lead_time
    }
    return metric_object("LEAD", "leadTime", lead_time, project_details)

def get_lead_time_object(object_type, task_lead_time, avg_task_lt):
    return {
        object_type: task_lead_time,
        "avgLeadTime": avg_task_lt
    }

def metric_object(metric, time_key, lead_time, project_details):
    return {
        "metric": metric,
        time_key: lead_time,
        "projectInfo": {
            "name": project_details["name"],
            "members": project_details["members"]
        }
    }
    

def get_cycle_time_details(project_details, auth_token):
    task_cycle_time, avg_task_ct = get_task_cycle_time(project_details["id"], auth_token)
    us_cycle_time, avg_us_ct = get_us_cycle_time(project_details["id"], auth_token)
    
    task_cycle_time.sort(key=lambda l: l["endDate"])
    us_cycle_time.sort(key=lambda l: l["endDate"])
    
    task_cycle_time = get_cycle_time_object("task", task_cycle_time, avg_task_ct)
    us_cycle_time = get_cycle_time_object("story", us_cycle_time, avg_us_ct)
    
    cycle_time = {
        "taskCycleTime": task_cycle_time,
        "storyCycleTime": us_cycle_time
    }
    return metric_object("CYCLE", "cycleTime", cycle_time, project_details)


def get_cycle_time_object(object_type, cycle_time, avg_lt):
    return {
        object_type: cycle_time,
        "avgCycleTime": avg_lt
    }
