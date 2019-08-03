class ViewController():

    def __init__(self, main_view=None):
        self.main_view = main_view
        self.window = main_view(self)
        self.window.show()
        self.path = []
    
    def show_view(self, new_view=None):
        self.path.append(self.window)
        self.window.close()
        self.window = new_view(self)
        self.window.show()
    
    def show_back(self):
        if self.path == []:
            print("Already at root")
            return
        else:
            self.window.close()
            self.window = self.path.pop()
            self.window.show()

Controller = None