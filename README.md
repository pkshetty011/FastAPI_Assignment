# FastAPI_Assignment
Code for Address Book Using Fast API

Steps to run the code :

STEP 1 :
Create a virtual envirnment if you are working on multipal projects
Command : python -m venv myenv   # replace "myenv" with the name of your virtual environment

STEP 2 :
Activate the virtual environment. Depending on your operating system, 
you can activate the virtual environment using one of the following commands:
* Unix-based systems: source myenv/bin/activate

* Windows: myenv\Scripts\activate

STEP 3 :
All the dependent packages are freezed in requirements.txt
    # pip install -r requirements.txt   [ Command to install the packages ]
    
STEP 4 :
Start the server using uvicorn:
Command : uvicorn app:app --reload

STEP 5 :
Now open the url where we can see FastAPI swagger doc with all the functionality mentioned in the assignment
url : http://localhost:8000/docs
