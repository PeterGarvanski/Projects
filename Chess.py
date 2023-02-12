import re
import math
import sys
import random
import time
import pyfiglet
import pygame
from pygame.locals import *

# Chess class storing all the initialized attributes
class Chess:
    def __init__(self, colour, type, StartingPosition, CurrentPosition, image):
        self.colour = colour
        self._type = type
        self.StartingPosition = StartingPosition
        self._current_position = CurrentPosition
        self._image = pygame.image.load(f"D:/Chess/Images/{image}.png")

    def Rectangle(self, CurrentPosition):
        self.rect = pygame.Rect(self._current_position[0], self._current_position[1], 100, 100)
        return self.rect
    
    @property
    def CurrentPosition(self):
        return self._current_position

    def set_current_position(self, coordinates):
        x , y = coordinates
        self._current_position = (x,y)
    
    @property
    def image(self):
        return self._image
    
    def set_image(self, new_type):
        self._image = pygame.image.load(f"D:/Chess/Images/{new_type}.png")

    @property
    def type(self):
        return self._type

    def set_type(self, new_type):
        self._type = new_type

# Pieces_Obj creates all the objects from the list of pieces using the Chess class assigning each piece attributes
def Pieces_Obj():
    
    # Storing piece names
    PieceNames = [
        "WLRook","WLKnight","WLBishop","WQueen","WKing","WRBishop","WRKnight","WRRook",
        "WAPawn","WBPawn","WCPawn","WDPawn","WEPawn","WFPawn","WGPawn","WHPawn",
        "BLRook","BLKnight","BLBishop","BQueen","BKing","BRBishop","BRKnight","BRRook", 
        "BAPawn","BBPawn","BCPawn","BDPawn","BEPawn","BFPawn","BGPawn","BHPawn"
    ]

    WX = 50
    WY = 800
    WPY = 700
    BX = 50
    BY = 100
    BPY = 200
    WPX = 50
    BPX = 50

    # Empty list to store all the Objects
    obj = []

    # Creates objects and gives them attributes
    for piece in PieceNames:
        matches = re.search(r"([A-Z]){1}(?:[A-Z])?(Rook|Knight|Bishop|Queen|King|Pawn)", piece)
        if str(matches.group(1)) == "W":
            colour = "white"
            if str(matches.group(2)) != "Pawn":
                piece = Chess(colour,(matches.group(2).lower()),(WX,WY),(WX,WY),f"W{matches.group(2)}")
                WX += 100
                obj.append(piece)
            else:
                piece = Chess(colour,"pawn",(WPX,WPY),(WPX,WPY),"WPawn")
                WPX += 100
                obj.append(piece)
        else:
            colour = "black"
            if str(matches.group(2)) != "Pawn":
                piece = Chess(colour,(matches.group(2).lower()),(BX,BY),(BX,BY),f"B{matches.group(2)}")
                BX += 100
                obj.append(piece)
            else:
                piece = Chess(colour,"pawn",(BPX,BPY),(BPX,BPY),"BPawn")
                BPX += 100
                obj.append(piece)
    
    return obj

# Blit_Objects creates, initializes and customizes the display, blits all pieces that are not lost onto the board and lost ones next to the equivelant player
def Blit_Objects(Objects, lost_pieces):
    # Initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((900, 1000))

    # Configuring the window and display size 
    display = pygame.display.set_caption("2-Player Chess")
    icon = pygame.image.load("D:/Chess/Images/icon.png")

    screen.fill((255,255,255))

    # Importing and adjusting the board size
    board = pygame.image.load("D:/Chess/Images/chessboard.png")
    board = pygame.transform.scale(board, (int(board.get_width()), int(board.get_height())))

    # Adjusting and setting the icon
    icon = pygame.transform.scale(icon, (int(icon.get_width()/16), int(icon.get_height()/16)))
    pygame.display.set_icon(icon)
        
    # Setting the board as background and pieces into starting positions
    screen.blit(board, (0, 0))

    for piece in Objects:
        screen.blit(piece.image, piece.CurrentPosition)

    WX = 270
    WY = 42
    BX = 270
    BY = 942

    if len(lost_pieces) != 0:
        for piece in lost_pieces:
            image = pygame.transform.scale(piece.image, (20,20))
            if piece.colour == "white":
                screen.blit(image, (WX,WY))
                WX += 20
            else:
                screen.blit(image, (BX,BY))
                BX += 20

# Select_Piece gets the mouse's position and checks if any piece is in the same position as the click if so it returns the piece
def Select_Piece(list):
    x , y = pygame.mouse.get_pos()
    for piece in list:
        if piece.Rectangle(piece.CurrentPosition).collidepoint(x, y):
            return piece

# Limit_Moves checks the piece type and position and depending on where it is it produces the only available moves to play and returns them as a list
def Limit_Moves(list, coordinates, piece):
    Available_Moves = []
    castling = []
    x , y = piece.CurrentPosition
    
    if piece.type == "pawn":
        for obj in list:
            direction = -100 if piece.colour == "white" else 100
            normal_move = (x, y + direction)
            double_move = (x, y + 2 * direction)
            attack_left = (x - 100, y + direction)
            attack_right = (x + 100, y + direction)

            if piece.CurrentPosition == piece.StartingPosition:
                if obj.CurrentPosition in [attack_left, attack_right] and obj.colour != piece.colour:
                    Available_Moves.extend([normal_move, double_move, obj.CurrentPosition])
                else:
                    Available_Moves.extend([normal_move, double_move])
            
            elif obj.CurrentPosition == normal_move:
                Available_Moves = [attack_left, attack_right]
            
            else:
                if obj.CurrentPosition in [attack_left, attack_right] and obj.colour != piece.colour:
                    Available_Moves.extend([normal_move, obj.CurrentPosition])
                else:
                    Available_Moves.append(normal_move)

    elif piece.type == "rook":
        ranks = [(0,100),(0,-100),(100,0),(-100,0)]
        for a, b in ranks:
            for i in range(1, 9):
                stop = False
                for obj in list:
                    if obj.CurrentPosition == (x + a * i, y + b * i):
                        if piece.colour == obj.colour:
                            stop = True
                            break
                        else:
                            Available_Moves.append((x + a * i, y + b * i))
                            stop = True
                            break
                if stop == True:
                    break
                else:
                    if (x + a * i) <= 750 and (y + b * i) <= 800 and (x + a * i) >= 50 and (y + b * i) >= 100:
                        Available_Moves.append((x + a * i, y + b * i))

    elif piece.type == "bishop":
        diagonals = [(100,100),(-100,-100),(-100,100),(100,-100)]
        for a, b in diagonals:
            for i in range(1, 9):
                stop = False
                for obj in list:
                    if obj.CurrentPosition == (x + a * i, y + b * i):
                        if piece.colour == obj.colour:
                            stop = True
                            break
                        else:
                            Available_Moves.append((x + a * i, y + b * i))
                            stop = True
                            break
                if stop == True:
                    break
                else:
                    if (x + a * i) <= 850 and (y + b * i) <= 750 and (x + a * i) >= 50 and (y + b * i) >= 50:
                        Available_Moves.append((x + a * i, y + b * i))

    elif piece.type == "knight":
        LShape = [
            (x-200,y-100),(x+200,y-100),(x-100,y-200),(x+100,y-200),
            (x-200,y+100),(x+200,y+100),(x-100,y+200),(x+100,y+200)
        ]
        for move in LShape:
            Available_Moves.append(move)
    
    elif piece.type == "king":

        LWcastling = None
        RWcastling = None
        LBcastling = None
        RBcastling = None

        if piece.StartingPosition == piece.CurrentPosition:
            if piece.colour == "white":
                for obj in list:
                    # Check if there are any pieces between the king and rook
                    if obj.CurrentPosition == (150, 800):
                        LWcastling = False
                    elif obj.CurrentPosition == (250, 800):
                        LWcastling = False
                    elif obj.CurrentPosition == (350, 800):
                        LWcastling = False
                
                    if obj.CurrentPosition == (550, 800):
                        RWcastling = False
                    elif obj.CurrentPosition == (650, 800):
                        RWcastling = False
                
                if LWcastling == None:
                    castling.append((x-200, y))
                if RWcastling == None:
                    castling.append((x+200, y))
            else:
                for obj in list:
                    # Check if there are any pieces between the king and rook
                    if obj.CurrentPosition == (150, 100):
                        LBcastling = False
                    elif obj.CurrentPosition == (250, 100):
                        LBcastling = False
                    elif obj.CurrentPosition == (350, 100):
                        LBcastling = False
                
                    if obj.CurrentPosition == (550, 100):
                        RBcastling = False
                    elif obj.CurrentPosition == (650, 100):
                        RBcastling = False
                
                if LBcastling == None:
                    castling.append((x-200, y))
                if RBcastling == None:
                    castling.append((x+200, y))

        Surrounding = [
            (x, y-100), (x, y+100), (x-100, y), (x+100, y),
            (x+100, y+100), (x-100, y-100), (x+100, y-100), (x-100, y+100)
        ]
        for move in Surrounding:
            Available_Moves.append(move)

    elif piece.type == "queen":
        directions = [(100,100),(-100,-100),(-100,100),(100,-100), (100,0),(-100,0),(0,-100),(0,100)]
        for a, b in directions:
            for i in range(1, 9):
                stop = False
                for obj in list:
                    if obj.CurrentPosition == (x + a * i, y + b * i):
                        if piece.colour == obj.colour:
                            stop = True
                            break
                        else:
                            Available_Moves.append((x + a * i, y + b * i))
                            stop = True
                            break
                if stop == True:
                    break
                else:
                    if (x + a * i) <= 850 and (y + b * i) <= 750 and (x + a * i) >= 50 and (y + b * i) >= 50:
                        Available_Moves.append((x + a * i, y + b * i))

    for obj in list:
        new_moves = []
        for move in Available_Moves:
            x, y = move
            if piece.colour != obj.colour or move != obj.CurrentPosition:
                if 50 <= x <= 750 and 100 <= y <= 800:
                    new_moves.append(move)
        Available_Moves = new_moves

    return Available_Moves, castling

# Promotes pawns that reach the other side off the board
def Promotion(piece, new_type):
    if piece.colour == "white":
        new_type = f"W{new_type}"
        piece.set_image(new_type)
        piece.set_type(new_type.strip("W").lower())
    else:
        new_type = f"B{new_type}"
        piece.set_image(new_type)
        piece.set_type(new_type.strip("B").lower())

# Place_Piece takes a list of objects and a piece when clicked it adjusts and stores the mouse coordinates and uses other functions before changing the pieces Current_Position
def Place_Piece(list, piece):
    try:
        X , Y = pygame.mouse.get_pos()

        # Dealing with positioning the X Coordinate
        x_coordinate = round(X / 100) * 100
        if x_coordinate < X:
            x_coordinate -= 50
        else:
            x_coordinate -= 50

        # Dealing with positioning the Y Coordinate
        y_coordinate = 100 * math.ceil(Y / 100)
        if y_coordinate > Y:
            y_coordinate -= 100

        xy_coordinates = int(x_coordinate), int(y_coordinate)
        Available_Moves, castling = Limit_Moves(list, xy_coordinates, piece)

        if len(castling) == 0:
            for move in Available_Moves:
                if xy_coordinates == move:
                    piece.set_current_position(xy_coordinates)

        else:
            for castle in castling:
                if piece.type == "king":
                    if xy_coordinates == castle:
                        piece.set_current_position(xy_coordinates)
                        if xy_coordinates == (250,800):
                            for obj in list:
                                if obj.colour == "white" and obj.type == "rook":
                                    if obj.StartingPosition == (50,800):
                                        obj.set_current_position((350,800))
                        elif xy_coordinates == (650,800):
                            for obj in list:
                                if obj.colour == "white" and obj.type == "rook":
                                    if obj.StartingPosition == (750,800):
                                        obj.set_current_position((550,800))
                        elif xy_coordinates == (250,100):
                            for obj in list:
                                if obj.colour == "black" and obj.type == "rook":
                                    if obj.StartingPosition == (50,100):
                                        obj.set_current_position((350,100))
                        elif xy_coordinates == (650,100):
                            for obj in list:
                                if obj.colour == "black" and obj.type == "rook":
                                    if obj.StartingPosition == (750,100):
                                        obj.set_current_position((550,100))
                    else:
                        for move in Available_Moves:
                            if xy_coordinates == move:
                                piece.set_current_position(xy_coordinates)
                else:
                    for move in Available_Moves:
                        if xy_coordinates == move:
                            piece.set_current_position(xy_coordinates)

        a , b = piece.CurrentPosition
        new_type = "Queen"

        if piece.type == "pawn":
            if b == 100 or b == 800:
                Promotion(piece, new_type)

    except AttributeError:
        pass

# Capture function takes a list and a piece checks if the piece collides with other objects in the list and returns the object if collided
def Capture(list, piece):
    try:
        list.remove(piece)
                    
        for i in list:
            if piece.Rectangle(piece.CurrentPosition).collidepoint(i.CurrentPosition):
                list.remove(i)
                list.append(piece)
                return i
            else:
                pass            
        
        list.append(piece)

    except ValueError:
        pass

# Main Game loop
def main():
    welcome = pyfiglet.figlet_format("Welcome to", font = "big")
    chess = pyfiglet.figlet_format("2 - Player Chess", font = "big")
    print(welcome)
    print(chess)
    print("Instructions:\n - To select a piece: Left click on the piece you wish to select.\n - To place a piece: Right click on a tile where you wish to place the piece.\n - To perform a checkmate simply capture the oppoments king.")
    print("\nRules:\n - In order to win the game you must perform a checkmate or win by time.\n - A turn by turn system has been implemented to assure alternating turns.\n - If you misplace a piece into a illegal position your move will not be processed and your turn shall end.")
    _ = input("\nIf you have undertood everything so far and wish to continue please press 'ENTER': ")
    if _ == "":
        print("\nGreat let's choose who plays white and who plays black now!")
        player1 = input("\nMay the first player enter their name: ").capitalize()
        player2 = input("May the second player enter their name: ").capitalize()

        player = random.choice([player1, player2])

        print(f"\n{player} has been randomly selected to play white!")
        if player == player1:
            print(f"Therefore {player2} has been selected to play with black.")
        else:
            print(f"Therefore {player1} has been selected to play with black.")
        
        while True:
            t = input("\nFinally, enter the amount of time, in minutes, you would like to play for: ")
            try:
                t = int(t) * 60
                break
            except ValueError:
                print("Please enter a integer!")
                pass

        print("\nHave Fun!")
        time.sleep(2)

    else:
        sys.exit("\nYou have quit the game!")
    
    # Initializing pygame
    pygame.init()
    screen = pygame.display.set_mode((900, 1000))

    # Converts all pieces into objects
    # Empty list and variables to store and moderate pieces
    
    Objects = Pieces_Obj()

    White = []
    Black = []
    
    running = True

    LEFT = 1
    RIGHT = 3
    
    lost_pieces = []

    white = True

    white_timer = t
    black_timer = t

    won = ""

    while running:
        start = time.perf_counter()

        # Spawns all the pieces in the current position after every iteration of the while loop
        Blit_Objects(Objects, lost_pieces)

        # Checking for any occuring events
        for event in pygame.event.get():
            # Allowing users to close the window
            if event.type == QUIT:
                running = False
            # Allows the user to select a piece
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    selected_piece = Select_Piece(Objects)
            # Allows the user to place the selected piece
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                # Implements a turn system
                if white == True:
                    if selected_piece.colour == "white":
                        Place_Piece(Objects, selected_piece)
                        white = False
                    else:
                        pass
                else:
                    if selected_piece.colour == "black":
                        Place_Piece(Objects, selected_piece)
                        white = True
                    else:
                        pass
                
                # Checks for a capture, if there is a capture, stores thhe piece in a list
                lost = Capture(Objects, selected_piece)
                if lost:
                    lost_pieces.append(lost)

        stop = time.perf_counter()
        
        if white == False:
            white_timer -= (stop - start)
        else:
            black_timer -= (stop - start)
        
        Wminutes, Wseconds = divmod(int(white_timer), 60)
        f = pygame.font.Font(None, 40)
        Wtimer = f.render(f"{Wminutes}:{Wseconds:02d}", True, (0, 0, 0))
        screen.blit(Wtimer, (680, 42))

        Bminutes, Bseconds = divmod(int(black_timer), 60)
        f = pygame.font.Font(None, 40)
        Btimer = f.render(f"{Bminutes}:{Bseconds:02d}", True, (0, 0, 0))
        screen.blit(Btimer, (680, 940))
        
        pygame.display.update()

        won_timer = None
        won_checkmate = None

        if white_timer <= 0:
            running = False
            won = "white timer"
        elif black_timer <= 0:
            running = False
            won = "black timer"
        
        for obj in lost_pieces:
            if obj.type == "king":
                running = False
                if obj.colour == "white":
                    won = "black checkmate"
                else:
                    won = "white checkmate"
    
    colour , condition = won.split(" ")
    wining = pyfiglet.figlet_format(f"{colour.capitalize()} has won by {condition}!", font = "big")
    print(wining)
    print("Created by Peter Garvanski!")

pygame.quit()

if __name__ == "__main__":
    main()