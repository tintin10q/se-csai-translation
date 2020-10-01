import os

os.chdir("C:/Users/DMA/PycharmProjects/se-csai-translation/data/nl-en")  # Select working directory
counter = 0

with open("europarl-v7.nl-en.nl", "r", encoding="utf-8") as f:  # must do with both .en and .nl files
    with open("europarl-v7.nl-en-fixed.nl", "w+", encoding="utf-8") as fixed:  # make sure you save to different files
        while True:
            line = f.readline()
            if line == "":
                break
            line = line.replace('.\n', ' .\n').replace("'", " &apos;").replace('"', ' &quot;').replace(',', ' ,')
            fixed.write(line)
            counter += 1
            if counter % 100000 == 0:
                print("I just did 100k lines")
