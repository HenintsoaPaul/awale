from Box import Box


class Game:

    def __init__(self):
        self._nb_boxes_per_side = 4
        self._ai_boxes = None
        self._player_boxes = None
    
    def init(self):
        ai_boxes = []
        player_boxes = []
        # set ids and degrees
        degree = 0
        for i in range(self._nb_boxes_per_side):
            if (i+1) >= (self._nb_boxes_per_side/2):
                degree = 1
            ai_boxes.append( Box(i, degree) )
            player_boxes.append( Box(i, degree) )
        # set game direction
        for i in range(self._nb_boxes_per_side-1):
            ai_boxes[i].set_next(ai_boxes[i+1])
            player_boxes[i].set_next(player_boxes[i+1])
        ai_boxes[ len(ai_boxes)-1 ].set_next( ai_boxes[0] )
        player_boxes[ len(player_boxes)-1 ].set_next( player_boxes[0] )

        self._ai_boxes = ai_boxes
        self._player_boxes = player_boxes

    def move(self, side: int, id_box: int):
        # id_box [0;3]
        # side: 0 -> AI and 1 -> Player
        boxes = self._ai_boxes
        opponent_boxes = self._player_boxes
        if side == 1:
            boxes = self._player_boxes
            opponent_boxes = self._ai_boxes
        
        # get box, take all of its content
        box = boxes[ id_box ]
        in_hand = box.get_item()
        box.set_item(0)

        # distribute 'in_hand' items
        while in_hand > 0:
            box = box.get_next()
            box.set_item( box.get_item() + 1 )
            in_hand -= 1

        # get item of the ennemy side
        if box.get_degree() == 0:
            id_box_opponent_to_be_taken = (self._nb_boxes_per_side/2) - 1 - box.get_id_box()
            box_opponent_to_be_taken = opponent_boxes[id_box_opponent_to_be_taken]
            if box_opponent_to_be_taken.get_item() > 0:
                #  - RECURSIVE CALL - 
                box.set_item(box_opponent_to_be_taken.get_item() + box.get_item())
                box_opponent_to_be_taken.set_item(0)
                self.move(side, box.get_id_box())

            else:
                isFirstLineNull = True
                for i in range(self._nb_boxes_per_side/2):
                    if opponent_boxes[i].get_item() != 0:
                        isFirstLineNull = False
                        break

                if isFirstLineNull:
                    id_box_opponent_to_be_taken = self._nb_boxes_per_side - 1 + box.get_id_box()
                    box_opponent_to_be_taken = opponent_boxes[id_box_opponent_to_be_taken]
                    if box_opponent_to_be_taken.get_item() > 0:
                        #  - RECURSIVE CALL - 
                        box.set_item(box_opponent_to_be_taken.get_item() + box.get_item())
                        box_opponent_to_be_taken.set_item(0)
                        self.move(side, box.get_id_box())