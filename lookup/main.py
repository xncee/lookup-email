import os, uuid, string, time, calendar, random, threading
from queue import Queue

try:
    import requests
except ImportError:
    os.system("pip install requests")
    import requests

class THRIDING():
    def __init__(self, target):
        self.threads_list = []
        self.target = target
    
    def gen(self, threads):
        for i in range(threads):
            t = threading.Thread(target=self.target)
            t.setDaemon(True)
            self.threads_list.append(t)
        return self.threads_list

    def start(self):
        for thread_start in self.threads_list:
            thread_start.start()

    def join(self):
        for thread_join in self.threads_list:
            thread_join.join()

class Xnce():
    def __init__(self):
        self.good, self.bad, self.error = 0, 0, 0
        try:
            self.users = list(open("list.txt","r").read().split("\n"))
        except:
            print("[-] list.txt is missing")
            input()
            exit()
        try:
            self.proxies = list(open("proxies.txt","r").read().split("\n"))
        except:
            print("[-] proxies.txt is missing")
            input()
            exit()
        
        self.UQue = Queue()
        for x in self.users:
            self.UQue.put(x)
        
        self.lock = threading.Lock()
    def random_proxy(self):
        prox = random.choice(self.proxies)
        proxy = {"http": prox, "https": prox}
        return proxy
    def check(self, user):
        head = {"user-agent": f"Instagram 150.0.0.0.000 Android (29/10; 300dpi; 720x1440; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}/{''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; {''.join(random.choices(string.ascii_lowercase+string.digits, k=16))}; en_GB;)",}
        data = {
            "phone_id": uuid.uuid4(),
            "q": user,
            "guid": uuid.uuid4(),
            "device_id": uuid.uuid4(),
            "android_build_type":"release",
            "waterfall_id": uuid.uuid4(),
            "directly_sign_in":"true",
            "is_wa_installed":"false"
        }
        req = requests.post("https://i.instagram.com/api/v1/users/lookup/", headers=head, data=data, proxies=self.random_proxy())
        #print(req.text, req.status_code)
        if "email_sent" in req.text:
            self.good += 1
            open("good.txt","a").write(f"{user}\n")
            print(f"\r[+] Good: {self.good} Bad: {self.bad} Error: {self.error}", end="")
        elif "No users found" in req.text:
            self.bad += 1
            open("bad.txt","a").write(f"{user}\n")
            print(f"\r[+] Good: {self.good} Bad: {self.bad} Error: {self.error}", end="")
        elif req.status_code==429:
            self.error += 1
            print(f"\r[+] Good: {self.good} Bad: {self.bad} Error: {self.error}", end="")
            return self.check(user)
    def main(self):
        while not self.UQue.empty():
            try:
                my_user = self.UQue.get()
                self.check(my_user)
                self.UQue.task_done()
            except:
                pass
x = Xnce()
th = int(input("[+] Threads : "))
input("[+] Enter To Start: ")
t = THRIDING(x.main)
t.gen(th)
t.start()
t.join()
input("\n[-] Enter To Exit: ")
exit()