class ANIMATION:
    def __init__(self, ui, animateID, startpos, endpos, movetype, length, wait, relativemove, command, runcommandat,
                 skiptoscreen, acceleration, permamove, ID):
        self.startpos = startpos
        self.endpos = endpos
        self.trueendpos = 0
        self.movetype = movetype
        self.length = length
        self.acceleration = acceleration
        self.relativemove = relativemove

        self.command = command
        self.runcommandat = runcommandat

        self.ui = ui
        self.ID = ID
        self.animateID = animateID
        self.permamove = permamove

        self.progress = 0
        self.timetracker = 0
        self.wait = wait
        self.skip = skiptoscreen
        self.fadeout = False

        self.onitem = False
        self.bounditems = []

    def gencordlist(self, regenerating=False):
        self.speedlist = [1 for a in range(self.length)]
        speed = 0
        pos = 0
        if self.movetype == 'sin':
            self.speedlist = []
            for p in range(self.length + 1):
                self.speedlist.append(1 - math.cos(math.pi * 2 * ((p + 1) / self.length)))
        elif self.movetype == 'sinin':
            self.speedlist = []
            for p in range(self.length + 1):
                self.speedlist.append(1 - math.cos(math.pi * ((p + 1) / self.length) + math.pi))
        elif self.movetype == 'sinout':
            self.speedlist = []
            for p in range(self.length + 1):
                self.speedlist.append(1 - math.cos(math.pi * ((p + 1) / self.length)))

        for a in range(len(self.speedlist)):
            self.speedlist[a] = (self.speedlist[a] / 2) ** self.acceleration
        self.speedlist = normalizelist(self.speedlist)
        self.cordlist = []
        for a in range(self.length):
            self.cordlist.append((
                                 self.startpos[0] + (self.endpos[0] - self.startpos[0]) * (sum(self.speedlist[:a + 1])),
                                 self.startpos[1] + (self.endpos[1] - self.startpos[1]) * (
                                     sum(self.speedlist[:a + 1]))))
        if (self.skip or type(self.ui.IDs[self.animateID]) == WINDOWEDMENU) and not regenerating:
            self.findonscreen()

    def findonscreen(self):
        scale = self.ui.IDs[self.animateID].scale
        dirscale = self.ui.IDs[self.animateID].dirscale
        scords = self.startpos[:]
        ecords = self.endpos[:]
        start = self.checkonscreen(dirscale, scale, scords)
        end = self.checkonscreen(dirscale, scale, ecords)
        cross = list(self.startpos[:])
        self.fadeout = False
        if end != start:
            if end:
                out = scords
            else:
                out = ecords
            if out[0] < 0:
                cross[0] = -self.ui.IDs[self.animateID].width
            elif out[0] > self.ui.screenw:
                cross[0] = self.ui.screenw / dirscale[0]
            if out[1] < 0:
                cross[1] = -self.ui.IDs[self.animateID].height
            elif out[1] > self.ui.screenh:
                cross[1] = self.ui.screenh / dirscale[1]

            if end:
                self.startpos = cross
            else:
                self.endpos = cross
                self.fadeout = True

            self.gencordlist(True)

    def checkonscreen(self, dirscale, scale, cords):
        return pygame.Rect(0, 0, self.ui.screenw, self.ui.screenh).colliderect(
            pygame.Rect(cords[0], cords[1], self.ui.IDs[self.animateID].width * scale,
                        self.ui.IDs[self.animateID].height * scale))

    def animate(self):
        prev = round(self.timetracker)
        if self.wait in [0, 1]:
            self.timetracker += 1
        self.timetracker += self.ui.deltatime
        new = round(self.timetracker)
        diff = new - prev
        if diff > 0:
            if self.moveframes(diff):
                return True
        return False

    def moveframes(self, frames=1):
        if not self.animateID in self.ui.IDs:
            return True

        self.wait -= frames

        if self.wait == 0 or (self.wait < 0 and self.wait + frames > 0):
            sp, ep = False, False
            if self.startpos == 'current':
                sp = True
                self.startpos = (self.ui.IDs[self.animateID].x, self.ui.IDs[self.animateID].y)
            if self.endpos == 'current':
                ep = True
                self.endpos = (self.ui.IDs[self.animateID].x, self.ui.IDs[self.animateID].y)
            if self.relativemove:
                if (sp and not ep):
                    self.endpos = ((self.startpos[0] + self.endpos[0]), (self.startpos[1] + self.endpos[1]))
                elif (ep and not sp):
                    self.startpos = ((self.startpos[0] + self.endpos[0]), (self.startpos[1] + self.endpos[1]))
            self.trueendpos = self.endpos[:]
            self.gencordlist()

        if self.wait <= 0:
            if self.progress < self.length:
                self.ui.IDs[self.animateID].smartcords(self.cordlist[self.progress][0], self.cordlist[self.progress][1],
                                                       self.permamove)
                if type(self.ui.IDs[self.animateID]) in [TABLE, TEXTBOX, TEXT, SCROLLER, SLIDER, WINDOWEDMENU, MENU]:
                    self.ui.IDs[self.animateID].refreshcords()
                if type(self.ui.IDs[self.animateID]) == WINDOWEDMENU:
                    self.ui.IDs[self.animateID].darken = self.ui.IDs[self.animateID].truedarken * (
                                self.progress / self.length)
                    if self.fadeout: self.ui.IDs[self.animateID].darken = self.ui.IDs[self.animateID].truedarken - \
                                                                          self.ui.IDs[self.animateID].darken

            if self.progress == self.runcommandat or (
                    type(self.runcommandat) == list and self.progress in self.runcommandat):
                self.command()
            self.progress += frames
            if self.progress >= self.length:
                self.progress = self.length
                self.finish()
                return True
        return False

    def finish(self, forcefinish=False):
        if forcefinish:
            while not self.animate():
                pass
        if self.relativemove and self.wait > 0 and self.endpos != 'current':
            if self.startpos == 'current':
                self.startpos = (self.ui.IDs[self.animateID].x, self.ui.IDs[self.animateID].y)
            self.endpos = (self.startpos[0] + self.endpos[0], self.startpos[1] + self.endpos[1])
        self.ui.IDs[self.animateID].smartcords(self.trueendpos[0], self.trueendpos[1], self.permamove)
        if (type(self.ui.IDs[self.animateID]) in [TABLE, TEXTBOX, TEXT, SCROLLER, SLIDER, WINDOWEDMENU,
                                                  MENU]) and self.permamove:
            self.ui.IDs[self.animateID].resetcords()
        if type(self.ui.IDs[self.animateID]) == WINDOWEDMENU:
            self.ui.IDs[self.animateID].darken = self.ui.IDs[self.animateID].truedarken
        if self.progress == self.runcommandat or self.runcommandat == -1 or (
                type(self.runcommandat) == list and self.progress in self.runcommandat):
            self.command()
