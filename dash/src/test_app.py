import requests


"""
Пример того как получить доступ к нашему апи.
"""
if __name__ == "__main__":
    print(requests.get("http://server:5000").json())