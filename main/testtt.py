import sys
import itertools

def main(lines):
    # このコードは標準入力と標準出力を用いたサンプルコードです。
    # このコードは好きなように編集・削除してもらって構いません。
    # ---
    # This is a sample code to use stdin and stdout.
    # Edit and remove this code as you like.

    for i, v in enumerate(lines):
        numList = list(v)

        minNum = int(v)
        for value in itertools.permutations(numList, len(numList)):
          target = int("".join(map(str, value)))
          if(len(str(target)) == len(numList)):
            if(target < minNum):
              minNum = target
        
        print(minNum)


if __name__ == '__main__':
    lines = []
    for l in sys.stdin:
        lines.append(l.rstrip('\r\n'))
    main(lines)
