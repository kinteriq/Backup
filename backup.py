from commands import receive_command, execute_command


def main():
    command_line = receive_command()
    result = execute_command(command_line)


if __name__ == '__main__':
    main()
