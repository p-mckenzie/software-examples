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
        
    def make_computer_move(self):
        # --------------- win or block ----------------------------
        for i in range(3):
            # check vertical
            if abs(self.board[:,i].sum())==2 and np.abs(self.board[:,i]).sum()==2:
                self.board[:,i] = np.where(self.board[:,i]==0, self.user, self.board[:,i])
                return
                
            elif abs(self.board[i,:].sum())==2 and np.abs(self.board[i,:]).sum()==2:
                self.board[i,:] = np.where(self.board[i,:]==0, self.user, self.board[i,:])
                return
                
        # check diagonal
        if abs((self.board * np.identity(3)).sum())==2  and (np.abs(self.board) * np.identity(3)).sum()==2:
            self.board = np.where((np.identity(3)==1) & (self.board==0), self.user, self.board)
            return
        elif abs((self.board * np.identity(3)[::-1]).sum())==2  and (np.abs(self.board) * np.identity(3)[::-1]).sum()==2:
            self.board = np.where((np.identity(3)[::-1]==1) & (self.board==0), self.user, self.board)
            return
        
        # --------------- fork or block fork ----------------------------
        for i in range(4):
            if (np.all(self.board[np.rot90(self.corner,i)]==0) and
                  np.all(self.board[np.rot90(self.space,i)]==0) and
                 (np.all(self.board[np.rot90(self.fork,i)]==-1) or np.all(self.board[np.rot90(self.fork,i)]==1))):
                self.board = np.where(np.rot90(self.corner,i), self.user, self.board)
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