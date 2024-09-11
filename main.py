from testrail_api import TestRailAPI
from testrail_api._exception import StatusCodeError
from dotenv import dotenv_values
from os import system


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def grab_input(some_iterable: tuple) -> int:
    while 1:
        try:
            choice =  int(input(f"Your choice (only single one, 0 to exit): "))
        except ValueError:
            print("Enter a valid integer number!")
        else:
            return choice if choice > 0 else 0


def check_presence(number, numbers) -> int or None:
    if not number in numbers:
        raise NotImplementedError("Wrong choice!")
    elif number == 0:
        print("Nothing to do, exitting...")
        return None
    else:
        return number


def do_work(plan_id, action, api_local) -> None:
    if action == 1:
        version = str(input("Please enter a version of your build here >>> "))
        sections = api_local.plans.get_plan(plan_id=plan_id)["entries"]
        for section in sections:
            for run in section["runs"]:
                print(run["name"], run["config"], run["id"])
                for test in api_local.tests.get_tests(run_id=run["id"])["tests"]:
                    if test["status_id"] != 4:
                        api_local.results.add_result(
                            test_id=test["id"],
                            status_id=4,
                            comment="Put into retest by python3 automatically",
                            version=version
                        )
                        print(f"{Colors.OKGREEN}{test['id']} {test['title']} Marked to RETEST!{Colors.ENDC}")
                    else:
                        print(f"{Colors.WARNING}{test['id']} {test['title']} Was already in RETEST!{Colors.ENDC}")


print("\nConnecting to the server...")
env_vars = dotenv_values(".env")

api = TestRailAPI(
    url=env_vars["TESTRAIL_URL"],
    email=env_vars["TESTRAIL_EMAIL"],
    password=env_vars["TESTRAIL_PASSWORD"]
)

# validate by sending a request and process response code
try:
    response = api.get("get_projects")
except StatusCodeError as error:
    print("Error Connecting to the Testrail API! The reason:", error)
    exit(1)
else:
    print("Connected successfully!")

# define actions here
actions: dict[int, str] = {
    1: "Mark all test runs for Retest"
}

# Ask the user to choose a project
projects: dict[int, str] = {
    project["id"]: [project["name"], project["url"]] for project in api.projects.get_projects()["projects"]
}
print("There are projects you can choose from:")
print("\n".join([f'===================={id}. {projects[id][0]}====================\nLink: {projects[id][1]}\n' for id in projects.keys()]))
project_ids = tuple(projects.keys())
project_id = grab_input(project_ids)
project_id = check_presence(project_id, project_ids)
if project_id is None:
    exit(0)
print(f"\nChose project {projects[project_id][0]}!")

# TODO get project id and go to the menu of a project with test plans. Choose a plan
print("There are test plans you can choose from:")
plans: dict[int, str] = {
    plan["id"]: [plan["name"], plan["url"]] for plan in api.plans.get_plans(project_id=project_id)["plans"]
}
plan_ids = tuple(plans.keys())
print("\n".join([f'===================={id}. {plans[id][0]}==================\nLink: {plans[id][1]}\n' for id in plans.keys()]))
plan_id = grab_input(plan_ids)
plan_id = check_presence(plan_id, plan_ids)
if plan_id is None:
    exit(0)
print(f"\nChose plan {plans[plan_id][0]}!")

print(f"So, project is {projects[project_id][0]} and test plan is {plans[plan_id][0]}")
action_prompt = "\n".join([f"{action_id}: {actions[action_id]}" for action_id in actions.keys()])
print(action_prompt)
action = grab_input(tuple(actions.values()))
if action == 0:
    print("Nothing to do, exitting...")
    exit(0)

# Notify user about his intentions
confirmation = input(f"\nProject: {projects[project_id][0]}. You are choosing to {actions[action]} on a test plan {plans[plan_id][0]}. The dev is not responsible for your actions, when you can change the data on another project by mistake! Are you sure? [y/N] >>> ")
if confirmation == "\n":
    confirmation = "n"
elif confirmation.lower() == "y":
    do_work(
        plan_id=plan_id,
        action=action,
        api_local=api
    )
    pass
else:
    print("You changed your mind. Quitting!")
    exit(0)
