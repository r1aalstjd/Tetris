import random
import time

x=0
y=0

i=0
j=0
k=0

cnt=0
blockshape=0
rotation=0
rotation=0

godrop=0
finishdrop=0
startground=0

board=[
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1]
]

blocks=[
	[
		[
			[0,1,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]
		],
		[
			[0,1,0,0],[0,1,1,0],[0,1,0,0],[0,0,0,0]
		],
		[
			[1,1,1,0],[0,1,0,0],[0,0,0,0],[0,0,0,0]
		],
		[
			[0,1,0,0],[1,1,0,0],[0,1,0,0],[0,0,0,0]
		]
	],
	[
		[
			[0,1,1,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]
		],
		[
			[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,0,0,0]
		],
		[
			[0,1,1,0],[1,1,0,0],[0,0,0,0],[0,0,0,0]
		],
		[
			[1,0,0,0],[1,1,0,0],[0,1,0,0],[0,0,0,0]
		]
	],
	[
		[
			[1,1,0,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]
		],
		[
			[0,1,0,0],[1,1,0,0],[1,0,0,0],[0,0,0,0]
		],
		[
			[1,1,0,0],[0,1,1,0],[0,0,0,0],[0,0,0,0]
		],
		[
			[0,1,0,0],[1,1,0,0],[1,0,0,0],[0,0,0,0]
		]
	],
	[
		[
			[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]
		],
		[
			[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]
		],
		[
			[0,1,0,0],[0,1,0,0],[0,1,0,0],[0,1,0,0]
		],
		[
			[0,0,0,0],[1,1,1,1],[0,0,0,0],[0,0,0,0]
		]
	],
	[
		[
			[1,0,0,0],[1,1,1,0],[0,0,0,0],[0,0,0,0]
		],
		[
			[1,1,0,0],[1,0,0,0],[1,0,0,0],[0,0,0,0]
		],
		[
			[0,0,0,0],[1,1,1,0],[0,0,1,0],[0,0,0,0]
		],
		[
			[0,1,0,0],[0,1,0,0],[1,1,0,0],[0,0,0,0]
		]
	],
	[
		[
			[0,0,0,0],[0,0,1,0],[1,1,1,0],[0,0,0,0]
		],
		[
			[1,0,0,0],[1,0,0,0],[1,1,0,0],[0,0,0,0]
		],
		[
			[0,0,0,0],[1,1,1,0],[1,0,0,0],[0,0,0,0]
		],
		[
			[1,1,0,0],[0,1,0,0],[0,1,0,0],[0,0,0,0]
		]
	],
	[
		[
			[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]
		],
		[
			[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]
		],
		[
			[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]
		],
		[
			[0,0,0,0],[0,1,1,0],[0,1,1,0],[0,0,0,0]
		]
	]
]

def randomblock():
    blockshape=random.randint(0,6)

def crash(x,y):
    for i in range(0,4):
        for j in range(0,4):
            if blocks[blockshape][rotation][i][j]==1 :
                if board[i+y][j+x] == 1 or board[i+y][j+x] == 2 :
                    return True
    return False

def dropblock():
    global x,y,godrop
    finishdrop=time.time()
    if finishdrop-godrop>800:
        if crash(x,y+1)==True:
            return
        y+=1
        godrop=time.time()
        startground=time.time()

def blockonground():
    global x,y
    if crash(x,y+1)==True:
        if finishdrop-startground>1000:
            for i in range(0,4):
                for j in range(0,4):
                    if blocks[blockshape][rotation][i][j]==1:
                        bload[i+y][i+x]=2
            x=8
            y=0

def removeline():
    for i in range(0,21):
        cnt=0
        for j in range(0,21):
            if board[i][j]==2:
                cnt+=1
        if cnt>=10:
            j=0
            while i-j>0:
                for k in range(1,11):
                    if i-j-1>=0:
                        board[i-j][k]=board[i-j-1][k]
                    else:
                        board[i-j][k]=0

x=8
y=0
godrop=time.time()
randomblock()

while True:
    