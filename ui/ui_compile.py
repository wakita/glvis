import PyQt5.uic

if True:
    with open('dialog.py', mode='w') as w:
        PyQt5.uic.compileUi('dialog.ui', w)
    with open('echo.py', mode='w') as w:
        PyQt5.uic.compileUi('echo.ui', w)

def compile():
    from pathlib import Path
    for f in Path('.').glob('*.ui'):
        with open(f.stem + '.py', mode='w') as w:
            PyQt5.uic.compileUi(str(f), w)
        print(f)

if __name__ == '__main__':
    compile()
