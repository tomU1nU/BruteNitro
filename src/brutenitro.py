import os, requests, random, threading, json, time
from colorama import Fore
from webserver import keep_alive
keep_alive()

def printer(color, status, code) -> None:
	threading.Lock().acquire()
	print(f"{color} {status} > {Fore.RESET}discord.gift/{code}")
	return

class Worker():              
    def pick_proxy(self):
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f]
        
        return random.choice(proxies)

    def config(self, args, extra=False):
        with open('config.json', 'r') as conf:
			
            data = json.load(conf)
        if extra:
            return data[args][extra]
        else:
            return data[args]
    
    def run(self):
        self.code = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890") for _ in range(16))
        try:
            req = requests.get(
				f'https://discordapp.com/api/v6/entitlements/gift-codes/{self.code}?with_application=false&with_subscription_plan=true', # API Endpoint to check if the nitro code is valid
				proxies={
					'http': self.config("proxies") + '://' + self.pick_proxy(),
					'https': self.config("proxies") + '://' + self.pick_proxy()
					}, 
				timeout = 0.5 # Timeout time between each request, sometimes causes proccess to be killed if it is too low of a number.
			)
            
            if req.status_code == 200:
                printer(Fore.LIGHTGREEN_EX, " Valid ", self.code)
                try:
                    requests.post(
						Worker().config("webhook", "url"), 
						json={
							"content": f"Nitro Code, Redeem ASAP\n\nhttps://discord.gift/{self.code}",
							"username": Worker().config("webhook", "username"),
							"avatar_url": Worker().config("webhook", "avatar")
						})
                except:
                    pass
            elif req.status_code == 429:
                rate = (int(req.json()['retry_after']) / 1000) + 1
                printer(Fore.LIGHTBLUE_EX, "RTlimit", self.code)
                time.sleep(rate)
        except KeyboardInterrupt:
            threading.Lock().acquire() # Kill all Threads
            print(f"{Fore.LIGHTRED_EX} Stopped > {Fore.RESET}BruteNitro Sniper Stopped by Keyboard Interrupt.")
            exit()
        except:
            pass # Kill me if you want


if __name__ == "__main__": # Driver Code
	print("""
	                                  .-.
     (___________________________()6 `-,       BruteNitro | Nitro code brute forcing
     (   ______________________   /''"`
     //\\                      //\\
     "" ""                     "" ""
	""")
	DNG = Worker()
	while True:
		if threading.active_count() <= int(Worker().config("thread")):  
			threading.Thread(target=DNG.run).start()
