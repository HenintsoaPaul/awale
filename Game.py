from copy import deepcopy
from Box import Box


class Game:
    def __init__( self ):
        self._nb_boxes_per_side = 4
        self._ai_boxes = None
        self._player_boxes = None
        self.is_game_over = False
        self.winner = None

    def get_winner(self) -> str :
        if self.winner == None:
            return None
        winner_name = "AI"
        if self.winner == 1:
            winner_name = "Player"
        return winner_name

    def get_nb_boxes_per_side( self ) -> int:
        return int( self._nb_boxes_per_side )

    def init( self ):
        ai_boxes = [ ]
        player_boxes = [ ]
        # set ids and degrees
        degree = 0
        for i in range( self.get_nb_boxes_per_side() ):
            if (i + 1) > (self.get_nb_boxes_per_side() / 2):
                degree = 1
            ai_boxes.append( Box( i, degree ) )
            player_boxes.append( Box( i, degree ) )
        # set game direction
        for i in range( self.get_nb_boxes_per_side() - 1 ):
            ai_boxes[ i ].set_next( ai_boxes[ i + 1 ] )
            player_boxes[ i ].set_next( player_boxes[ i + 1 ] )
        ai_boxes[ len( ai_boxes ) - 1 ].set_next( ai_boxes[ 0 ] )
        player_boxes[ len( player_boxes ) - 1 ].set_next( player_boxes[ 0 ] )

        self._ai_boxes = ai_boxes
        self._player_boxes = player_boxes

    def clone( self ):
        clone = Game()
        clone._ai_boxes = deepcopy( self._ai_boxes )
        clone._player_boxes = deepcopy( self._player_boxes )
        return clone

    def check_game_over( self ) -> bool:
        is_game_over = False
        max_items = 2 * 2 * self.get_nb_boxes_per_side()

        items_in_ai_boxes = 0
        items_in_player_boxes = 0
        for i in range( self.get_nb_boxes_per_side() ):
            items_in_ai_boxes += self._ai_boxes[ i ].get_item()
            items_in_player_boxes += self._player_boxes[ i ].get_item()

        if items_in_ai_boxes == max_items or items_in_player_boxes == max_items:
            is_game_over = True
            self.winner = 1
            if items_in_ai_boxes > items_in_player_boxes:
                self.winner = 0
                
        self.is_game_over = is_game_over
        return is_game_over

    def move( self, side: int, id_box: int, in_hand = 0 ):
        # print ("side: ", side, "id_box: ", id_box, "in_hand: ", in_hand)
        # id_box [0;3]
        # side: 0 -> AI and 1 -> Player
        boxes = self._ai_boxes
        opponent_boxes = self._player_boxes
        if side == 1:
            boxes = self._player_boxes
            opponent_boxes = self._ai_boxes

        # get box, take all of its content
        box = boxes[ id_box ]
        in_hand += box.get_item()
        box.set_item( 0 )

        # distribute 'in_hand' items
        while in_hand > 0:
            box = box.get_next()
            box.set_item( box.get_item() + 1 )
            in_hand -= 1

        # get item on the enemy side
        if box.get_degree() == 0:
            id_box_opponent_to_be_taken = int((self.get_nb_boxes_per_side() / 2) - 1 - box.get_id_box())
            box_opponent_to_be_taken = opponent_boxes[ id_box_opponent_to_be_taken ]
            if box_opponent_to_be_taken.get_item() > 0:
                #  - RECURSIVE CALL - 
                in_hand += box_opponent_to_be_taken.get_item()
                box_opponent_to_be_taken.set_item( 0 )
                self.move( side, box.get_id_box(), in_hand )

            else:
                isFirstLineNull = True
                for i in range( int(self.get_nb_boxes_per_side() / 2) ):
                    if opponent_boxes[ i ].get_item() != 0:
                        isFirstLineNull = False
                        break

                if isFirstLineNull:
                    id_box_opponent_to_be_taken = int(self.get_nb_boxes_per_side() - 2 + box.get_id_box())
                    box_opponent_to_be_taken = opponent_boxes[ id_box_opponent_to_be_taken ]
                    if box_opponent_to_be_taken.get_item() > 0:
                        #  - RECURSIVE CALL - 
                        in_hand += box_opponent_to_be_taken.get_item()
                        box_opponent_to_be_taken.set_item( 0 )
                        self.move( side, box.get_id_box(), in_hand )

        # check if game is over
        self.check_game_over()

    # returns the max/min score that can be got from a specific state
    def minimax( self, side: int, depth: int, toMaximize: bool ) -> int:
        if depth == 0 or self.is_game_over:
            return self.evaluate( side )

        if toMaximize:  # AI's turn
            best_score = float( '-inf' )
            for i in range( self.get_nb_boxes_per_side() ):
                if self._ai_boxes[ i ].get_item() > 0:
                    # clone the Game, then perform the test on the clone 
                    clone = self.clone()
                    clone.move(side, i)
                    score = clone.minimax(0, depth - 1, True)
                    best_score = max(best_score, score)

            return best_score
        else:  # Player's turn
            best_score = float( 'inf' )
            for i in range( self.get_nb_boxes_per_side() ):
                if self._player_boxes[ i ].get_item() > 0:
                    # clone the Game, then perform the test on the clone 
                    clone = self.clone()
                    clone.move(side, i)
                    score = clone.minimax(0, depth - 1, False)
                    best_score = min(best_score, score)

            return best_score

    def evaluate( self, side: int ):
        boxes = self._ai_boxes
        remaining_items = 0
        if side == 1:
            boxes = self._player_boxes
        for i in range( self.get_nb_boxes_per_side() ):
            remaining_items += boxes[ i ].get_item()
        return remaining_items - (self.get_nb_boxes_per_side() * 2)

    # returns the best move for the AI
    def get_ai_move( self ) -> int:
        depth = 5
        max_score = float( '-inf' )
        id_best_box = 0
        # explore all possible moves and get best move
        for i in range(self.get_nb_boxes_per_side()): 
            clone = self.clone()
            clone.move( side=0, id_box=i )
            score = self.minimax( 0, depth, True )
            if score > max_score:
                max_score = score
                id_best_box = i
        return id_best_box
