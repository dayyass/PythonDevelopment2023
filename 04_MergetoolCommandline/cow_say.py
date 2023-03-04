import cmd
import shlex
import readline
from cowsay import list_cows, make_bubble, cowsay, cowthink, Option, COW_PEN, THOUGHT_OPTIONS

class cmdline(cmd.Cmd):
    intro = "cowsay"
    prompt = ">>> "

    def do_list_cows(self, args):
        """
        Lists all cow file names in the given directory

        list_cows [cow_path]
        """
        parsed_args = shlex.split(args)
        cows = list_cows(parsed_args[0] if len(parsed_args) else COW_PEN)
        for cow in cows:
            print(cow)

    def do_make_bubble(self, args):
        """
        Wraps text is wrap_text is true, then pads text and sets inside a bubble.
        This is the text that appears above the cows

        make_bubble text [-b cowsay] [-w width] [-w wrap_text]

        - param text: text in bubble
        - param -b: brackets
        - param -w: width
        - param -wt: wrap_text
        """
        parsed_args = shlex.split(args)
        args_dict = {
            "-b": "cowsay",
            "-w": 40,
            "-wt": True,
        }
        if "-b" in parsed_args:
            args_dict["-b"] = parsed_args[parsed_args.index("-b") + 1]

        if "-w" in parsed_args:
            args_dict["-w"] = int(parsed_args[parsed_args.index("-w") + 1])

        if "-wt" in parsed_args:
            args_dict["-wt"] = bool(parsed_args[parsed_args.index("-wt") + 1])

        print(
            make_bubble(
                parsed_args[0],
                brackets=THOUGHT_OPTIONS[args_dict["-b"]],
                width=args_dict["-w"],
                wrap_text=args_dict["-wt"],
            ),
        )


    def complete_make_bubble(self, pfx, line, beg, end):
        parsed_args = shlex.split(line)
        key, command = parsed_args[-2], parsed_args[-1]
        complete_args_dict = {
            "-b": ["cowsay", "cowthink"],
            "-wt": ["True", "False"],
        }
        if key in complete_args_dict:
            return [s for s in complete_args_dict[key] if s.startswith(command)]
        elif command in complete_args_dict:
            return complete_args_dict[command]
        else:
            return []

    def do_cowsay(self, args):
        """
        Similar to the cowsay command. Parameters are listed with their
        corresponding options in the cowsay command. Returns the resulting cowsay
        string

        cowsay message [-c cow] [-e eye_string] [-T tongue_string]

        - param message: the message to be displayed
        - param -c: cow
        - param -e: eye_string
        - param -T: tongue_string
        """
        parsed_args = shlex.split(args)
        args_dict = {
            "-c": "default",
            "-e": "oo",
            "-T": "  ",
        }
        if "-c" in parsed_args:
            args_dict["-c"] = parsed_args[parsed_args.index("-c") + 1]

        if "-e" in parsed_args:
            args_dict["-e"] = parsed_args[parsed_args.index("-e") + 1]

        if "-T" in parsed_args:
            args_dict["-T"] = parsed_args[parsed_args.index("-T") + 1]

        print(
            cowsay(
                parsed_args[0],
                cow=args_dict["-c"],
                eyes=args_dict["-e"],
                tongue=args_dict["-T"],
            ),
        )

    def complete_cowsay(self, pfx, line, beg, end):
        parsed_args = shlex.split(line)
        key, command = parsed_args[-2], parsed_args[-1]
        complete_args_dict = {
            "-c": list_cows(),
            "-e": ["oo", "LL", "oO"],
            "-T": ["  ", "&&"],
        }
        if key in complete_args_dict:
            return [s for s in complete_args_dict[key] if s.startswith(command)]
        elif command in complete_args_dict:
            return complete_args_dict[command]
        else:
            return []

    def do_cowthink(self, args):
        """
        Similar to the cowthink command. Parameters are listed with their
        corresponding options in the cowthink command. Returns the resulting
        cowthink string

        cowthink message [-c cow] [-e eye_string] [-T tongue_string]

        - param message: the message to be displayed
        - param -c: cow
        - param -e: eye_string
        - param -T: tongue_string
        """
        parsed_args = shlex.split(args)
        args_dict = {
            "-c": "default",
            "-e": "oo",
            "-T": "  ",
        }
        if "-c" in parsed_args:
            args_dict["-c"] = parsed_args[parsed_args.index("-c") + 1]

        if "-e" in parsed_args:
            args_dict["-e"] = parsed_args[parsed_args.index("-e") + 1]

        if "-T" in parsed_args:
            args_dict["-T"] = parsed_args[parsed_args.index("-T") + 1]

        print(
            cowthink(
                parsed_args[0],
                cow=args_dict["-c"],
                eyes=args_dict["-e"],
                tongue=args_dict["-T"],
            ),
        )

    def complete_cowthink(self, pfx, line, beg, end):
        self.complete_cowsay(pfx, line, beg, end)

    def do_exit(self, args):
        """
        Exit from command line
        """
        return 1


if __name__ == "__main__":
    cmdline().cmdloop()
