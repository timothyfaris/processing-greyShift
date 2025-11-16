from PIL import Image
import numpy as np

debug = True

img = Image.open("Screenshot 2024-01-18 084423.png")

low = mid = high = 0

redlow = greenlow = bluelow = []
redmid = greenmid = bluemid = []
redhigh = greenhigh = bluehigh = []

redlowSum = greenlowSum = bluelowSum = 0
redmidSum = greenmidSum = bluemidSum = 0
redhighSum = greenhighSum = bluehighSum = 0

# low = 25% B
r1, r2 = 54, 74
# mid = 50% B          These values need to be flexible. Add in an IF statement(s) to try to correct NaN errors.
r3, r4 = 119, 139
# high = 75% B
r5, r6 = 183, 203
""""""
# low
redlowOffset = greenlowOffset = bluelowOffset = 0
# mid
redmidOffset = greenmidOffset = bluemidOffset = 0
# high
redhighOffset = greenhighOffset = bluehighOffset = 0

pixels = np.array(img)

# Low
for i in range(img.width * img.height):
    rl, gl, bl = pixels[i]

    if (r1 <= rl <= r2) and (r1 <= gl <= r2) and (r1 <= bl <= r2):
        low += 1
        redlow.append(rl)
        greenlow.append(gl)
        bluelow.append(bl)

for p in range(low):
    redlowSum += redlow[p]
    greenlowSum += greenlow[p]
    bluelowSum += bluelow[p]

redlowOffset = redlowSum / low - 64
greenlowOffset = greenlowSum / low - 64
bluelowOffset = bluelowSum / low - 64

for i in range(img.width * img.height):
    rl, gl, bl = pixels[i]
    pixels[i] = [round(rl - redlowOffset), round(gl - greenlowOffset), round(bl - bluelowOffset)]

# Mid
for ii in range(img.width * img.height):
    rm, gm, bm = pixels[ii]

    if (r3 <= rm <= r4) and (r3 <= gm <= r4) and (r3 <= bm <= r4):
        mid += 1
        redmid.append(rm)
        greenmid.append(gm)
        bluemid.append(bm)

for pp in range(mid):
    redmidSum += redmid[pp]
    greenmidSum += greenmid[pp]
    bluemidSum += bluemid[pp]

redmidOffset = redmidSum / mid - 129
greenmidOffset = greenmidSum / mid - 129
bluemidOffset = bluemidSum / mid - 129

for ii in range(img.width * img.height):
    rm, gm, bm = pixels[ii]
    pixels[ii] = [round(rm - redmidOffset), round(gm - greenmidOffset), round(bm - bluemidOffset)]

# High
for iii in range(img.width * img.height):
    rh, gh, bh = pixels[iii]

    if (r5 <= rh <= r6) and (r5 <= gh <= r6) and (r5 <= bh <= r6):
        high += 1
        redhigh.append(rh)
        greenhigh.append(gh)
        bluehigh.append(bh)

for ppp in range(high):
    redhighSum += redhigh[ppp]
    greenhighSum += greenhigh[ppp]
    bluehighSum += bluehigh[ppp]

redhighOffset = redhighSum / high - 193
greenhighOffset = greenhighSum / high - 193
bluehighOffset = bluehighSum / high - 193

for iii in range(img.width * img.height):
    rh, gh, bh = pixels[iii]
    pixels[iii] = [round(rh + redhighOffset), round(gh - greenhighOffset), round(bh + bluehighOffset)]

img = Image.fromarray(np.uint8(pixels))

img.show()
