import Common.WindowOperations as WO
import Common.ImageDetectionOperations as IDO
import Common.MovementOperations as MO
import random
import time
import Common.FileUnpacker as FU


def DecisionController(player, monsters, playerMap):
    """
    Controls what decision the player should make

    :param target: a tuple (x,y)
    :param player: a tuple (x,y)
    """
    print('Decision Start')
    Movement(playerMap)

    if len(monsters) > 0:
        Fire(player, monsters)
    else:
        UpOrDown(playerMap)


    print('Decision End')


def UpOrDown(player):
    # top level
    if player[1] < 95:
        MO.DoubleKeyPress('alt', 'down', random.uniform(0.15, 0.3))

    # middle Level
    if 95 < player[1] < 117:
        r = random.randrange(0,2)
        if r == 0:
            MO.DoubleKeyPress('alt', 'down', random.uniform(0.15, 0.3))
        else:
            MO.DoubleKeyPress('alt', 'up', random.uniform(0.25, 0.35))
            time.sleep(random.uniform(0.07, 0.11))
            MO.DoubleKeyPress('alt', 'up', random.uniform(0.15, 0.3))

    # Bot Level
    if 117 < player[1]:
        MO.DoubleKeyPress('alt', 'up', random.uniform(0.15, 0.3))
        time.sleep(random.uniform(0.07, 0.11))
        MO.DoubleKeyPress('alt', 'up', random.uniform(0.15, 0.3))

    time.sleep(random.uniform(1.3, 1.6))


def Movement(player):
    """
    Controls the movement of the player
    Still needs some work

    :param target: a tuple (x,y)
    :param player: a tuple (x,y)
    """

    print('Move Start')

    target = 86
    print(player[0])

    xDist = abs(player[0] - target)
    xTime = (xDist / 294) + 0.1
    time.sleep(0.1)
    if player[0] - target > 0:
        MO.KeyPress('left', xTime)
    if player[0] - target < 0:
        MO.KeyPress('right', xTime)
    print('Move End')


def Fire(player, monster):
    """
    Controls the attacking of the player

    :param target: a tuple (x,y)
    :param player: a tuple (x,y)
    """

    direction = 0
    for p in monster:
        direction += (p[0] - player[0])

    print(direction)

    print('Fire Start')
    if direction < 0:
        MO.KeyPress('left', random.uniform(0.08, 0.22))
    else:
        MO.KeyPress('right', random.uniform(0.08, 0.22))

    MO.KeyPress('q', random.uniform(0.15, 0.27))

    print('Fire End')


def CheckHealthAndMana(im, x, y):
    """
    Will use a mana or health potion if health or mana drops too low

    :param im: numpy image
    :param x: length of window
    :param y: height of window
    """
    # two options
    # - check for gray pixels in a known location
    # - template match for transition between gray and mp / hp

    life = im[1154][1010]
    mana = im[1170][936]

    # low life or low mana
    if 90 < life[0] < 120 or 100 < mana[0] < 110 and 95 < mana[1] < 105:
        MO.KeyPress('a', random.uniform(0.8, 1.3))


def CheckForRopeStick():
    print('stuck on rope')
    MO.DoubleKeyPress('left', 'alt', random.uniform(0.2, 0.4))


def main(player, playerClass, map):
    """
    Starts the farming loop

    :param player: numpy image of the player to be found
    :param map: The name of the map the player is on
    """

    data, im1, im2 = FU.Unpack(map)

    ROI = [data['ROI'][1]['y'], data['ROI'][3]['y1'], data['ROI'][0]['x'], data['ROI'][2]['x1']]

    timeKeeping = False
    xa, ya, x1a, y1a = WO.GetWindowPos('MapleStory')
    count = 0
    # height . width
    # ROI = [0, 158, 0, 175]
    pastPos = (0, 0)

    while 1:
        a = time.perf_counter()
        im, x, y, x1, y1 = WO.GetWindowScreenshot('MapleStory', xa, ya, x1a, y1a)

        b = time.perf_counter()
        if timeKeeping:
            print('Screenshot: ' + str((b - a)))

        if im is not None:
            a = time.perf_counter()
            miniMapRoi = im[ROI[0]:ROI[1], ROI[2]:ROI[3]]
            monsterLoc, w, h = IDO.LocateTemplate(im, 'Resources/Maps/DarkEreve/Bird.png', 0.75, True, 150)
            monsterLocFlip, w, h = IDO.LocateTemplate(im, 'Resources/Maps/DarkEreve/BirdFlip.png', 0.75, True, 150)
            playerMap, w1, h1 = IDO.LocateTemplate(miniMapRoi, 'Resources/Player/MapIcon.png', 0.8, False)
            playerLoc, w1, h1 = IDO.LocateTemplate(im, 'Resources/Player/TryKillBoss.png', 0.8, False)
            b = time.perf_counter()

            if timeKeeping:
                print('Template Match: ' + str((b - a)))

            for cords in monsterLocFlip:
                monsterLoc.append(cords)

            if len(monsterLoc) > 0:
                img = IDO.DrawImages(im, monsterLoc, w, h)

            if playerLoc and len(monsterLoc) > 0:
                playerLocList = [playerLoc]  # Todo: Fix this - create a player list because of how code elsewhere works
                img = IDO.DrawImages(img, playerLocList, w1, h1)


            monsters = []

            if playerLoc:
                # find closest baddie
                for i, pts in enumerate(monsterLoc):
                    if pts[1] - 100 < playerLoc[1] < pts[1] + 100:
                        monsters.append(pts)

                img = IDO.DrawLines(img, playerLoc, monsterLoc)
                IDO.DisplayImage(img, 'resize', 800, 600)

                DecisionController(playerLoc, monsters, playerMap)

            CheckHealthAndMana(im, x - x1, y - y1)

            if pastPos == playerLoc:
                CheckForRopeStick()

            count += 1

            # Cool down skill One
            if count % 40 == 0:
                MO.KeyPress('e', random.uniform(0.13, 0.21))

            # Buff skills macro
            if count % 80 == 0:
                MO.KeyPress('r', random.uniform(0.13, 0.21))
                time.sleep(2)

            # Big cooldown
            if count % 75 == 0:
                MO.KeyPress('2', random.uniform(0.13, 0.21))

            if count % 130 == 0:
                MO.KeyPress('3', random.uniform(0.13, 0.21))

            if count % 140 == 0:
                MO.KeyPress('1', random.uniform(0.13, 0.21))

            pastPos = playerLoc


if __name__ == '__main__':
    main()