# Entry point to start the application

# Tutorial for implementing new Views:
#   1. Go to the source file in the /views folder associating with that view (for example: LoginView goes to 'view_authentication.py')
#   2. Implementing the redirecting logic for the View (as a new View class) and the business logic for that View (implement in
# the Controller associating View class)
#       2.1 Note: import the appropriate Controller class into 'controllers/__init__.py'
#       2.2 Note: the function in each View must all be named "dispatch_request()"
#   3. Go to 'views/__init__.py' and import the new View (just follow the convention in that file)
#   4. Register the View: Go to 'app/__init__.py', under Registering views (just follow the convention in that file)
#   5. Test out the View before you commit to the remote repository
#   6. Check 'done' for your tasks on Jira

# If you have trouble with importing stuffs in Python, please contact Tu Em

from app import krm_app_instance

if __name__ == "__main__":
    krm_app_instance.run(debug=True)