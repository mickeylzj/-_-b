import json


def main():
    with open("./.key/key") as f:
        aa = f.read()
        print aa
        a = json.loads(aa)
        print a


if __name__ == '__main__':
    main()
