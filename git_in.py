import base64
from github import Github

token = "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"
repository = "1masa0ka/CR"
fileName = "CR_date.csv"

def get_file():

    g = Github(token)
    repo = g.get_repo(repository)
    contents = repo.get_contents(fileName)
    content = base64.b64decode(contents.content)

    with open("copy_" + fileName, mode="wb") as f:
        f.write(content)

    return("[succeed]")

def main():
        result = get_file()
        print(result)

if __name__ == "__main__":
    main()

