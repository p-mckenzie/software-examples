import numpy as np

class TicTacToe():
    def __init__(self):
        self.board = np.zeros((3,3), dtype=np.int8)
        self.game_finished = False
        self.user = 1
        
        self.corner = np.zeros((3,3))
        self.corner[0,0] = 1
        self.corner = self.corner.astype(bool)
        self.fork = np.zeros((3,3))
        self.fork[0,1] = 1
        self.fork[1,0] = 1
        self.fork = self.fork.astype(bool)
        self.space = np.zeros((3,3))
        self.space[0,2] = 1
        self.space[2,0] = 1
        self.space = self.space.astype(bool)
        
    def is_game_finished(self):
        for i in range(3):
            # check vertical
            if abs(self.board[:,i].sum())==3:
                self.winner = self.user
                self.how = 'vertical'
                return True
            
            # check horizontal
            if abs(self.board[i,:].sum())==3:
                self.winner = self.user
                self.how = 'horizontal'
                return True
            
        # check diagonal
        if abs((self.board * np.identity(3)).sum())==3 or abs((self.board * np.identity(3)[::-1]).sum())==3:
            self.winner = self.user
            self.how = 'horizontal'
            return True
            
        if ~(self.board==0).max():
            self.winner = 0
            self.how = 'draw'
            return True
        else:
            return False
            
    def twos(self, direction):
        for i in range(3):
            # check vertical
            if self.board[:,i].sum()==direction*2:
                self.board[:,i] = np.where(self.board[:,i]==0, self.user, self.board[:,i])
                return True
                
            # check horizontal
            elif self.board[i,:].sum()==direction*2:
                self.board[i,:] = np.where(self.board[i,:]==0, self.user, self.board[i,:])
                return True
                
        # check diagonal
        if (self.board * np.identity(3)).sum()==direction*2:
            self.board = np.where((np.identity(3)==1) & (self.board==0), self.user, self.board)
            return True
        elif (self.board * np.identity(3)[::-1]).sum()==direction*2:
            self.board = np.where((np.identity(3)[::-1]==1) & (self.board==0), self.user, self.board)
            return True
            
        return False
        
    def make_computer_move(self):
        # --------------- win ----------------------------
        if self.twos(self.user):
            return
        
        # --------------- or block ----------------------------
        if self.twos(-1*self.user):
            return
        
        # --------------- fork or block fork ----------------------------
        # l fork in corners
        for i in range(4):
            if (np.all(self.board[np.rot90(self.corner,i)]==0) and
                  np.all(self.board[np.rot90(self.space,i)]==0) and
                 (np.all(self.board[np.rot90(self.fork,i)]==-1) or np.all(self.board[np.rot90(self.fork,i)]==1))):
                self.board = np.where(np.rot90(self.corner,i), self.user, self.board)
                return
        
        # diagonal double fork (left and right)
        if ((self.board!=0).sum()==3 and (self.board[np.identity(3, dtype=np.bool)[::-1]]==np.array([1,-1,1])).all() and (self.board[np.identity(3, dtype=np.bool)] == np.array([0,-1,0])).all()) or ((self.board!=0).sum()==3 and (self.board[np.identity(3, dtype=np.bool)]==np.array([1,-1,1])).all() and (self.board[np.identity(3, dtype=np.bool)[::-1]] == np.array([0,-1,0])).all()):
            self.board[1,0] = self.user
            return
        
        # --------------- center ----------------------------
        if self.board[1,1]==0:
            self.board[1,1] = self.user
            return
        
        # --------------- opposite corner ----------------------------
        rows, cols = np.where(np.rot90(self.board==self.user*-1, 2) & (self.board==0))
        try:
            self.board[rows[0], cols[0]] = self.user
            return
        except IndexError:
            pass
        
        # --------------- empty corner ----------------------------
        rows, cols = np.where((np.rot90(np.identity(3)).astype(bool) | np.identity(3).astype(bool)) 
                              & (self.board==0))
        try:
            self.board[rows[0], cols[0]] = self.user
            return
        except IndexError:
            pass
        
        # --------------- empty side ----------------------------
        rows, cols = np.where(np.ones((3,3)).astype(bool) 
                              & ~(np.rot90(np.identity(3)).astype(bool) | np.identity(3).astype(bool)) 
                              & (self.board==0))
            
        try:
            self.board[rows[0], cols[0]] = self.user
            return
        except IndexError:
            print("SOMETHING WENT BADLY WRONG")
            pass
        
        return
    
    def get_users_move(self):
        # display the current layout
        print(self.board)

        while True:
            # get user input and update board accordingly
            try:
                move = int(input("Enter your choice (0-9): "))
                assert self.board[move//3, move%3]==0
                return move
            except:
                print("Enter valid input (0-9) that has not already been selected.")
                continue
        
    def run_game(self):
        while not self.game_finished:
            
            if self.user==1:
                # user has made fewer moves, so let them make the move
                
                move = self.get_users_move()

                self.board[move//3, move%3] = 1
                
            else:           
                # make computer move
                self.make_computer_move()
                    
            # check if the new move made either player win
            self.game_finished = self.is_game_finished()
            self.user *= -1
        
        print(self.board)
        if self.winner:
            print("{} won by {}!".format(self.winner, self.how))
        else:
            print("It's a draw!")
            
    def do_games(self):
        log = []
        while not self.game_finished:
            if self.user==1:
                # user has made fewer moves, so let them make the move
                
                move =  np.random.randint(0,9)
                while self.board[move//3, move%3]!=0:
                    move =  np.random.randint(0,9)

                self.board[move//3, move%3] = 1
                
            else:           
                # make computer move
                self.make_computer_move()
                    
            # check if the new move made either player win
            self.game_finished = self.is_game_finished()
            self.user *= -1
            log.append(self.board.copy())
            
        if self.winner==1:
            print("Found one!")
            for item in log:
                print(item)