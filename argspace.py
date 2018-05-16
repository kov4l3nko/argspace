import re


# Tokenize a command line
#   command_line - a command line as a str
# Return: a list of tokens
def tokenize(command_line):
    # Finite automata states
    state_not_token = 0
    state_escaped = 1
    state_not_escaped = 2
    # Characters to be recognized as spaces
    spaces = [" ", "\t"]
    # Initial finite automata state
    current_state = state_not_token
    # Initial current token
    current_token = ""
    # Tokens
    tokens = []
    # Start the finite automata
    for character in command_line:
        # FA is not inside a token
        if current_state == state_not_token:
            # FA faced a non-space character, it means FA entered a token
            if character not in spaces:
                current_token = character
                # If token started with the escape character, the FA state is changed to
                # to state_escaped, else the state is state_not_escaped
                current_state = state_escaped if character == "\\" else state_not_escaped
            # Next character please!
            continue
        # FA is inside a token, the current character is not escaped
        if current_state == state_not_escaped:
            # FA faced a space walking through a token: this is the end of the token
            if character in spaces:
                # Add the token to the tokens list
                tokens.append(current_token)
                # Flush the current token variable
                current_token = ""
                # Change the state
                current_state = state_not_token
            # FA faced a non-space character
            else:
                # Add the character to the current token
                current_token += character
                # If the character is `\`, change state to state_escaped
                if character == "\\":
                    current_state = state_escaped
            continue
        # FA is inside a token, the current character is escaped
        if current_state == state_escaped:
            # Add the character to the current token
            current_token += character
            # Change the FA state to state_not_escaped
            current_state = state_not_escaped
    # FA ends with the command line and the current state is NOT state_not_token
    if current_state != state_not_token:
        # Append the current token to the tokens list (if the token ends with a single escape character`\`,
        # add a space, so `token\` will be added as `token\ `
        tokens.append(current_token + " " if current_state == state_escaped else current_token)
    # Return tokens
    return tokens


# Resolve escapes in a string
#   string - the string :)
# Return: a string with resolved escapes
def resolve_escapes(string):
    return re.sub(r"\\(.)", "\\1", string)


# Resolve escapes in a namespace for string and list of strings variables
#   name_space - the name space
# Return: the name space without escapes in strings and lists of strings
def resolve_escapes_namespace(name_space):
    # Run through the name space
    for k in name_space.__dict__:
        # Get nex value
        value = name_space.__dict__[k]
        if value is not None:
            # It's a string, resolve the escapes
            if type(value) is str:
                name_space.__dict__[k] = resolve_escapes(value)
            # It's a list
            if type(value) is list:
                list_without_escapes = []
                # Run through the list and resolve string members
                for v in value:
                    list_without_escapes.append(resolve_escapes(v) if type(v) is str else v)
                name_space.__dict__[k] = list_without_escapes
    # Return the name space with resolved escapes
    return name_space


if __name__ == "__main__":
    test_command_line = "  -a test -b empty\\ spaces\\ \\-\\   -c \\-first_minus -d last\\\\backslash\\\\ -e last\\ space\\"
    print "Smoke test"
    print "----------"
    print "Command line:\t", test_command_line
    got_tokens = tokenize(test_command_line)
    print "Tokenized:\t\t", got_tokens
    print "No escapes:\t\t", [resolve_escapes(s) for s in got_tokens]
