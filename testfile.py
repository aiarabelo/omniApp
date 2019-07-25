import json

filename = "userdata.json"
with open(filename, "r") as f:
    contents = json.loads(f.read())

question = "Are you authorized to work in the country from which you are applying? "
answer = input(question)
print(answer)

contents[question] = answer
print(contents)

with open(filename, "w+") as f:
    f.write(json.dumps(contents))
