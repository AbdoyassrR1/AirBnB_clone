#!/usr/bin/python3
'''entry point of the command interpreter'''
import cmd
from utils.clsPath import classLocations
from models import storage


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

        Example: $ create BaseModel
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

    def do_show(self, arg):
        '''Prints the string representation of an instance
        based on the class name and id.

        Example: $ show BaseModel 1234-1234-1234'''
        argArr = arg.split(" ")
        clsName = argArr[0]
        if clsName == "":
            print("** class name missing **")
            return
        if clsName not in classLocations.keys():
            print("** class doesn't exist **")
            return
        if len(argArr) < 2:
            print("** instance id missing **")
            return
        id = argArr[1]
        keyFind = f"{clsName}.{id}"
        if keyFind not in storage.all().keys():
            print("** no instance found **")
            return
        print(storage.all()[keyFind])

    def do_destroy(self, arg):
        '''Deletes an instance based on the class name
        and id (save the change into the JSON file).

        Example: $ destroy BaseModel 1234-1234-1234'''
        argArr = arg.split(" ")
        clsName = argArr[0]
        if clsName == "":
            print("** class name missing **")
            return
        if clsName not in classLocations.keys():
            print("** class doesn't exist **")
            return
        if len(argArr) < 2:
            print("** instance id missing **")
            return
        id = argArr[1]
        keyFind = f"{clsName}.{id}"
        if keyFind not in storage.all().keys():
            print("** no instance found **")
            return
        storage.delete(keyFind)

    def do_all(self, arg):
        '''Prints all string representation of all
        instances based or not on the class name.

        Example: $ all BaseModel or $ all.'''
        argArr = arg.split(" ")
        clsName = argArr[0]

        if clsName == "":
            allCls = []
            for key, clss in storage.all().items():
                allCls.append(str(clss))
            print(allCls)
            return
        if clsName not in classLocations.keys():
            print("** class doesn't exist **")
            return
        allCls = []
        for key, clss in storage.all().items():
            if key.split(".")[0] == clsName:
                allCls.append(str(clss))
        print(allCls)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
