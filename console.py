#!/usr/bin/python3
'''entry point of the command interpreter'''
import cmd
from utils.clsPath import classLocations


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

    def do_create(self, arg):
        '''Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id

        Usage: create <className>
        Exapple: create BaseModel
        '''
        clsName = arg.split(" ")[0]
        if clsName == "":
            print("** class name missing **")
            return
        if clsName not in classLocations.keys():
            print("** class doesn't exist **")
            return
        module = __import__(classLocations[clsName],
                                        fromlist=[clsName])
        class_ = getattr(module, clsName)
        obj = class_()
        obj.save()
        print(obj.id)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
