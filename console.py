#!/usr/bin/python3
'''entry point of the command interpreter'''
import cmd
from utils.clsPath import classLocations
from models import storage
import re


def castNum(input_str):
    '''casts str to num'''
    # Try converting to float
    try:
        result = float(input_str)
        if result.is_integer():
            result = int(result)
        return result
    except ValueError:
        pass
    try:
        result = int(input_str)
        return result
    except ValueError:
        # If both fail, raise an exception or handle it accordingly
        raise ValueError("Input cannot be cast to float or int")


def getArgfrominsideBracket(insideBrakets: str, clsName: str) -> str:
    '''This function is used as a helper
    function to get final arg string
    that is passed to the do_actions'''
    insideBrakets = insideBrakets.strip('"')
    if insideBrakets == '':
        arg = clsName
    else:
        arg = "{} {}".format(clsName, insideBrakets)
    return arg


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
            parts = line.split('.', 1)
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
                    arg = getArgfrominsideBracket(insideBrakets, clsName)
                    return self.do_show(arg)
                elif methodName == "destroy":
                    arg = getArgfrominsideBracket(insideBrakets, clsName)
                    return self.do_destroy(arg)
                elif methodName == "update":
                    args = insideBrakets.split(',', 1)
                    if args[1].strip()[0] != '{':
                        args = [args[0], *args[1].split(',')]

                    if len(args) > 3 or len(args) < 2:
                        raise

                    id = args[0].strip('"')
                    if len(args) == 3:
                        attrName = args[1].strip().strip('"')
                        attrVal = args[2].strip()
                        if attrVal[0] == '"':
                            attrVal = attrVal.strip('"')
                            line = "{} {} {} \"{}\"" \
                                .format(clsName, id, attrName, attrVal)
                        else:
                            attrVal = attrVal.strip('"')
                            line = "{} {} {} {}" \
                                .format(clsName, id, attrName, attrVal)
                        return self.do_update(line)
                    if len(args) == 2:
                        d = eval(args[1].strip())
                        for key, val in d.items():
                            if isinstance(val, str):
                                line = "{} {} {} \"{}\"" \
                                    .format(clsName, id, key, val)
                            else:
                                line = "{} {} {} {}" \
                                    .format(clsName, id, key, val)
                            self.do_update(line)
                        return
                else:
                    raise
            else:
                raise
        except Exception:
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
        atrName = str(argArr[2])
        atrVal = str(argArr[3]).strip('"') \
            if argArr[3][0] == '"'  \
            else castNum(argArr[3])
        obj = storage.all()[keyFind]
        setattr(obj, atrName, atrVal)
        obj.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
