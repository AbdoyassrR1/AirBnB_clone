#!/usr/bin/python3
'''entry point of the command interpreter'''
import cmd


class HBNBCommand(cmd.Cmd):
    '''Command processor'''
    prompt = "(hbnb) "

    def emptyline(self):
        '''Called when an empty line is entered.'''
        pass

    def do_EOF(self, arg):
        '''A clean way to exit interpreter\n'''
        print()
        return True

    def do_quit(self, arg):
        """Quit command to exit the program\n"""
        return True


if __name__ == '__main__':
    HBNBCommand().cmdloop()
