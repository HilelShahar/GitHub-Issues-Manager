import requests

BASE_URL = "https://api.github.com"
TOKEN = "Your_Personal_Token"

def validation_interface() -> str:
    global TOKEN
    TOKEN = input("\nEnter your GitHub Personal Access Token: ")
    username = None
    
    while username is None:
        username = validate_token()
        
        if not username:
            while True:
                print("\nOptions:")
                print("1. Try again")
                print("2. Exit")
                choice = input("Choose an option: ")    
                
                if choice == "1":
                    TOKEN = input("\nEnter your GitHub Personal Access Token: ")
                    break
                elif choice == "2":
                    print("\nExiting... See ya!\n")
                    return
                else:
                    print("\nInvalid choice. Please try again.")
            
    print(F"\nHello {username}! \nWelcome to your: GitHub-Issues-Manager")
    repo = input("\nEnter your repository name: ")
    repo = username + '/' + repo
    
    while not validate_repo(repo):
        while True:
            print("\nOptions:")
            print("1. Try again")
            print("2. Exit")
            choice = input("Choose an option: ")    
                    
            if choice == "1":
                repo = input("\nEnter your repository name: ")
                repo = username + '/' + repo
                break
            elif choice == "2":
                print("\nExiting... See ya!\n")
                return
            else:
                print("\nInvalid choice. Please try again.")         
    return repo
        
        
def validate_token() -> str:
    url = "https://api.github.com/user"
    headers = {"Authorization": f"token {TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    #Checking if the given token is valid
    if response.status_code == 200:
        user = response.json()
        return user['login']  
    elif response.status_code == 401:
        print("\nError: Invalid or expired token.")
        return None
    else:
        print(f"\nFailed to validate token: Error code {response.status_code}")
        return None
    
    
def validate_repo(repo: str):
    url = f"{BASE_URL}/repos/{repo}"
    headers = {"Authorization": f"token {TOKEN}"}

    response = requests.get(url, headers=headers)
    
    #Checking if the given repository exists
    if response.status_code == 200:
        return True
    elif response.status_code == 404:
        print("\nRepository was not found.")
        return False
    else:
        print(f"\nFailed to validate repository: Error_code {response.status_code}")
        return False
    
    
def list_issues(repo, state=None):
    url = f"{BASE_URL}/repos/{repo}/issues"
    headers = {"Authorization": f"token {TOKEN}"}
    
    if state:
        state = state.lower()
        if state not in ["open", "closed"]:
            print("\nInvalid status type (check grammer).")
            return
        params = {"state": state}
    else:
        params = {"state": "all"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        issues = response.json()
        #Filtering by status
        if issues:
            print(f"\n{params['state'].capitalize()} issues:")
            for issue in issues:
                print(f"#{issue['number']}: {issue['title']}")
        else:
            print("\nNo issues found.")
    else:
        print(f"\nFailed to fetch issues: Error_code {response.status_code}")


def create_issue(repo, title, body):
    url = f"{BASE_URL}/repos/{repo}/issues"
    headers = {"Authorization": f"token {TOKEN}"}
    data = {"title": title, "body": body}

    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        #If issue was successfully created, the url is printed from the json dict
        print("\nIssue created:", response.json()["html_url"])
    else:
        print(f"\nFailed to create issue: Error_code {response.status_code}")


def close_issue(repo, issue_number):
    url = f"{BASE_URL}/repos/{repo}/issues/{issue_number}"
    headers = {"Authorization": f"token {TOKEN}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        issue = response.json()
        if issue["state"] == "closed":
            print(f"\nIssue #{issue_number} is already closed.")
            return
    elif response.status_code == 404:
        print(f"\nIssue #{issue_number} not found in repository.")
        return
    else:
        print(f"\nFailed to fetch issue details: Error_code {response.status_code}")
        
    data = {"state": "closed"}
    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"\nIssue #{issue_number} closed.")
    else:
        print(f"\nFailed to close issue: Error_code {response.status_code}")


def main():
    repo = validation_interface()
    if not repo:
        return
        
    while True:
        print("\nOptions:")
        print("1. Get issues list")
        print("2. Create a new issue")
        print("3. Close an issue")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            state = input("\nEnter status (specify open/closed, or leave blank for all): ")
            list_issues(repo, state)
        elif choice == "2":
            title = input("\nEnter issue title: ")
            body = input("\nEnter issue description: ")
            create_issue(repo, title, body)
        elif choice == "3":
            issue_number = input("\nEnter issue number to close: ")
            close_issue(repo, issue_number)
        elif choice == "4":
            print("\nExiting... See ya!\n")
            break
        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()