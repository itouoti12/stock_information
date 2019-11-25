import sys
import itertools


def main(lines):
    # このコードは標準入力と標準出力を用いたサンプルコードです。
    # このコードは好きなように編集・削除してもらって構いません。
    # ---
    # This is a sample code to use stdin and stdout.
    # Edit and remove this code as you like.

    # numList = list(lines)

    # tmplist = []
    # min = int(lines)
    # for value in itertools.permutations(numList, len(numList)):
    #     if(tmplist != value):
    #         target = int("".join(map(str, value)))
    #         print("target is " + str(target))
    #         if(len(str(target)) == len(numList)):
    #             print("a:" + str(len(str(target))))
    #             print("b:" + str(len(numList)))

    #             print(str(target) + " vs " + str(min))
    #             if(target < min):
    #                 min = target

    # print(min)
    numList = list(lines)

    firstMinIndex = 9
    firstMinValue = 9
    for i, v in enumerate(numList):
        print("value :" + str(v))
        if(int(v) != 0 & int(v) < int(firstMinValue)):
            firstMinIndex = i
            firstMinValue = v
            print("firstindex :"+str(firstMinIndex))
            print("firstvalue :"+str(firstMinValue))

    numList.pop(firstMinIndex)
    minList = sorted(numList)

    print(str(firstMinValue)+ "".join(map(str, minList)))


if __name__ == '__main__':
    args = sys.argv
    main(args[1])
