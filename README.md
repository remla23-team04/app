### Changing the code + running

When updating the code you might want to run: 
```
docker compose up --build app
```
to only rebuild the `app`, cause it takes like 2min to rebuild the entire thing, and `docker compose up` doesn't update the code.

### Debugging

When running the app through docker the normal `print()` in Python doesn't show any output (you can do it through the js code and it will show it in the console).
    
OR you can make use of an output file and copy it from the docker container like this: 
```
docker cp app:debugging_output.txt <path_to_root_project_folder>\app
```

in code usage:
```
# Debugging stuff
with open('/debugging_output.txt', 'w') as f:
    f.write("sentiment: " + str(response_data["sentiment"]) + "\n")
    f.write("review: " + str(review) + "\n")
```

