from model.fix_parser import FIXParser

if __name__ == '__main__':
    parser = FIXParser('FIX42')
    parser.parse_fix_message('8=FIX.4.19=6135=A34=149=EXEC52=20121105-23:24:0656=BANZAI98=0108=3010=003 '
                             '8=FIX.4.19=6135=A34=149=BANZAI52=20121105-23:24:0656=EXEC98=0108=3010=003')
