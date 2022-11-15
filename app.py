#!/usr/bin/env python3

from idlelib.tooltip import Hovertip
from yaml.loader import SafeLoader
import tkinter as tk
import webbrowser
import importlib
import threading
import yaml
import re

class MyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.homepage = HomePage(self)
        # self.configurepage = ConfigurePage(self)
        # self.aboutpage = AboutPage(self)

        # Set window size
        self.HEIGHT = 500
        self.WIDTH = 600

        # window title
        self.title('IP Analyzer Tool')

        # gets current directory for icon
        # path = Path(__file__).parent.absolute()
        # icon_path = f'{path}\icon.ico'
        # self.iconbitmap(icon_path)

        # Icon base64
        self.icon_base64 = """
        iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAYAAAD0eNT6AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAACAASURBVHic7d13mF1Vof7xd+3TZyYz6QlpkEKoUkIPUgTpSGhBEQslIiCgV2leQPHqVbkoWO+9IE1Q4dJBEAsdpAbpICYQSEKENJKpp+71+yPgL0DKlHPO2vus7+d5eB5KMuedsGef96y9ihGA6rPWzJz/8q6h0f7G2F1kNUXSUEktrqOtrueV0a4jfFAga4KwolSlPUhUXlZGv71j+3H/6zoW0IiM6wBAI9nT3p8csWD4l6zM1yVNcZ1nfSJXANYgSFWKprl4Y/vI8qwHJk7Mu84DNAoKAFAlMxc+v4utJK6SsZu4ztJbcSgA7zOpctG0lr7y++3HX+46C9AIAtcBgEZwxPwX/82GwYNxevOPG1tKpu2y7K8+9diCm11nARoBBQAYoCPffPFsI10sKeU6S6OzMgrbc4d/6rGF97vOAsQdBQAYgJnzXzhZRj90ncM3YXt2z0MeX3Ct6xxAnFEAgH464o2XtrUyF7vO4auwPfu5Q2a/OdN1DiCuKABAP5mE/YWkrOscvrLWyHamr5S13MeAfuAHB+iHIxa8eISsprvO4buwkGr51FMLL3SdA4gjlgECfXTi7Nmp5SOzL0na2HWWgYrTMsC1CVK2lDV26I2fGNnpOgsQJ4wAAH20fFTuJDXAm3+jCEsmlW8qXuE6BxA3jAAAfXDYwleGJcLwFcmOcJ2lGhphBECSgoQNs4O6pty400bzXGcB4oIRAKC3rDWJsHJFo7z5N5KwYoJCMfMYEwKB3uOHBeilmQtfPEPSDNc5sGaV7tSoGU8sutV1DiAuKABALxwx/+VDrTX/6ToH1q2yMn3IjKfmf891DiAOKADAesx844WDjMLrxVa/kWdlVFmeO3fGkwt+4DoLEHUUAGAdZs5/6VgbmFslZVxnQe9YGZVXZM859PEFl7rOAkQZqwCANTh23rxsZ7L7Qll7uusstdQoqwDWJmgpvp5s6d7l1q2nLHadBYgaRgCAD5n55gv7dCa6nm70N38fhJ3pSaXlLfMPeWLBWa6zAFHDCADwnsPfeHlaIgi/b6X9XGepl0YfAVhdkCsuVa5w+u93mHid6yxAFFAA4LWZC14aaq39jKTjJG3vOk+9+VQA3mcy5S6TLd6ZSOrc27af8JrrPIArFAA0tGPnzcu2p9qHp8rBoNAEw6zRMFmNluz2MtpF0mby+FGYjwXgX4xkUuV8kKq8qVQ4W9bON0ktTCh4sxQWFidSwZzbtp24wnVMoFYoAGgoB8yZk2nOFveSDWdIwb6S3VAev8Gvj9cFYH2MFCRtyWRLc5QsX1cKCz+7e+eN213HAqqFAoCGcOLs2al3R+SOs8b+h6RRrvPEBQWgDxKhTTQX/xhkS59lZACNgAKA2Ju54Pk9rE1cJdmJrrPEDQWg74KULam1+xu/337Dn7vOAgwEQ6OItSMXvDjL2uDPvPmjXsKSSYXLmn526OMLb3CdBRgICgBi68g3X/qmrH4lKe06C3xjVFqZnTnj0QV/cp0E6C8KAGJp5oIXDpOxHPoCp8oduX0PeXz+Ja5zAP1BAUDsHLHg5Y2tNdeK6xcRUOlo+uqhT765t+scQF9xA0XsGBv+UFKz6xyAJCmUCfPJq13HAPqKAoBYmbngpR0lHeY6B7C6Sk9m3GFPv/kl1zmAvqAAIFZCa78qlq8igsr51DmuMwB9QQFAbJw4e3bKSAe4zgGsSdidnPip2YuaXOcAeosCgNhYPiK3u6QhrnMAaxQGJrDlL7uOAfQWBQCxYaQdXGcA1sVWDKsBEBsUAMSGNeFGrjMA62LDgB0pERsUAMSIaXWdAFgXYw1zABAbFADEh1HSdQRgnSqWaxSxQQEAAMBDFAAAADxEAQAAwEMUAAAAPEQBAADAQxQAAAA8RAEAAMBDFAAAADxEAQAAwEMUAAAAPNTrbSuttbmO7sInA2Om21AbyZjhtQwGfNhFHQs/9nKx23UMYK3aUsGYN99eucx1DvglkDqNMYuChL2nOaVL2tralvfm9623AKzsLu4cWHtmV3dxPyPTbK0kI0l2gJGBvmk2DFgh8oJyJRzqOgS8M1TSBJW1c09B581/p/2tdDLxrdHDmq9c129a6x11ZT4/paOrcHNg7aOSDrdSc7UTAwCA6iqVK2O78sUrFixuX7BwSccn1vbr1lgAOjvz+wUV85Skw/Xe530AABAfxVJlXKlUuXfR0pXfXdN//0gB6OjOn2aNuUvS4JqnAwAANRNaa3oK4XmLlnbc8OH/9oEC0NFdOFzW/ERSom7pAABATfUUyjMXLem8ZPV/968C0NlZ3MZYXSOWBgIA0HB6iqWv/XNxx5Hv/3MgSdZaY439Hyb6AQDQuIph5WprbSC9VwA6e4ozJe3sNBUAAKipcsU2L1redaH0/nC/1bedJgIAAHVRLoanSlLQ0VHYQtLmjvMAAIA6KIeV7D8XrzwwsIFmuA4DAADqp2ISpwbGmL1cBwEAAPUTVio7BrJ2E9dBAABA/YRWbYGkYa6DAACA+qmEYTKQlHMdBAAA1Be7/gEA4CEKAAAAHqIAAADgIQoAAAAeogAAAOAhCgAAAB6iAAAA4CEKAAAAHqIAAADgIQoAAAAeogAAAOAhCgAAAB6iAAAA4CEKAAAAHqIAAADgIQoAYsO4DgAADYQCgNhIcbki4pJcoogRLlfERtIwBoBoowAgTrhcERtpCgAiLmms6whAr1EAEBspZgEg4lJcoogRCgBigwKAqEsxSoUYoQAgNtKGyxXRlgp4BID44I6K2GAEAFGXCrilIj64WhEbTdxcEXGDEq4TAL3HHRWxMThIuY4ArNNwZgEiRigAiI3BAR+vEG0jE9xSER9crYgNCgCibnSaWyrig6sVsdFsEqwEQGSZwGoI81QQI1ytiJVWRgEQUYlk6DoC0CcUAMTK4CDpOgKwRukkewAgXigAiJWhjAAgonIUAMQMBQCxMjpIu44ArNHwjOsEQN9QABArYxMUAETT+Cx7ACBeKACIlTFJCgCiaXKax1OIFwoAYmV0kFaCMwEQMUZWG2cpAIgXCgBiJWmMRrAlMCImmakozVHAiBkKAGJnLI8BEDGDMqwAQPxQABA7Y5gIiIgZQQFADFEAEDsTk1nXEYAPmJLjVor44apF7GycyjINEJGyXTPzUhA/FADETotJaDSPARAR6UxZwzkGGDHEVYtY2jiZcx0BkCQNb+L5P+KJAoBYmppiHgCiYTJdFDFFAUAsMQKAqJjWwgmViCcKAGJpZCKlwZwMCMeCZKjJaQoA4okCgNjaJNXkOgI8N7Sp4joC0G8UAMTW1ulm1xHguS1bWZCK+KIAILa2SjVxMBDcMVZ7DmL9P+KLAoDYajYJTWE1ABxpbqpoKOv/EWNcvYg1HgPAlSmDWP+PeKMAINa2S7W4jgBP7dbK7H/EGwUAsTYykdKoBM9hUV+pTEVTWf6HmKMAIPamMQqAOpswiOV/iD8KAGJv12yr6wjwzD6DGXVC/FEAEHtjE2ltlGQ1AOojlytr8yzD/4g/CgAawq4ZRgFQH1sOZvY/GgMFAA1hl0yLUoZNgVBjxuqAwWnXKYCqoACgITSbhLZKsScAamtYa1nD2fwHDYIrGQ3j4zwGQI3tPIRbJhoHVzMaxsdSTRwRjJpJpELt3czsfzQOCgAaRsIY7Z0d7DoGGtTmQ8tKMs8EDYQCgIayV7ZNacNljeoygdVhQzOuYwBVxZ0SDaXJJJgLgKobN5jJf2g8XNFoOPtmB4uBWlSNkQ4bzsY/aDwUADScUYmUtuGYYFTJkEElTeHgHzQgCgAa0n7ZIa4joEEcMJyVJWhMFAA0pE1SOU1J5VzHQMw1N5W1cxNL/9CYKABoWDNzw1xHQMwdOIrZJGhcFAA0rKmpnLZMNbmOgZhqHVTWbs3s+4/GRQFAQzuiaRgrAtAvR4zk9ojGxhWOhrZRMqvtMi2uYyBmhraWtG2OZ/9obBQANLwjc8OVYBwAvWWko0ay7A+NjwKAhjcqkdJ0dgdEL41uK2nzLAUAjY8CAC8c2TRMTYb13Fg3E1h9cTQT/+AHCgC80BokdFgTywKxbtuNKmtsktsi/MCVDm/snW3TxGTWdQxEVCZb0Wc58Q8eoQDAG0bS55tHMB0QH2WkI8caJQ1XB/xBAYBXJiaz2iPb5joGImb84JJ2YtkfPEMBgHdmNg1TKxMC8Z4gEeoEJv7BQxQAeKfJJPTZ5hGuYyAi9hoTamiCWyH8w1UPL+2UGaSd04Ncx4BjIweXdEgbE//gJwoAvPWFlhEanmDDF18lUxWdNpo3f/iLAgBv5UxCX2oerYB1Af4x0qHjpLYk/+/hLwoAvDY1ldN+2cGuY6DOJg8raneO+oXnKADw3mFNwzQhwVCwLzLZik4exYZQAAUA3ksZoy8PGq2M4ceh0ZmE1fHjAqXZ8AegAACSNCaR1okto5kN0OD2HlPRZpz0B0iiAAD/Mi3drINyQ13HQI1MHVFkyR+wGgoAsJrDm4Zpq3Sz6xiosrZBJZ0yMuc6BhApFABgNUbSyS2jtUGCGeKNIpmu6Ovj0wp4vgN8AAUA+JCsCXTaoA2UZVJg7JmE1QkTAg0J+H8JfBg/FcAabJBI66RBGyjBbPHYMrI6eHyoLZj0B6wRBQBYi61TTZrVMoqVATG169iK9mnhUQ6wNhQAYB12Tg/SMc0jXcdAH209uqyjhjDjH1gXCgCwHntn27R/dojrGOilycOLOmE4b/7A+lAAgF44qnm4dsu0uY6B9RjRVtJpo1nuB/QGBQDoBSPpiy0jtC17BETW4EElfXNchpsa0Ev8rAC9lJDRV1o20PaZFtdR8CHD2ko6f8OMkqzaAHqNAgD0QcIYndwyWh/PtLqOgvcMby3p3HEZpVivAfQJC2SBPgpkdHzLKBkZPVxY6TqO1zYYUtLZY7Ls8gf0AyMAQD8YSce1jNQ+ucGuo3hr7JCSzh7Lmz/QX4wAAP1kJB3dNEIJK/0xv8J1HK9MHl7UV5ntDwwIIwDAABhJn24eoWObRyrBM+jaM9J2o0u8+QNVwAgAUAV7ZNs0LJHSf3e8rR5bcR2nIZmE1YFjK9qvNes6CtAQGAEAqmTLVJP+vW2chiXo1dWWSFV04kbSfq3s8AdUCwUAqKJxibQuaJugqSmGqKsllyvr7EkJbZGjWAHVRAEAqqzFJHTGoLGanmavgIEaMbik70xKaXQq4ToK0HBMR1fBug4BNKq/Ftp1TdcSFW3oOsoa9bwy2nWENTPStqNKOm44z/uBWmFMDaihXTOtmpTM6n863taCSsF1nFhIpSv64oaBtsrw5g/UEiMAQB2UrNWNPUv1l55o7RcQtRGAkYNL+rcxGTWzuw9QcxQAoI6eLnbqys7F6o7IUsGoFAATWO0xpqLDBzPLH6gXHgEAdbRdukUbtmX0667FerHU7TpOJAxqLmnWmJQmZnjzB+qJEQDAkacKnbqma7E6HY4GuBwBMIlQO46s6OhhWZYjAQ5QAACHumxFN3Yv04N5N6cKuioAQ1tLOmkDlvcBLlEAgAh4rtStazvf0bKwXNfXrXcBCJKhPjkm1MHs6Ac4RwEAIiKvULd3LdNfCitVsfX5saxXATCy2nBYWbNGZtSaYIY/EAUUACBi3qmU9NuuxXqhDpME61EAmpvL+uwGCX0sy5xjIEooAEBEPVvs0m+7F2tppXaPBWpZAIJkqF1HhTpiSIZJfkAEUQCACCvYUHf3vKs/5N9VqQaPBWpRAIysxg8t68RRDPcDUUYBAGJgcaWk33Yv0fPFrqp+3WoXgJbmso4Zzcl9QBxQAIAYebbYpd91L9GSSqkqX69aBSCRCjV9ZKiZQ5jdD8QFBQCImaINdU9+pe7oWa7CAE8ZHHABMNKkYSXNGplRC/v3A7FCAQBianlY1s3dy/Roob3fX2MgBaBtUFnHjU5qUobNfIA4YnIuEFNDg6S+1DJKwaV/l97pqd8LB0V1PXSjvrthhjd/IMYoAEDMmbntSlz8ooLb35TyNTxXILAqv/283jnvdLX//q7avQ6AumCqLtAIQivzyDtKPP+uwoPGy247TKrmI/nKMi373/9W8bXXqvhFAbhEAQAaSXtRwXWvSU8uVnjohrKjmwb05UxQUOd9t6r9rj9WKSCAqKAAAI3otQ4Fl7wkO32k7F4byA5K9+33B2UV//Gkll91tWyxWJuMAJyiAACN6r3HAuaJxbLbDpPdZpjspFZpLbvzGVnZcKUKLz+tFTfdpLCrjhMLAdQdBQBodCUr8+RSmSeXSslAdkyTNCwjm0uqkJyrsKNdpTcXqPuZZ2W7edMHfEEBAHxSDmXmd0rzO2UkLX/lFteJADjCMkAAADxEAQAAwEMUAAAAPEQBAADAQxQAAAA8RAEAAMBDFAAAADxEAQAAwEMUAAAAPEQBAADAQxQAAAA8RAEAAMBDFAAAADxEAQAAwEMUAAAAPEQBAADAQxQAAAA8RAEAAMBDFAAAADxEAQAAwEMUAAAAPEQBAADAQxQAAAA8RAEAAMBDFAAAADxEAQAAwEMUAAAAPJR0HQCr6VohLX5Tal8m9bTLFgsyxR7ZQreUSMpkmqRsi2wmK+XaZEaMl4ZuIAUJ18kRYWlT1qhghYYH7WoKCkqrrIwpqTkoaNzwV9WllLptoG6b0MowqbmlJj3V06KOkOsKa2cqZQVLFipY9LpM50oF+W6Z7napp1uqlKVck2ymScrkFLa0KRw8SuHYSQpbh7qOjvdQAFxpXyo7d7b02nPSO6+veuPvbv/IL7Nr+ft//XMyJQ0bJ42cILPhlrKTp8mM3UQKGNzxUdqUtHFykTZLvaUJyaUaFazQkKBT5iNXzyqVnsVr/kI5KUyl1JnIaJFp0qOlIbqzc5hWVigFXgorSr7+olIvPqbEnGeUfOs1mbfny5SLff5StmWwKmMmqTJhE5U230mlrabLDh5Zg9BYH9PRVVjznQHVZUPp9edkn7tPmjt71Rt+reRapcnbyGw2Xdp6LynbUrvXgnP/PuuX2ikzR5unFmhi8h0lFPb691aendv7FzJG3ZmcXlWbru0ao/NuvbkfaREXprtd6UfvUurp+5R66YlVn+5rJBw3RaUtp6sw/WCVN9tBMqZmr4X/jwJQY/bdd2Se/YvsE7dLS9+qf4BkWpq6g8x2B0hb7i4lGPRpCPlO2ZcelmbfLTvn6bV+wl+fPhWAD2trU2n7vdR9xNdUGblh/78OoiOsKPXiY8o8eIvST9wt5XvqH2HYaBV2O0zFvY9SZYOJdX99n1AAamXe89K9V8v+/XHXSf7FDBklu8fnZHb6lJRKu46D/lixWHrgN7JP/F4qFQb85QZUAN6XMKpssZ26jv+eyuM2HfjXQ/0VC8rec52yd1yqYOk/XadZxRiVttlTPTNPU3nqNNdpGhIFoNrmzJa95yrptWdcJ1m7QUOlPY+R2XmGlGlynQa9sfQt2fuvlZ6+WyqXqvZlq1IA3mcChZt8TJ3HfUflydtU7+uiZkxPl7J/ulaZO69QsGKJ6zhrVdpyuvIzT1Npi11cR2koFIBqWbZIuu3Hsq885jpJ77UOkw46ZdXjAUSSLealB34r3Xet1I8JV+tT1QLwPmNU2WpHtX/9UtnmwdX/+qiK1Ox71fyrcxUse9t1lF4rbbe3uo6/QOGo8a6jNAQKwEBVyrKP3iLdfalUrP/zsqqYvK3MEWdKIzdynQSre/kR2dsukZbXbki2JgXgfdmM8kedqu5DTqvda6DPEm+/oabLv63Usw+6jtI/6Yx6Dj1Z+cNPlk1mXKeJNQrAQCyaI3vt+dKS+a6TDFwyLR1wkszun2YGrmv5DtkbfiA9/0DNX6qmBeA9dqMpWnn+7xS2sdTLKWuVu/1SZa+/uF/L96KmMn5jdX7t56psyLyT/qIA9JN9+m6Zmy9aNUTbSDb/uMxnzpOaWl0n8ZJd+HfpN+fXbcVIPQqAJKkpp67Tf6zC9gfW5/XwAUHHu2r++TeU+tt9rqNUlU1l1PO5c5Q/6DjXUWKJAtBXhW7Zm34oPXOP6yQ1Y4aMlj7/PWnC5q6jeMU+fKN01y+qOslvfepWACSZwKi436fVccIP6/aakJL/+JtaLv5KdGb310Bx98PUeeL3pWzOdZRYoQD0RXe77BVnSG++6DpJ7SXTMp/9trTVJ1wnaXzWSnf+XPbB6+v+0vUsAO8Lt5imFd+6gT0p6iD91F/UcsmpUnHgS0ajrjx5K3Wee5XC1mGuo8QGBaCX7LtvS5d9rTGe9/dWEKyaHLjTDNdJGle5JPt/33U2ouSiAEiSnThVK79/u8IUn9hqJfPAzWr6n7NlKmXXUeomHDtZ7edfq3D4GNdRYoEN43vjnXnSL77s15u/JIWh7E3/Jd3/G9dJGlOxR7ryzIZ+nLQ2Zt4/1Pb1vaWu2m0v67PsLf+t5l+e4dWbvyQFb72m1nMPV2LBHNdRYoECsD7L/yl76enSyuhuklFT1sre9d+yD/2f6ySNpVKWrjlX9h9Puk7ijPnnIg05e38FcV0+G1GZP16jpt/916pHSx4Klr2t1u8co2DxQtdRIo8CsC5dK2R/9W+rjuf13e9/Jvv03a5TNAZrZW+8MFLbRLti3l6k1m8d7u2bVbWlH7lDzVde4DqGc2bFYg36j89FenfDKKAArIUt5mWvPMu/Yf+1sVa64Qeyrz7hOkn83fkLafZdrlNERjD3FbX98AuuY8Re6sVH1fyLM6Ww96dBNrLE22+o5QcnyOS7XUeJLArA2lz3H37M9u+LSlm69vxV2x6jf568U/bB61yniJzE0w+r+br/dB0jthJvv6GW/zpRptz4s/37Ivna82r+5ZmuY0QWBWAN7CM3SS884DpGNOU7V21U0wA7idXdO/Ok2y52nSKyMrdeocyLD7uOETumXFDzxafKdHe6jhJJ6cfuUuZPTGReEwrAh/1zrnTXL12niDS74BXpD//jOka8lIqyv72g8XaOrKYwVPOPT2ZlQB/lrvmBkq8zWrkuTVd9V8l5L7mOETkUgNXYYl72mnOrcs56o7MP3yC9/FfXMWLD3v4TaRFLk9aro1NtFzIfoLdST92j7N2/dh0j8ky5oOZLTpMKFPDVUQBWd89V0pIFrlPEg7Wyt1wU3xMQ62ne89ITt7tOERuJV55V9q+3uo4RfYW8mq/8Nisoeimx6HXlbmF0d3UUgPctWSCx1r1vViyWvYdPH+sUVmRv/TE36b6wUtMV326IE+tqKXfDJQqW1OfQqEaRvf1SJRa95jpGZFAA3nfbJUxs64+HrpMWv+E6RWTZR25i6L8/2tvVctV5rlNEVmLBHGXvvNJ1jNgx5aKarrjAdYzIoABI0osPyb7Kpiz9Ui5Jv/+56xTR1L1S+tPlrlPEVuremxUsb9wT7Aai6dffk6nU79TIRpJ67mGlZt/rOkYkUAAk6V6GsQfCvvLYqpUB+AD7yE1Soct1jPgqV9Ry9bdcp4ic5LyXlHruIdcxYi13Ex9aJAqA7KtP8OZVDRwY9EHFHumvN7tOEXvJp+6XaV/uOkakZG/8KXNKBig591mlnn/EdQznvC8Auvca1wkawwsPrtroBqs8eovUtcJ1ivgrldXy2++4ThEZwcK5Ss/27/TIWsjezIoArwuAXfCK9PozrmM0BhtyYuD7wgp/FlWUeuRuqezXsbZrk7vjMvb6r5LUS48p+doLrmM45XUB0FN/cJ2gsTx7L5soSbL/eEpqX+o6RuMoFJXjEZNULCj9OCdyVlP6wVtcR3DK3wJQLknPMRO0qgpd0ks8VzMcm1x1mXs5QCn9+N0y3R2uYzSU9CN3eL2aIuk6gDN/f4xntDXwym9/rV9f5++hJBkVdW7lAaVcB2kwwev/0KlHfEkrQn//ZL8bPKXtjOsUjSVoX6bkcw+rNG0v11Gc8LYA2Gf+7DpCQ9rYvq78sqXqDLOuozixS+ZVpZr9/URRM6HVUdnX9PPlY10ncWKIKWrbJh4r1ULmodu8LQB+PgKwoTTnadcpGlJCoTZJ+rs96Rap+a4jNKwdEu+6juDMNomVCsTSv1pIPv9Xb5dVelkA7KK5q3ZpQ034XACmJhe5jtCwNij5+/x7m4DHlbUStC9TYsE/XMdwwssCoLl8+q+lTVMLXUdwYnRihYYE/s5/qLWgVNbW2W7XMZzYJskHllpKvfCo6whO+FkAXvub6wQNbYPEuxoc+LcFrs8jH/VyQLN/z8FHmKLGGY7drqXUi391HcEJPwvAwlddJ2h44xP+3agnJJe4jtDwpno4wrKxh99zvSXmveQ6ghP+FYBCt9SxzHWKhjcq4d8zy1GBv5PU6mWozbuOUHfjAj8fe9RTsOxtmbx/f87eFQC7ZL63Mz7rabSHM7ZHe1h66q257N9Ok+MDhv9rzloFb7/hOkXdeVcAtIRlWvXg25th1hTVxie1mgtKZQ1J+nUuwHjDdVUPybdecx2h7rwrAGYZy7TqYUTg16zlEUG76wje2Drj1wTTDQL/Hnu4YN7278OhdwVAPf6uJa6nJuPXUK1v369LQxJ+jQC0GL++X1dMt38l3rsCYAs8T6uHjCnLeLRzWTYouo7gjVaP3hADWWXE8b/1EPT4t9rCuwJgCjxPqwcjq7RHN+qM2P+/XlqDiusIdZNVKM7/qQ+T9+vRkuRhAbAUgLrJevSmmDX+fK+utQT+FMuc8afsuGYYAfCAZTitXhLGnz9rDmqpn4RHy3i5ruqo4s/96n3+FYBMznUCb/TYtOsIdZO3/p5TX28dNuE6Qt3k5c/36prNNbuOUHf+FYB0k+sE3ijKnzfFgkffq2udoT9/1t0elR3XbK7FdYS6864AmCwFoB6KNqmK9Wf6UsGj0Q7X2j16U6zIqGi9u007wQiAB2yGAlAPPg3/S/59vy6tDP0pAJLUpaTrCF5gBMADZvAo1xG8sDz064fJt+/Xpb8X/CrxSyiXdRGOGOs6Qt15VwA0H5jVrAAAFiNJREFUYoLrBF54JxziOkJdrQyb1B1mXMdoeDaR0PySX3/OC0O/Co8rlTGTXEeoO/8KwMgNXSfwwtsVvwqAJC0O21xHaHiFlF9v/pI0P8y6juCFkALggZYhUnaQ6xQN752Kf2+GPpaeelse+FcAFlpGAGrNtgxWOMi/n1//CoAkjZnsOkHDe6syzHWEunsr9O97rrf5Hr4Zzgv9m51eb5UNN3EdwQk/C8CkbVwnaGjtNqe3K4Ndx6i7V0tjXEdoeA/k/fuU9mbYpHeZCFhTpS12cR3BCS8LgJmynesIDe3vpfGyHh5hMr8yUnlu1DVjg0D3d/pXLK2k55hfUlOlLae7juCElwVAG35MSnGjrpW/l/xbTiNJFWs0p7yB6xgN691si8oeFktJerZMAaiZTFaVqVu7TuGEnwUglV5VAlATr5TGuY7gzMul8a4jNKwXPf4U/KyHj9TqpbTpjrJJ/yaXSr4WAElm671cR2hIb1ZGamnY6jqGM08XJ3OCe00Y/a5ztOsQziywOc1lMmBNFKcf5DqCM/7uMbnN3tLtP5XKRddJGsrwfY/UD7ef4TqGU5XrnlUw/znXMRpKZfgIHffVH7mO4VT6rzdIf/yl6xgNxaYyKu5ygOsYzvhbAHKt0ubTpecfcJ2kcQQJtXz8ILUM8nxb3F0OkqUAVFV5txnaeDO/N/EKNjhW9i+XylTKrqM0jNIO+8g2+Tti6e0jAEky2/nb/Gpik50kDzfT+Iit9pJJs3tb1SQCdR9yiusUzoWDR6i89cddx2gohd0Pcx3BKa8LgDbbVRrBpK2q2e0o1wmiIdMku4O/zxWrrbLFNFmKpSQpv/+xriM0jMqoDVXedg/XMZzyuwAEgcweR7tO0RjGTpXZeAfXKSLDfOLzUjLlOkb8mUCdX7jAdYrIKE3bU+XJW7mO0RDyh58im/D3KbjkewGQpB0OlhnCEcEDZfY5XjLMfv+XwSOlbfZ1nSL2wqlbqLLRlq5jREr+sJNcR4i9cNhoFffwe/hfogBIiaTsbp9xnSLeRk2UttjNdYrIMXt/Xgr4Ees3Y9T1xW+5ThE5xR33VzhuiusYsZafcZJsks3guDtJMtMPk0ZMcB0jvg4+lU//azJigrST30siByL82DSVpvJY6SOCQF3Hnu86RWxVNpiowr48+pUoAKsk09JhX3edIp622lNmMz8P0ugNc+CXVx1BjT4x6ZTaT2PN+9qUttlDxR32cR0jlrqP+7a3O/99GAXgPWbqjtLH9nQdI1ZMOitz8GmuY0RbrlXmwJNdp4id/KeOVTjE353/eqP7hO9I2ZzrGLFS3OUglabt6TpGZFAAVnfIV6WMf+eN99u+J0hDOfxmvXY4SJro52Ej/WFHjFTXZ/7ddYzIC4ePUffhFPDesk0t6v7iea5jRAoFYDVmyCiZmd90HSMeJm8r7c5ztF4xRuaY70hN/h5m02vJpNrPuoI5Jb2UP/QklT62q+sYsdA163sKh/OBZXUUgA/bZm9px0+5ThFtLUNWvaExw733Bo+U+cx5vLGtR/7or6kykZM6ey0I1PXVn8gOGeE6SaTl9/msirsf6jpG5HAHXwNz2DekMRu7jhFNJpA++22pdbjrJPGz+a4yux7hOkVkhdvsrO4Zp7qOETvh4BHqPOVHFPK1qEyYqu5jWU66Jlwxa5JKy3z+e1IzZ3B/mDnwpFUTJtE/B5+66vEJPmjUaLWfdZXrFLFV2nYPdX/6G65jRE7YOkydZ10mZTibY00oAGszYrw068dMClzd9COkT3zOdYp4S6Zljv8vaexU10kiw7a2asUP7lCYZkb7QOSP+IryBx/vOkZ0ZLLqPOdXqozeyHWSyKIArIMZv5nMcT9kT3dJ2vaTMof9m+sUjSHTLPOlSziISpJyOXV89xaFrSNdJ2kI3V84T8XpB7uO4ZxNpNRxxqUqT53mOkqkUQDWZ8r20qfPk3w+NGKz6TKfPn/V839UR8sQmeN/JLV5PHkrl1HHt65VeSzb2lZNEKjr9B+rtO0nXCdxxiZS6j79YpU8P+mvN7ij94LZdh+ZWRd7+TjATNtf5lhGQWpixHiZr14hjZ7sOkn9NTer/bu3qLTx9q6TNBybzKjznF+psJeHx3Nnsuo85zIVdmUlV29QAHpr4+1lvvwzryYGmt1mSkd7PvpRa63DZU75pbSRR0vfBg/Ryov+oPJGW7hO0rBsIqmuky9U/pATXUepG9vcpvbzf+P16EdfmY6ugnUdIlbemSd79TnSkgWuk9ROMiUdfJrMx490ncQfhW7Z678nvfBAXV+28uzcur6e3WiK3v2PW6Sm1rq+rs+yd16h3LU/lKmUXEepmXDsZLWfdZnCsR6Opg0ABaA/Ct3STRfKPvMX10mqb/BImc99169PpFHy+G2yt10iletzs65bATCBSnvNUMfJl9Tn9fABybnPqeWSUxW803gfXIq7H6auE/9TNuvfI9qBogAMgH36bpmbL5It5l1HqY7NP75qtzo+nTllF/5d+s350tK3av5adSkATTl1nf5jFbY/sPavhbUKOt5V88+/odTf7nMdpSpsKqOez52j/EHHuY4SWxSAgVq6ULr1x7KvPuE6Sf81tcoceNKqs+vZqjYaij2yD/xOuu+amo4G1LQAGKNwi2lq//plCluH1e510HvWKvPQrcpd830FK5e6TtNvpS12VteXvqdwHCtIBoICUC0vPyJ780XSyiWuk/SeMTLT9pMOOd2ryY2x8s+5q66rN16oyZevWQEYNkydX/mRilsxISuKTHe7ctdfouwfr5HCius4vWYHj1T3589RYY/DXUdpCBSAasp3rvrU9shNUr7TdZq1M0badBdpv1ky4zZ1nQbrY0PZv/1Zuudqacn8qn7pqheAlmYV9v+8uo46i73pYyA591nlbviJUn97wHWUdbJNrcofdJzyn/qSbFOL6zgNgwJQC4Vu2SfvXDV827HcdZr/zxhps+nSPsfLjN/MdRr0lQ2lVx6V/nzlqnkCVVC1AjCoRcW9j1LnZ77JnhExlHjz78rdcZnSD98eqRGBsHWoCvt/QfmDj5dlblLVUQBqqdAtPfsX2dl/lN54XrKO/qhbh0vT9pPZ8WBp5IZuMqB6rJX9xxPS7D9ILz4slQr9/lIDKgCBkd1wsvJ7H62efY/jE38DCBbOVfbe/1Pm4dtlVix2E8IYlTfdXoU9jlDh4zOkLGdE1AoFoF6WviX7tz9Kz90nvTOv9q/X1Cqz6S6y2+0vs/EO3JwbVb5Teu6+VY8I3nyhzxMG+1wATCA7fLhKO++v7hmnKhzMHv4NKawo9dwjyjx0i1LPPCjTuaLmL1mZMFXFXQ5SYffDFY7inIx6oAC40LFcdu5sac7T0uvPSMsWrRreHYjsIJmNtpDdeHtpynYyYzZm737P2GJemvecNGe2zGt/k/3na1K5uM7fs94CYALZtjaFkzZTcdre6vn4kVJLWxVTI/LCUMl5Lyn14qNKvviokq8+I9PdPrCvGQSqjJyg8pY7q7TldJW22EV2iMfnYjhCAYiCUmHV5K7F86WlC2RXLJYpdMkWeqRCt0yhWzaZkknnZHMtq06Ty7VIIydIwydIozaSWoa4/i4QNWEoLf+n7NIF0jtvSMvfksl3yxZ7pHynTL5L5Yceks1kpXRWNp2Vsk2qjBqv8kZbqrzxNJUmbc0zfXxEsGKJgrdeV3LRawoWzZPpbpfp7pTp7pDJd0nlomy2Rco1yWabFeZaZIdvoMqYSe/9NVFKZV1/G96jAAAeW7yi23UEAI4wRgwAgIcoAAAAeIgCAACAhygAAAB4iAIAAICHKAAAAHiIAgAAgIcoAAAAeIgCAACAhygAAAB4iAIAAICHKAAAAHiIAgAAgIcoAAAAeIgCAACAhygAAAB4iAIAAICHKAAAAHiIAgAAgIcoAAAAeIgCAACAhygAAAB4iAIAAICHKAAAAHiIAgAAgIcoAAAAeIgCAACAhygAAAB4iAIAAICHKAAAAHiIAgAAgIcoAAAAeIgCAACAhygAAAB4iAIAAICHKAAAAHiIAgAAgIcoAAAAeIgCAACAhygAAAB4iAIAAICHKAAAAHiIAgAAgIcoAAAAeMicffZt1nUIAG6Uy6+6jgDAkeQbbyx3nQGAI3Needh1BACO8AgAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPUQAAAPAQBQAAAA9RAAAA8BAFAAAAD1EAAADwEAUAAAAPBZKs6xAAAKCejAJJPa5jAACA+jFBwgaSecd1EAAAUD+JRKYcSPYV10EAAED9JJPZ5YEx+pPrIAAAoH5SqeYHg0oleZuYCAgAgCeMMqmmi4Mbb/zCfEmPuY4DAABqL5Ntbf/z/T96IpCkMNS/uw4EAABqL5sbfoH03kZAN954/IOS7nYZCAAA1FY2N+yd+x/86SXSajsBGmNnSVrkLBUAAKiZIJEJW5pGzPjXP7//N9dff8IiYzRTUsFJMgAAUBPGBGptHfu1P9//oyfe/3cfOAvg+uuPf9QYe5SkzrqnAwAAVRcECTuobeL37nvwZz//wL//8C+8/voT7ghDM10y8+oXDwAAVFsyla0MHjLpcw889NPzP/zf1nga4I03HvdCoaBp1upCcVYAAACxYkxCLYPGPDZ42MiJ99x/ye/W+GvW90WOOeZX40qlxKnG6FBJm1Q9JQBn5rxyi+sIAKoomWoqZrND/pZIt5x6//0/fnpdv3a9BWB1Rx991abWhrtaayYaY4ZZa9c4ggDUUyqVnZLJ5PZynSOOXp97n+sI8WTt8nI5z0FqcM9aaxLJd41J/SOdTN/0l/sv/kNvf2ufCgAQRWee+cRvJB3jOkcczZ//kusIsZTNtrz+618fNdl1DmAg+ASPWJs584aEpP1c54BfisX8RjNn3pB2nQMYCAoAYm3SpI12kjTcdQ74JQzLQWtr+guucwADQQFArIWhPch1BvgpDEtfdJ0BGAgKAGLNWlEA4ESxWNzOdQZgICgAiK2zznpkjDHaynUO+KlcLuRmzbqTEoDYogAgxpIHi5UscCgMi6e7zgD0FwUAsWVtwPA/nCqXC/u4zgD0FwUAsXTaaXMy1lo2/4FTxWJ+g2OO+UOr6xxAf1AAEEtNTcv3NEYtrnPAb9ZaNTUVT3adA+gPCgBiKQyZ/Y9oKJVKn3GdAegPCgBiyVod4DoDIEnFYn4L1xmA/qAAIHa+8Y3ZmxqjKa5zAJJUqZRSxx//h31d5wD6igKA2EkkQob/ESnG5E9xnQHoKwoAYsdatv9FtJRKhd1cZwD6igKAWDnttMdbJe3qOgewukIhP/SUU24b7zoH0BcUAMRKLqd9JXEMKyLGqlAI2RUQsUIBQKxw+A+iqlyuzHCdAegLCgBi44ILbCCZ/V3nANakWOyefMEF9ydd5wB6iwKA2OjoeGo7SaNd5wDWJAwrwVtvdRztOgfQWxQAxEYiwex/RFupVDzedQagtygAiA2e/yPqyuXCDq4zAL1FAUAsnHHGX0dKmuY6B7AupVKxedas27dynQPoDQoAYiEIEgeJ6xWRZxWGZZYDIha4oSIWrA0Y/kcslMvl/VxnAHqDAoDIO/HE2SnJftJ1DqA3isWesaeccn+L6xzA+lAAEHmtrZXdJLW5zgH0hrWhKRRWfsl1DmB9KACIvCBg9j/iJQzLn3WdAVgfCgAij+V/iJtiMc9KAEQeBQCRds45T02StInrHEBflMvF9Je/fOvernMA60IBQKSVy/Zg1xmA/iiV7EmuMwDrQgFApBnD9r+Ip1KpsKfrDMC6UAAQWWec8VyzpN1d5wD6o1TKD//qV28f5ToHsDYUAERYzyclZV2nAPrDWquurspprnMAa0MBQGSx/A9xVyqVD3edAVgbCgAiyhprzQGuUwADUSrlp0qW+ywiiQsTkXTmmU9tLWmc6xzAQFQq5cSJJ95xhOscwJpQABBJ1jL7H42hVCqzLTAiybgOgPg666ynNrE2nCHZfSSziaRhkppc50LvzZ//kusI6ANjAgVBopxIJFcmk+knjMn99MorD/yz61yIJwoA+uyss5441Fp9RxLbncYcBSD+UqlMTzabu/jyyw8/z3UWxAsFAL129tlPblGp2MuM0XTXWVAdFIDGkU5n23O55s9edtmMu1xnQTwwBwC9cuaZT+4fhvavvPkD0VQs5ls7Olb8/oQTbv2+6yyIBwoA1uvMM5+YJdm7JLW5zgJg7cKwYjo73/3mCSfccrXrLIg+CgDW6cwzn9hN0i/FtQLERmfnyi/OmnX7N1znQLRxU8danX327AmSbpOUdp0FQF9YdXWtuOiUU+7YwXUSRBcFAGsVhpXvSxrqOgeAvgvDiunqyl/nOgeiiwKANTrjjMe3knS06xwA+i+f75o8a9Yd/BxjjSgAWCNjdKa4PoCYsyqV8t91nQLRxA0eH3HiibNTkmErXqABFIs9k4499iqO1cZHUADwEa2tdg9JQ1znADBwYVgxicSQk13nQPRQAPARxlTY7AdoIGFYPtB1BkQPBQAfYa2Z5DoDgOoJQ7uh6wyIHgoAPsIYdvwDGom1YbPrDIgeCgAAAB6iAOAjrNVK1xkAVI8xQZfrDIgeCgDWwLzmOgGA6gmC4A3XGRA9FAB8RBDoUdcZAFRPIhH8wXUGRA8FAB/R1NT1oKTlrnMAGLggSNhyecX/us6B6KEA4CMuuOATZWt1l+scAAYunc6+fvXVx+Vd50D0UACwRolE5SJJoescAAbCKJVqOtd1CkQTBQBrdOGF01+Q9BvXOQD0XzbbMufyyz/1f65zIJooAFirSsWcJ2mp6xwA+i6RSISpVI6jgLFWFACs1cUX77ggCOxhkoquswDoC6Ncru2Myy8/+GnXSRBdFACs04UX7vyItTpFUsV1FgC909zcdtUVVxx6iesciDYKANbrRz/a6QrJHCxphessANYuCBJ20KDB/3nllYcf7zoLoo8CgF656KId/2hMOF3Sw66zAPioTCa7orl56MGXX374ea6zIB6M6wCIn7POeuwQa4PvSNrGdRYMzPz5L7mOgAFKJjM9TU3NF/3qV4d+23UWxAsFAP12zjmPTqlUgkOtNZ80RptKGi6JY0djhAIQL8YYBUGqnEgkVqRSmcdTKfOTSy897F7XuRBP/w/x4C1mi3XMfAAAAABJRU5ErkJggg==
        """

        # Icon
        self.iconphoto(True, tk.PhotoImage(data=self.icon_base64))

        # Create initial menubar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # File menubar
        self.file_menu = tk.Menu(self.menubar, tearoff=False)
        self.file_menu.add_command(label='Configure', command=lambda:[self.homepage.home_frame.destroy(), ConfigurePage(self)]) # Removes current home_frame and then opens config page
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.destroy,)

        # Help menubar
        self.help_menu = tk.Menu(self.menubar, tearoff=False)
        self.help_menu.add_command(label='About', command=lambda:[self.homepage.home_frame.destroy(), AboutPage(self)])

        # Add all Menus to the menubar
        self.menubar.add_cascade(label='File', menu=self.file_menu)
        self.menubar.add_cascade(label='Help', menu=self.help_menu)

        # canvas - creates the screen
        self.canvas = tk.Canvas(self, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        # Draw home_page on the screen
        HomePage(self)

    # Reads the config.yaml
    def read_config_yaml(self):
        with open('config.yaml', 'r') as f:
            config = yaml.load(f, Loader=SafeLoader)
        return config

class HomePage(tk.Frame):
    def __init__(self, myapp):
        super().__init__()

        self.myapp = myapp

        # Frame for everything on home screen
        self.home_frame = tk.Frame(self.myapp, bg='grey')
        self.home_frame.place(relwidth=1, relheight=1)

        # Label - IP Address Field
        self.input_label = tk.Label(self.home_frame, text='IP Address: ', bg='grey', fg='white')
        self.input_label.grid(row=0, column=0, sticky=tk.W, padx=(113, 0))

        # Input box for ip address
        self.search_ip = tk.Entry(self.home_frame, width=35)
        self.search_ip.grid(row=0, column=0, sticky=tk.W, padx=(180, 0))

        # Submit button and enter key creation
        self.search_btn = tk.Button(self.home_frame, text = 'Submit', fg = 'black', command=self.search_ip_clicked)
        self.search_btn.grid(row=0, column=0, sticky=tk.W, padx=(400, 0))
        self.myapp.bind('<Return>', self.search_ip_clicked)

        # Output Window
        self.output_window = tk.Text(self.home_frame, height=29, width=75)
        self.output_window.insert(tk.INSERT, 'Results show up here')
        self.output_window.grid(row=1, column=0)
    
    # event=None has to be here for the ENTER button on keyboard to be used.
    def search_ip_clicked(self, event=None):
        ip_result = re.search(r'\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}', str(self.search_ip.get())) # pulls only an ipv4 address from search_ip input box
        if ip_result == None: # Checks if nothing was found
            self.output_window.delete(1.0, tk.END) # Clear output window
            output = '[-] Only use an IPv4 Address. Ex: 8.8.8.8'
            self.output_window.insert(tk.END, output)
        else:
            r_config_yaml = self.myapp.read_config_yaml()
            self.output_window.delete(1.0, tk.END) # Clear output window
            output = f'Showing results for: {ip_result.group(0)}\n'
            self.output_window.insert(tk.END, output) # Adds the searched IP Address to the top of the reporting list.
            self.run_analyzer(ip_result.group(0), r_config_yaml)
            self.search_ip.delete(0, tk.END) # Clear search window
        
    # Checks to see if analyzer is enabled and if so then creates a new thread for that analyzer
    def run_analyzer(self, ip_address, config):
        for analyzers in config['analyzers']: # Dynamically creates a thread for each analyzer
            enabled = f'{analyzers}_enabled'
            if config[enabled] == True:
                analyzer = threading.Thread(target=self.query_analyzer, args=(ip_address, config, analyzers))
                analyzer.start()

    # fetches/filters data for each analyzer dynamically
    def query_analyzer(self, ip_address, config, analyzer):
        if config[analyzer] == 'your_api_key_goes_here': # Checks to see if there no data in api key field
            output = f'\n[-] {analyzer} is missing an API Key\n'
        else:
            fetch_data = 'fetch_data'
            mod = importlib.import_module(f'{analyzer}_analyzer') 
            fetch = getattr(mod, fetch_data)

            filter_data = 'filter_data'
            filter = getattr(mod, filter_data)

            data = fetch(ip_address, config[analyzer])
            output = filter(data)

        self.output_window.insert(tk.END, output) # Adds output to output window

class ConfigurePage(tk.Frame):
    def __init__(self, myapp):
        super().__init__()

        self.myapp = myapp
        self.homepage = HomePage(self.myapp)

        # Frame for everything on Configuration page
        self.config_frame = tk.Frame(self.myapp, bg='grey')
        self.config_frame.place(relwidth=1, relheight=1)

        # Back Button - Removes current config_frame and then opens config page
        self.back_btn = tk.Button(self.config_frame, text = 'Back', fg = 'black', command=lambda:[self.save_btn_func(), self.config_frame.destroy(), self.homepage])
        self.back_btn.grid(row=0, column=0, sticky=tk.W)

        # Load on/off Images
        self.on_image = tk.PhotoImage(file='switch-on.png')
        self.off_image = tk.PhotoImage(file='switch-off.png')

        # Adds AbuseIPDB to config page
        self.abuseipdb_widget()

        # Adds alienvault to config page
        self.alienvault_widget()

        # Adds greynoise to config page
        self.greynoise_widget()

        # Adds pulsedive to the config page
        self.pulsedive_widget()

        # Adds virustotal to the config page
        self.virustotal_widget()

        # Configuration Label
        # self.input_label = tk.Label(self.config_frame, text='Configuration Page', bg='grey', fg='white', font=('Calibri', 18))
        # self.input_label.grid(row=1, column=0, pady=(0, 20))

    # abuseIPDB widget
    def abuseipdb_widget(self):
        abuseipdb_label = tk.Label(self.config_frame, text='AbuseIPDB', bg='grey', fg='white', font=('Calibri', 13))
        abuseipdb_label.grid(row=2, column=0)
        self.abuseipdb_btn = tk.Button(self.config_frame, command=lambda: [self.switch_btn('abuseipdb')], bg='grey', bd=0, activebackground='grey',)
        abuseipdb_image = self.set_init_switch('abuseipdb')
        self.abuseipdb_btn.config(image=abuseipdb_image)
        self.abuseipdb_btn.grid(row=2, column=0, sticky=tk.E)
        self.abuseipdb_entry = tk.Entry(self.config_frame, width=90)
        abuseipdb_key = self.set_init_key('abuseipdb')
        self.abuseipdb_entry.insert(0, abuseipdb_key)
        self.abuseipdb_entry.grid(row=3, column=0, padx=(20, 0))
        self.abuseipdb_link = tk.Label(self.config_frame, text='https://www.abuseipdb.com/account/api', fg='orange', bg='grey', font=('Calibri', 10))
        self.abuseipdb_link.grid(row=4, column=0, padx=(20, 0), pady=(0, 20), sticky=tk.W)
        self.abuseipdb_link.bind('<Button-1>', lambda e: self.open_url('https://www.abuseipdb.com/account/api'))
        self.abuseipdb_link_tooltip = Hovertip(self.abuseipdb_link, 'Click here to register for an API Key - AbuseIPDB')

    # alienvault widget
    def alienvault_widget(self):
        alienvault_label = tk.Label(self.config_frame, text='AlienVault', bg='grey', fg='white', font=('Calibri', 13))
        alienvault_label.grid(row=5, column=0)
        self.alienvault_btn = tk.Button(self.config_frame, command=lambda: [self.switch_btn('alienvault')], bg='grey', bd=0, activebackground='grey',)
        alienvault_image = self.set_init_switch('alienvault')
        self.alienvault_btn.config(image=alienvault_image)
        self.alienvault_btn.grid(row=5, column=0, sticky=tk.E)
        self.alienvault_entry = tk.Entry(self.config_frame, width=90)
        alienvault_key = self.set_init_key('alienvault')
        self.alienvault_entry.insert(0, alienvault_key)
        self.alienvault_entry.grid(row=6, column=0, padx=(20, 0))
        self.alienvault_link = tk.Label(self.config_frame, text='https://otx.alienvault.com/api', fg='light blue', bg='grey', font=('Calibri', 10))
        self.alienvault_link.grid(row=7, column=0, padx=(20, 0), pady=(0, 20), sticky=tk.W)
        self.alienvault_link.bind('<Button-1>', lambda e: self.open_url('https://otx.alienvault.com/api'))
        self.alienvault_link_tooltip = Hovertip(self.alienvault_link, 'Click here to register for an API Key - AlienVault')

    # greynoise widget
    def greynoise_widget(self):
        greynoise_label = tk.Label(self.config_frame, text='GreyNoise', bg='grey', fg='white', font=('Calibri', 13))
        greynoise_label.grid(row=8, column=0)
        self.greynoise_btn = tk.Button(self.config_frame, command=lambda: [self.switch_btn('greynoise')], bg='grey', bd=0, activebackground='grey',)
        greynoise_image = self.set_init_switch('greynoise')
        self.greynoise_btn.config(image=greynoise_image)
        self.greynoise_btn.grid(row=8, column=0, sticky=tk.E)
        self.greynoise_entry = tk.Entry(self.config_frame, width=90)
        greynoise_key = self.set_init_key('greynoise')
        self.greynoise_entry.insert(0, greynoise_key)
        self.greynoise_entry.grid(row=9, column=0, padx=(20, 0))
        self.greynoise_link = tk.Label(self.config_frame, text='https://www.greynoise.io/viz/account', fg='orange', bg='grey', font=('Calibri', 10))
        self.greynoise_link.grid(row=10, column=0, padx=(20, 0), pady=(0, 20), sticky=tk.W)
        self.greynoise_link.bind('<Button-1>', lambda e: self.open_url('https://www.greynoise.io/viz/account'))
        self.greynoise_link_tooltip = Hovertip(self.greynoise_link, 'Click here to register for an API Key - GreyNoise')

    # pulsedive widget
    def pulsedive_widget(self):
        pulsedive_label = tk.Label(self.config_frame, text='Pulsedive', bg='grey', fg='white', font=('Calibri', 13))
        pulsedive_label.grid(row=11, column=0)
        self.pulsedive_btn = tk.Button(self.config_frame, command=lambda: [self.switch_btn('pulsedive')], bg='grey', bd=0, activebackground='grey',)
        pulsedive_image = self.set_init_switch('pulsedive')
        self.pulsedive_btn.config(image=pulsedive_image)
        self.pulsedive_btn.grid(row=11, column=0, sticky=tk.E)
        self.pulsedive_entry = tk.Entry(self.config_frame, width=90)
        pulsedive_key = self.set_init_key('pulsedive')
        self.pulsedive_entry.insert(0, pulsedive_key)
        self.pulsedive_entry.grid(row=12, column=0, padx=(20, 0))
        self.pulsedive_link = tk.Label(self.config_frame, text='https://pulsedive.com/api/#login', fg='light blue', bg='grey', font=('Calibri', 10))
        self.pulsedive_link.grid(row=13, column=0, padx=(20, 0), pady=(0, 20), sticky=tk.W)
        self.pulsedive_link.bind('<Button-1>', lambda e: self.open_url('https://pulsedive.com/api/#login'))
        self.pulsedive_link_tooltip = Hovertip(self.pulsedive_link, 'Click here to register for an API Key - Pulsedive')

    # virustotal widget
    def virustotal_widget(self):
        virustotal_label = tk.Label(self.config_frame, text='VirusTotal', bg='grey', fg='white', font=('Calibri', 13))
        virustotal_label.grid(row=14, column=0)
        self.virustotal_btn = tk.Button(self.config_frame, command=lambda: [self.switch_btn('virustotal')], bg='grey', bd=0, activebackground='grey',)
        virustotal_image = self.set_init_switch('virustotal')
        self.virustotal_btn.config(image=virustotal_image)
        self.virustotal_btn.grid(row=14, column=0, sticky=tk.E)
        self.virustotal_entry = tk.Entry(self.config_frame, width=90)
        virustotal_key = self.set_init_key('virustotal')
        self.virustotal_entry.insert(0, virustotal_key)
        self.virustotal_entry.grid(row=15, column=0, padx=(20, 0))
        self.virustotal_link = tk.Label(self.config_frame, text='https://www.virustotal.com/gui/my-apikey', fg='orange', bg='grey', font=('Calibri', 10))
        self.virustotal_link.grid(row=16, column=0, padx=(20, 0), pady=(0, 20), sticky=tk.W)
        self.virustotal_link.bind('<Button-1>', lambda e: self.open_url('https://www.virustotal.com/gui/my-apikey'))
        self.virustotal_link_tooltip = Hovertip(self.virustotal_link, 'Click here to register for an API Key - VirusTotal')

    # Saves all entry fields
    def save_btn_func(self):
        r_config_yaml = self.myapp.read_config_yaml()
        self.abuseipdb_field_check(r_config_yaml)
        self.alienvault_field_check(r_config_yaml)
        self.greynoise_field_check(r_config_yaml)
        self.pulsedive_field_check(r_config_yaml)
        self.virustotal_field_check(r_config_yaml)
    
    def abuseipdb_field_check(self, r_config_yaml):
        if self.abuseipdb_entry.get() == '':
            r_config_yaml['abuseipdb'] = 'your_api_key_goes_here'
        else:
            r_config_yaml['abuseipdb'] = self.abuseipdb_entry.get()
        self.write_config_yaml(r_config_yaml)
    
    def alienvault_field_check(self, r_config_yaml):
        if self.alienvault_entry.get() == '':
            r_config_yaml['alienvault'] = 'your_api_key_goes_here'
        else:
            r_config_yaml['alienvault'] = self.alienvault_entry.get()
        self.write_config_yaml(r_config_yaml)

    def greynoise_field_check(self, r_config_yaml):
        if self.greynoise_entry.get() == '':
            r_config_yaml['greynoise'] = 'your_api_key_goes_here'
        else:
            r_config_yaml['greynoise'] = self.greynoise_entry.get()
        self.write_config_yaml(r_config_yaml)

    def pulsedive_field_check(self, r_config_yaml):
        if self.pulsedive_entry.get() == '':
            r_config_yaml['pulsedive'] = 'your_api_key_goes_here'
        else:
            r_config_yaml['pulsedive'] = self.pulsedive_entry.get()
        self.write_config_yaml(r_config_yaml)
    
    def virustotal_field_check(self, r_config_yaml):
        if self.virustotal_entry.get() == '':
            r_config_yaml['virustotal'] = 'your_api_key_goes_here'
        else:
            r_config_yaml['virustotal'] = self.virustotal_entry.get()
        self.write_config_yaml(r_config_yaml)
    
    def set_init_key(self, analyzer):
        r_config_yaml = self.myapp.read_config_yaml()
        return r_config_yaml[analyzer]

    # Checks config.yaml to see if the analyzer is turned on or not
    def set_init_switch(self, analyzer):
        r_config_yaml = self.myapp.read_config_yaml()
        analyzer_bool = f'{analyzer}_enabled'
        if r_config_yaml[analyzer_bool]:
            return self.on_image
            
        else:
            return self.off_image

    # Used for changing the buttons from on to off in Configuration page
    def switch_btn(self, analyzer):
        r_config_yaml = self.myapp.read_config_yaml()
        analyzer_bool = f'{analyzer}_enabled'
        if analyzer == 'abuseipdb':
            if r_config_yaml[analyzer_bool]:
                self.abuseipdb_btn.config(image=self.off_image)
                r_config_yaml[analyzer_bool] = False
                self.write_config_yaml(r_config_yaml)
                
            else:
                self.abuseipdb_btn.config(image=self.on_image)
                r_config_yaml[analyzer_bool] = True
                self.write_config_yaml(r_config_yaml)

        if analyzer == 'alienvault':
            if r_config_yaml[analyzer_bool]:
                self.alienvault_btn.config(image=self.off_image)
                r_config_yaml[analyzer_bool] = False
                self.write_config_yaml(r_config_yaml)
                
            else:
                self.alienvault_btn.config(image=self.on_image)
                r_config_yaml[analyzer_bool] = True
                self.write_config_yaml(r_config_yaml)
        
        if analyzer == 'greynoise':
            if r_config_yaml[analyzer_bool]:
                self.greynoise_btn.config(image=self.off_image)
                r_config_yaml[analyzer_bool] = False
                self.write_config_yaml(r_config_yaml)
                
            else:
                self.greynoise_btn.config(image=self.on_image)
                r_config_yaml[analyzer_bool] = True
                self.write_config_yaml(r_config_yaml)

        if analyzer == 'pulsedive':
            if r_config_yaml[analyzer_bool]:
                self.pulsedive_btn.config(image=self.off_image)
                r_config_yaml[analyzer_bool] = False
                self.write_config_yaml(r_config_yaml)
                
            else:
                self.pulsedive_btn.config(image=self.on_image)
                r_config_yaml[analyzer_bool] = True
                self.write_config_yaml(r_config_yaml)
        
        if analyzer == 'virustotal':
            if r_config_yaml[analyzer_bool]:
                self.virustotal_btn.config(image=self.off_image)
                r_config_yaml[analyzer_bool] = False
                self.write_config_yaml(r_config_yaml)
                
            else:
                self.virustotal_btn.config(image=self.on_image)
                r_config_yaml[analyzer_bool] = True
                self.write_config_yaml(r_config_yaml)

    def open_url(self, url):
        webbrowser.open_new_tab(url)

    # Writes new config to config.yaml
    def write_config_yaml(self, new_config_yaml):
        with open('config.yaml', 'w') as f:
            yaml.dump(new_config_yaml, f)

class AboutPage(tk.Frame):
    def __init__(self, myapp):
        super().__init__()

        self.myapp = myapp
        self.homepage = HomePage(self.myapp)

        # Frame for everything on home screen
        self.about_frame = tk.Frame(self.myapp, bg='grey')
        self.about_frame.place(relwidth=1, relheight=1)

        # Back Button - Removes current config_frame and then opens config page
        self.back_btn = tk.Button(self.about_frame, text = 'Back', fg = 'black', command=lambda:[self.about_frame.destroy(), self.homepage])
        self.back_btn.grid(row=0, column=0, sticky=tk.W)

        # Label - About Label
        # self.input_label = tk.Label(self.about_frame, text='About Page', bg='grey', fg='white', font=('Calibri', 18))
        # self.input_label.grid(row=1, column=0, padx=(150, 0), pady=(0, 40))

        # Version Information
        self.version_label = tk.Label(self.about_frame, text='Version: 1.0.4', bg='grey', fg='white', font=('Calibri', 12))
        self.version_label.grid(row=1, column=0, padx=(150, 0), pady=(0, 40))
        self.version_label.bind('<Button-1>', lambda e: self.open_url('https://github.com/PeanutTheAdmin/IP-Analyzer-Tool'))
        self.version_label_tooltip = Hovertip(self.version_label, 'Github Link: https://github.com/PeanutTheAdmin/IP-Analyzer-Tool')
        
        self.created_by_attribute = tk.Label(self.about_frame, text='Created by: Jacob Cavaness', fg='orange', bg='grey', font=('Calibri', 10))
        self.created_by_attribute.grid(row=2, column=0, padx=(215, 0), pady=(0, 30), sticky=tk.W)
        self.created_by_attribute.bind('<Button-1>', lambda e: self.open_url('https://www.linkedin.com/in/jacob-cavaness/'))
        self.created_by_attribute_tooltip = Hovertip(self.created_by_attribute, 'Connect On Linkedin: https://www.linkedin.com/in/jacob-cavaness/')

        self.ip_icon_attribute = tk.Label(self.about_frame, text='IP icons created by Freepik - Flaticon', fg='light blue', bg='grey', font=('Calibri', 10))
        self.ip_icon_attribute.grid(row=3, column=0, padx=(200, 0), pady=(0, 30), sticky=tk.W)
        self.ip_icon_attribute.bind('<Button-1>', lambda e: self.open_url('https://www.flaticon.com/free-icons/ip'))
        self.ip_icon_attribute_tooltip = Hovertip(self.ip_icon_attribute, 'Click here to visit: https://www.flaticon.com/free-icons/ip')

        self.on_icon_attribute = tk.Label(self.about_frame, text='On icons created by Pixel perfect - Flaticon', fg='orange', bg='grey', font=('Calibri', 10))
        self.on_icon_attribute.grid(row=4, column=0, padx=(188, 0), pady=(0, 30), sticky=tk.W)
        self.on_icon_attribute.bind('<Button-1>', lambda e: self.open_url('https://www.flaticon.com/free-icons/on'))
        self.on_icon_attribute_tooltip = Hovertip(self.on_icon_attribute, 'Click here to visit: https://www.flaticon.com/free-icons/on')

        self.off_icon_attribute = tk.Label(self.about_frame, text='Off icons created by Pixel perfect - Flaticon', fg='light blue', bg='grey', font=('Calibri', 10))
        self.off_icon_attribute.grid(row=5, column=0, padx=(188, 0), pady=(0, 40), sticky=tk.W)
        self.off_icon_attribute.bind('<Button-1>', lambda e: self.open_url('https://www.flaticon.com/free-icons/off'))
        self.off_icon_attribute_tooltip = Hovertip(self.off_icon_attribute, 'Click here to visit: https://www.flaticon.com/free-icons/off')

        # Create a Label Widget to display the text or Image
        python_powered_img = tk.PhotoImage(file="python-powered.png")
        self.python_powered_label = tk.Label(self.about_frame, image = python_powered_img)
        self.python_powered_label.photo = python_powered_img
        self.python_powered_label.grid(row=6, column=0, padx=(175, 0))
        self.python_powered_label.bind('<Button-1>', lambda e: self.open_url('https://www.python.org/'))
        self.python_powered_tooltip = Hovertip(self.python_powered_label, 'Click here to visit: https://www.python.org/')

    def open_url(self, url):
        webbrowser.open_new_tab(url)

if __name__ == '__main__':
    myapp = MyApp()
    myapp.mainloop()