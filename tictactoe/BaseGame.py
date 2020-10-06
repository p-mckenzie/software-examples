import numpy as np

class TicTacToe():
    def __init__(self):
        self.board = np.zeros((3,3), dtype=np.int8)
        self.game_finished = False
        self.user = 1
        
        self.fork = np.zeros((3,3), dtype=bool)
        self.fork[:,0] = 1
        self.fork[0,:] = 1
        
        self.corner = np.zeros((3,3), dtype=bool)
        self.corner[0,0] = 1
        
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
            self.how = 'diagonal'
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
        
        # --------------- block fork ----------------------------
        # diagonal double fork
        if (self.board!=0).sum()==3 and self.board[1,1]==self.user and ((self.board[np.rot90(self.corner, 2) | np.rot90(self.corner, 0)]==-1*self.user).all() 
                    or (self.board[np.rot90(self.corner, 3) | np.rot90(self.corner, 1)]==-1*self.user).all()):
            self.board[1,0] = self.user
            return
        
        # single fork
        for i in range(4):
            if (self.board[np.rot90(self.fork, i)]==self.user*-1).sum()==2 and (self.board[np.rot90(self.fork, i)]==0).sum()==3:
                self.board[np.rot90(self.corner, i)] = self.user
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