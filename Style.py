
YellowButton_up = """QPushButton{
                        color: grey;
                        border-image: url(artwork/arrow-yel-1.png);
                        border-top: 3px transparent;
                        border-bottom: 3px transparent;
                        border-right: 10px transparent;
                        border-left: 10px transparent;
                    }"""
YellowButton_down = """QPushButton{
                        color: white;
                        border-image: url(artwork/arrow-yel-2.png);
                        border-top: 3px transparent;
                        border-bottom: 3px transparent;
                        border-right: 10px transparent;
                        border-left: 10px transparent;
                    }"""
PinkButton_up = """QPushButton{
                        color: white;
                        border-image: url(artwork/arrow-pi-1.png);
                        border-top: 3px transparent;
                        border-bottom: 3px transparent;
                        border-right: 10px transparent;
                        border-left: 10px transparent;
                }"""
PinkButton_down = """QPushButton{
                        color: white;
                        border-image: url(artwork/arrow-pi-2.png);
                        border-top: 3px transparent;
                        border-bottom: 3px transparent;
                        border-right: 10px transparent;
                        border-left: 10px transparent;
                    }"""

PlayButton = """QPushButton{
                        color: white;
                        border-image: url(artwork/Butt-PLAY.png);
                        border-top: 3px transparent;
                        border-bottom: 3px transparent;
                        border-right: 10px transparent;
                        border-left: 10px transparent;
                    }""" + """QPushButton: pressed{
                        color: white;
                        border-image: url(artwork/arrow-pi-2.png);
                        border-top: 3px transparent;
                        border-bottom: 3px transparent;
                        border-right: 10px transparent;
                        border-left: 10px transparent;
                    }"""

DefaultButtonStyle = """QPushButton{
                    color: grey;
                    border-image: url(artwork/Butt-PLAY.png) 3 10 3 10;
                    border-top: 3px transparent;
                    border-bottom: 3px transparent;
                    border-right: 10px transparent;
                    border-left: 10px transparent;
                }"""

OKButton = """QPushButton{
                    color: grey;
                    border-image: url(artwork/Butt-OK.png) 3 10 3 10;
                    border-top: 3px transparent;
                    border-bottom: 3px transparent;
                    border-right: 10px transparent;
                    border-left: 10px transparent;
                }"""

Label = """QLabel{
                    font-family: times;
                    font-weight: bold; 
                    color: rgb(247, 115, 109);
                    
                }"""
PopUp = """QWidget{
                    font-family: times;
                    border-image: url(artwork/Butt-NO.png) 3 10 3 10; 
                    border-top: 3px transparent;
                    border-bottom: 3px transparent;
                    border-right: 10px transparent;
                    border-left: 10px transparent;
                }"""

FieldLabel = """QLabel{   
                        font-family: times;
                        font-weight: bold; 
                        color: rgb(247, 115, 109);
                    }"""

TextBox = """QLineEdit{
                        border-image: url(artwork/textbox.png) 3 10 3 10;
                        border-top: 3px transparent;
                        border-bottom: 3px transparent;
                        border-right: 10px transparent;
                        border-left: 10px transparent;
                        font-family: Courier
            }"""
