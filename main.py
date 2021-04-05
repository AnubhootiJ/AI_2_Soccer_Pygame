import pygame
import random
import math


class RedTeam():
    def __init__(self, rows, cols, screen, bWidth, bHeight, goal_box=False):
        self.rows = rows
        self.cols = cols
        self.legalCols = cols//2 - 1
        self.screen = screen
        self.redPlayer = pygame.image.load('RedP_mod.png')
        self.pos_x = None
        self.pos_y = None
        self.bWidth = bWidth
        self.bHeight = bHeight
        self.goal_box = goal_box


    def drawAgent(self):
        self.screen.blit(self.redPlayer, (self.pos_x-self.bWidth/2, self.pos_y-self.bHeight/2))

    def updatePosition(self):
        if self.goal_box:
            self.pos_x = random.randint(3, 14)
            self.pos_y = random.randint(1, 4)
        else:
            self.pos_x = random.randint(1, self.rows-2)
            self.pos_y = random.randint(5, self.legalCols)
        self.pos_x = self.pos_x* self.bWidth
        self.pos_y = self.pos_y* self.bHeight
        self.pos_x = (2 * self.pos_x+self.bWidth)/2
        self.pos_y = (2 * self.pos_y+self.bHeight)/2
        return self.pos_x, self.pos_y

    def getPosition(self):
        return self.pos_x, self.pos_y


class BlueTeam():
    def __init__(self, rows, cols, screen, bWidth, bHeight, is_kicker=False, goal_box=False):
        self.rows = rows
        self.cols = cols
        self.legalCols = cols//2 - 1
        self.screen = screen
        self.bluePlayer = pygame.image.load('BlueP_mod.png')
        self.pos_x = None
        self.pos_y = None
        self.is_kicker = is_kicker
        self.bWidth = bWidth
        self.bHeight = bHeight
        self.goal_box = goal_box

    def drawAgent(self):
        self.screen.blit(self.bluePlayer, (self.pos_x-self.bWidth/2, self.pos_y-self.bHeight/2))

    def updatePosition(self):
        if self.is_kicker:
            self.pos_x = self.rows//2
            self.pos_y = self.legalCols + 1
        elif self.goal_box:
            self.pos_x = random.randint(3, 14)
            self.pos_y = random.randint(1, 4)
        else:
            self.pos_x = random.randint(1, self.rows-2)
            self.pos_y = random.randint(5, self.legalCols)

        self.pos_x = self.pos_x* self.bWidth
        self.pos_y = self.pos_y* self.bHeight
        self.pos_x = (2 * self.pos_x + self.bWidth) / 2
        self.pos_y = (2 * self.pos_y + self.bHeight) / 2
        return self.pos_x, self.pos_y

    def getPosition(self):
        return self.pos_x, self.pos_y


class Ball():
    def __init__(self, rows, cols, screen, bWidth, bHeight):
        self.pos_x = rows//2
        self.pos_y = cols//2 - 1
        self.screen = screen
        self.bWidth = bWidth
        self.bHeight = bHeight
        self.ball_img = pygame.image.load('ball_mod.png')
        self.index = 0

    def checkBallPath(self, x, final_x, final_y):
        if x<0 and (final_x, final_y) <= (self.pos_x, self.pos_y) <= (final_x + self.bWidth/2, final_y + self.bHeight/2):
            return False
        elif x > 0 and (final_x-self.bWidth/2, final_y-self.bHeight/2) <= (self.pos_x, self.pos_y) <= (final_x, final_y):
            return False
        elif final_x<0 or final_y<0:
            return False
        else:
            return True

    def move(self, passDist):
        if self.index < len(passDist):
            final_x, final_y = passDist[self.index]
            x = self.pos_x - final_x
            y = self.pos_y - final_y
            if x!=0:
                slope = y/x
                if slope!=0:
                    const = self.pos_y - slope * self.pos_x
                    if y<0 and self.checkBallPath(x, final_x, final_y):
                        self.pos_y += 0.5
                        self.pos_x = (self.pos_y - const)/slope
                        self.drawBall()
                    elif y>0 and self.checkBallPath(x, final_x, final_y):
                        self.pos_y -= 0.5
                        self.pos_x = (self.pos_y - const) / slope
                        self.drawBall()
                    else:
                        self.index+=1
                else:
                    if x<0 and not (final_x-self.bWidth/2 <= self.pos_x <= final_x+self.bWidth/2):
                        self.pos_x += 0.5
                        self.drawBall()
                    elif x>0 and not final_x-self.bWidth/2 <= self.pos_x <= final_x+self.bWidth/2:
                        self.pos_x -= 0.5
                        self.drawBall()
                    else:
                        self.index += 1
            else:
                if y<0 and not (final_y-self.bHeight/2 <= self.pos_y <= final_y+self.bHeight/2):
                    self.pos_y+=0.5
                    self.drawBall()
                elif y>0 and not (final_y-self.bHeight/2 <= self.pos_y <= final_y+self.bHeight/2):
                    self.pos_y-=0.5
                    self.drawBall()
                else:
                    self.index+=1

    def updateBallPos(self):
        self.pos_x = self.pos_x*self.bWidth
        self.pos_y = self.pos_y*self.bHeight
        self.pos_x = self.pos_x + self.bWidth / 2
        self.pos_y = self.pos_y + self.bHeight / 2
        return self.pos_x, self.pos_y

    def getBallPos(self):
        return self.pos_x, self.pos_y

    def drawBall(self):
        self.screen.blit(self.ball_img, (self.pos_x-self.bWidth/2+4, self.pos_y-self.bHeight/2+2))


class Ground():
    def __init__(self, rows, cols, Width, Height, bWidth, bHeight, screen):
        self.rows = rows
        self.cols = cols
        self.width = Width
        self.height = Height
        self.bWidth = bWidth
        self.bHeight = bHeight
        self.screen = screen
        self.players = []
        self.positions = []
        self.goalPost_x = 9 * self.bWidth + self.bWidth/2
        self.goalPost_y = 0 * self.bHeight + self.bHeight/2
        self.ball = Ball(self.rows, self.cols, self.screen, self.bWidth, self.bHeight)
        self.kicker = BlueTeam(self.rows, self.cols, self.screen, self.bWidth, self.bHeight, True)
        self.b1 = BlueTeam(self.rows, self.cols, self.screen, self.bWidth, self.bHeight, False, True)
        self.b2 = BlueTeam(self.rows, self.cols, self.screen, self.bWidth, self.bHeight)
        self.b3 = BlueTeam(self.rows, self.cols, self.screen, self.bWidth, self.bHeight)
        self.r1 = RedTeam(self.rows, self.cols, self.screen, self.bWidth, self.bHeight, True)
        self.r2 = RedTeam(self.rows, self.cols, self.screen, self.bWidth, self.bHeight)
        self.r3 = RedTeam(self.rows, self.cols, self.screen, self.bWidth, self.bHeight)
        self.agent = self.kicker

    def drawGrid(self):
        for x in range(self.rows):
            x = x * self.bWidth
            pygame.draw.line(self.screen, (255, 255, 255), (x, 0), (x, self.height), 2)
        for y in range(self.cols):
            y = y*self.bHeight
            pygame.draw.line(self.screen, (255, 255, 255), (0, y), (self.width, y), 2)

    def checkPos(self, x, y):
        for pos in self.positions:
            if [x, y] == pos:
                return False
        if [x, y] == self.ball.getBallPos():
            return False
        return True

    def getStaticPosition(self):
        self.players = [self.kicker, self.b1, self.b2, self.b3, self.r1, self.r2, self.r3]
        for player in self.players:
            x, y = player.updatePosition()
            while not self.checkPos(x, y):
                x, y = player.updatePosition()
            self.positions.append([x, y])
        self.ball.updateBallPos()

    def drawAgent(self):
        for player in self.players:
            player.drawAgent()
        self.ball.drawBall()

    def checkRed(self, x, y, destx, desty):
        x1 = x-destx
        y1 = y-desty

        for i in range(4,7):
            redx, redy = self.players[i].getPosition()
            if x1 != 0:
                slope = y1 / x1
                const = y - slope * x
                val = slope * redx + const
                if y1!=0:
                    valx = (redy - const)/slope
                    if (redx-self.bWidth/2, redy-self.bHeight/2) <= (valx, val) <= (redx+self.bWidth/2, redy+self.bHeight/2):
                        if (x1>0 and destx<=redx<=x) or (x1<0 and x<=redx<=destx):
                            if (y1>0 and desty<=redy<=y) or (y1<0 and y<=redy<=desty):
                                return False
                elif y1==0 and (y-self.bHeight/2 <=redy <= y+self.bHeight/2):
                    if x1>0 and destx<=redx<=x:
                        return False
                    elif x1<0 and x<=redx<=destx:
                        return False
                    else:
                        return True
            elif x1 == 0 and (x-self.bWidth/2 <=redx <= x+self.bWidth/2):
                if y1>0 and desty <= redy <= y:
                    return False
                elif y1<0 and y <= redy <= desty:
                    return False
                else:
                    return True
            else:
                return True
        return True

    def play(self):
        pl = True
        text = []
        blue = [1, 2, 3]
        passDist = []
        while pl:
            comb = []
            if self.agent != self.players[0] :
                play_x, play_y = self.agent.getPosition()
                fin_dist = math.sqrt((play_x - self.goalPost_x) ** 2 + (play_y - self.goalPost_y) ** 2)
                if self.checkRed(play_x, play_y, self.goalPost_x, self.goalPost_y):
                    comb.append([fin_dist,'Y', 'G'])
                else:
                    comb.append([fin_dist, 'N', 'G'])

            for i in range(1, 4):
                if self.players[i] != self.agent and i in blue:
                    agent_x, agent_y = self.agent.getPosition()
                    if self.players[i].is_kicker:
                        play_x, play_y = self.ball.getBallPos()
                    else:
                        play_x, play_y = self.players[i].getPosition()
                    dist = math.sqrt((play_x - agent_x)**2 + (play_y - agent_y)**2)
                    fin_dist = dist + math.sqrt((play_x - self.goalPost_x) ** 2 + (play_y - self.goalPost_y) ** 2)
                    if self.checkRed(agent_x, agent_y, play_x, play_y):
                        comb.append([fin_dist, 'Y', i])
                    else:
                        comb.append([fin_dist, 'N', i])

            text.append(comb)
            comb.sort(key = lambda x: x[0])
            flag = 0

            for i in range(len(comb)):
                if comb[i][1] == 'Y':
                    minPlayer = comb[i]
                    flag = 1
                    break

            if flag == 0:
                text.append("NP")
                break

            if minPlayer[2] == 'G':
                passDist.append([self.goalPost_x, self.goalPost_y])
                text.append("F")
                pl = False
            else:
                player = minPlayer[2]
                blue.remove(player)
                self.agent = self.players[player]
                passDist.append(self.agent.getPosition())
        return self.ball, passDist, text


def main():
    gwidth = 570
    gheight = 726
    bWidth = 30
    bHeight = 33
    rows = gwidth//bWidth
    cols = gheight//bHeight

    white = (255, 255, 255)
    black = (0, 0, 0)

    width = gwidth + 400
    pygame.init()
    win = pygame.display.set_mode((width, gheight))

    ground = Ground(rows, cols, gwidth, gheight, bWidth, bHeight, win)
    ground.getStaticPosition()
    ball, passDist, gtext = ground.play()
    background = pygame.image.load('AI2_Assignment1_T3_2021.png')

    font = pygame.font.Font('freesansbold.ttf', 32)
    Title = font.render("Let's Play Soccer", True, white, black)

    titleRect = Title.get_rect()
    titleRect.center = (gwidth + 200, 30)

    printText = []
    lp = 1
    for t in gtext:
        if t == 'F':
            st = 'Game Finished Successfully'
            printText.append(st)
        elif t == 'NP':
            st = "Blue team can't win"
            printText.append(st)
        else:
            s = "Round " + str(lp)
            printText.append(s)
            lp += 1
            for gt in t:
                st1 = "Path Cost = "+ str(round(gt[0],2)) +","
                if gt[1] == 'Y':
                    if gt[2] != 'G':
                        st2 = 'possible to reach to Player '+ str(gt[2])
                    else:
                        st2 = 'reached to goal'
                else:
                    if gt[2] != 'G':
                        st2 = 'not Possible to reach to Player '+ str(gt[2])
                    else:
                        st2 = "can't reach goal yet!"
                printText.append(st1)
                printText.append(st2)

    flag = True
    while flag:
        win.fill(black)
        win.blit(background, (0, 0))

        #ground.drawGrid()
        ground.drawAgent()
        win.blit(Title, titleRect)

        start = 80
        add = 30
        for tx in printText:
            start+=add
            font = pygame.font.Font('freesansbold.ttf', 20)
            text = font.render(tx, True, white, black)
            textRect = text.get_rect()
            textRect.center = (gwidth + 200, start)
            win.blit(text, textRect)

        ball.move(passDist)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False

        pygame.display.update()

if __name__ == "__main__":
    main()