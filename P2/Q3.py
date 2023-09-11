class turing_machine():
    def __init__(self):
        self.transitions = input().split('00')




turing = turing_machine()
n = int(input())
for i in range(n):
    w = input()
    j = 0
    p=0
    while j < len(w):
        for tr in turing.transitions: 
            if(w[j] != tr[0]):
                p+=1
        print('Accepted')
        break
        print('Rejected')
    
