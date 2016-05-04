import json


def main():
    with open("./.key/key") as f:
        key = json.loads(f.read())
        print(key)


if __name__ == '__main__':
    main()
