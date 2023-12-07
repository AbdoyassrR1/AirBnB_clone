#!/usr/bin/python3
'''entry point of the command interpreter'''
import cmd
from utils.clsPath import classLocations
from models import storage
import re


class HBNBCommand(cmd.Cmd):
    '''Command processor'''
    prompt = "(hbnb) "

    def emptyline(self):
        '''Called when an empty line is entered.'''
        pass

    def default(self, line: str) -> None:
        '''This func is called if line does not match any action'''
        # 1. Get line parts
        # 2. If line has <ClassName>.method do it
        # 3. else do super.default(line)
        try:
            parts = line.split('.')
            clsName = parts[0]
            if clsName in classLocations.keys():
                method = parts[1]
                methodName = method.split('(')[0]
                insideBrakets = re.search(r'\((.*?)\)', method).group(1)
                # Do all the methods
                if methodName == 'all' and insideBrakets == '':
                    return self.do_all(clsName)
                elif methodName == 'count' and insideBrakets == '':
                    count = 0
                    for key, _ in storage.all().items():
                        if key.split(".")[0] == clsName:
                            count += 1
                    return print(count)
                elif methodName == 'show':
                    insideBrakets = insideBrakets.strip('"')
                    if insideBrakets == '':
                        arg = clsName
                    else:
                        arg = "{} {}".format(clsName, insideBrakets)
                    return self.do_show(arg)
                else:
                    raise

            else:
                raise
        except:
            super().default(line)

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

    def do_update(self, arg):
        '''Updates an instance based on the class name and id
        by adding or updating attribute (save the change into the JSON file).

        Usage: update <class name> <id> <attribute name> "<attribute value>"

        Ex: $ update BaseModel 1234-1234-1234 email "aibnb@mail.com
        "'''
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
        if len(argArr) < 3:
            print("** attribute name missing **")
            return
        if len(argArr) < 4:
            print("** value missing **")
            return
        atrName = str(argArr[2]).strip('"')
        atrVal = str(argArr[3]).strip('"')
        obj = storage.all()[keyFind]
        setattr(obj, atrName, atrVal)
        obj.save()





if __name__ == '__main__':
    HBNBCommand().cmdloop()
