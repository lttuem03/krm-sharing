# Entry point to start the application

from app import krm_app_instance

if __name__ == "__main__":
    krm_app_instance.run(debug=True, port= 12345)