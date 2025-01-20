  if len(self.selected_cards) >1 and self.selected_cards[1]:

                x = 300 
                y = 200  
                self.selected_cards[0].paint(x, y, show_front=True, is_small=True)
            
            if len(self.selected_cards) > 2 and self.selected_cards[2]:

                x=975
                y=200
                self.selected_cards[1].paint(x,y,show_front=True, is_small = True)

            return  # Stop drawing the rest of the stage while reveal is active