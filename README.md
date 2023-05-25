# Mini-FORTRAN-Compiler

Welcome to the mini compiler !
<div align="right">
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b8/Fortran_logo.svg/640px-Fortran_logo.svg.png" alt="FORTRAN mini combiler" width="40" height="40"/>
</div>


here we designed a valid grammar for FORTRAN  language that was refactoring to be 
free from (left recursion and left factoring ) then implemented to handle FORTRAN syntax  





## Key Features


 ### ✅ Program supports animation :
 providing an animation for the DFA for 
every token with the same order of the syntax 

### ✅ Program implements panic mode : 
when error detected in your syntax code 
the program will proceed checking to other token and wont stop until the end of 
the syntax

### ✅Program can identify type of error :
by detecting errors in syntax the 
parser can figure the correct tokens and show what should to be done 

### ✅Program can identify the line where the error occurred :
by getting errors 
the compiler can handle the line number of the syntax errors 

### ✅Program can generate DFA :
by using Pyvis library we made a large-scale 
diagram that contains all possible tokens for this language

## installation 

```python
# navigate to the folder dir
# create a new folder 
mkdir temporarily 

# to create the environment
python -m venv my_project

#c to the project
cd my_project
# to activat the environment
	.\Scripts\activate
	
# to deactivate  the environment
deactivate
git clone --branch master <repository_url>
 #you can chose master or main
 pip install -r requirements.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

