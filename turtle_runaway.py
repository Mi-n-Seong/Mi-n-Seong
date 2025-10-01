# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random, math, time   # math, time 추가

class RunawayGame:
    def __init__(self, canvas, runner, chaser, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        # Instantiate another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2

    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.time_limit = 180    # 3분 카운트다운
        self.start_time = time.time()
        self.canvas.ontimer(self.step, self.ai_timer_msec)

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())

        # TODO) You can do something here and follows.
        elapsed = time.time() - self.start_time
        time_left = int(self.time_limit - elapsed)
        is_catched = self.is_catched()

        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-320, 300)
        self.drawer.write(f'Time Left: {time_left}s | Is catched? {is_catched}')

        if is_catched:
            self.drawer.setpos(-120, 0)
            self.drawer.write('❌ Caught! Game Over', font=('Arial', 16, 'bold'))
            return
        if time_left <= 0:
            self.drawer.setpos(-150, 0)
            self.drawer.write('✅ Runner Survived! Victory', font=('Arial', 16, 'bold'))
            return

        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    """Runner (직접 조종)"""
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        # 직접 조종이라 AI 없음
        pass

class SmartChaser(turtle.RawTurtle):
    """Chaser (AI, Runner를 추격)"""
    def __init__(self, canvas, step_move=8, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn
        self.penup()

    def run_ai(self, opp_pos, opp_heading):
        dx = opp_pos[0] - self.xcor()
        dy = opp_pos[1] - self.ycor()
        angle = math.degrees(math.atan2(dy, dx))
        self.setheading(angle)
        self.forward(self.step_move)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = ManualMover(screen)    # Runner = 직접 조종
    chaser = SmartChaser(screen)    # Chaser = AI

    game = RunawayGame(screen, runner, chaser)
    game.start()
    screen.mainloop()
