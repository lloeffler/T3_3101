class PrintLogo:
    def print_color(self):
        """
        Prints DHBW logo as ascii art in black and white.
        """
        light_grey = '\033[37m'
        red = '\033[31m'
        light_red = '\033[91m'
        reset = '\033[0m'
        print('''{0}                                ,%*
                              (###*
                           ,######*
                         /########*
     #################{1}%* %%%%%%%%%#{2}/////////         {0}##########\\      ##      ##   {2}#########    #\\     /##\\     /#{0}
     ###############{1}%%&* %%%%%%%%%#{2}/////////         {0}##       \\#      ##      ##   {2}##      \\#   \\#     #/\\#     #/{0}
     ############{1}%%%%%&* %%%%%%%%%#{2}/////////         {0}##        #\\     ##      ##   {2}##      #/    #\\   /#  #\\   /#{0}
     ##########{1}%%%%%%%&* %%%%%%%%%{2}//////////         {0}##         #)    ##########   {2}#########     \\#   #/  \\#   #/{0}
     #########{1}%%%%%%%%&* %%%%%&{2}(////////////         {0}##        #/     ##      ##   {2}##      \\#     #\\ /#    #\\ /#{0}
     #########{1}%%%%%%%%&* %%%%{2}///////////////         {0}##       /#      ##      ##   {2}##      #/     \\#.#/    \\#.#/{0}
     #########{1}%%%%%%%%&* %{2}(/////////////////         {0}##########/      ##      ##   {2}#########       \\##      \\##{2}
              //////////
              ////////
              /////                                  Duale Hochschule
              ///                                    Baden-Wuerttemberg\n'''.format(red, light_red, light_grey), reset)

    def print_bw(self):
        """
        Prints DHBW logo as ascii art in black and white.
        """
        print('''                                ,%*
                              (###*
                           ,######*
                         /########*
     #################%* %%%%%%%%%#/////////         ##########\\      ##      ##   #########    #\\     /##\\     /#
     ###############%%&* %%%%%%%%%#/////////         ##       \\#      ##      ##   ##      \\#   \\#     #/\\#     #/
     ############%%%%%&* %%%%%%%%%#/////////         ##        #\\     ##      ##   ##      #/    #\\   /#  #\\   /#
     ##########%%%%%%%&* %%%%%%%%%//////////         ##         #)    ##########   #########     \\#   #/  \\#   #/
     #########%%%%%%%%&* %%%%%&(////////////         ##        #/     ##      ##   ##      \\#     #\\ /#    #\\ /#
     #########%%%%%%%%&* %%%%///////////////         ##       /#      ##      ##   ##      #/     \\#.#/    \\#.#/
     #########%%%%%%%%&* %(/////////////////         ##########/      ##      ##   #########       \\##      \\##
              //////////
              ////////
              /////                                  Duale Hochschule
              ///                                    Baden-Wuerttemberg\n''')


if __name__ == '__main__':
    PrintLogo.print_bw()
    print()
    PrintLogo.print_color()