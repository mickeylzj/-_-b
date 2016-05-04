import json
import keymanage  # get keys


def main():
<<<<<<< HEAD
    pass
=======
    with open("./.key/key") as f:
        key = json.loads(f.read())
        print(key)
>>>>>>> origin/master


if __name__ == '__main__':
    main()
