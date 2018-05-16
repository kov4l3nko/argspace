# ARGSPACE

**Argspace** is just three Python functions. It's even not a micro framework, just a piece of useful code :)

## Requirements

All you need is Python 2.7 :)

## `tokenize(command_line)`

The function takes a command line as a `str` and returns a list of tokens. The rules are

- if `\` leads a character, the character is considered as _escaped_;
- non-escaped spaces and/or tabs divide the command line into _tokens_;
- if the command line ends with `\`, but no escaped character (because the command line ends up), it is assumed that the last token ends with a single escaped space.

Examples:

- `"teststring"` is tokenized to `["teststring"]`
- `"test string"` is tokenized to `["test", "string"]`
- `"test\\ string"` is tokenized to `["test\\ string"]` (the space is escaped, so it does not divide the command line into two tokens)
- `"test\\\\ string"` is tokenized to `["test\\\\", "string"]`
- `"test\\  string"` is tokenized to `["test\\ ", "string"]` (there are tow spaces between `test\\` and ` string`, first one is escaped, second one is not)
- `"test\\ string\\"`  is tokenized to `["test\\ string\\ "]` (the command line ends with `\`, but there is not escaped character because the command line ends up, so it is assumed that the last token ends with a single escaped space)
- `"t\\est \\-string"` is tokenized to `["t\\est", "\\-string"]`

## `resolve_escapes(string)`

The function takes a string with escaped characters and returns a string with resolved escapes, i.e. it turns every two symbols `"\\<some symbol>"` into `"<some symbol>"`.

Examples:

- `"t\\est"` turns to `"test"`
- `"test\\\\"` turns to `"test\\"`
- `"\\-string"` turns to `"-string"`
- `"test\\ string"` turns to `"test string"`
- `"test\\ "` turns to `"test "`

## `resolve_escapes_namespace(name_space)`

If `parse_args(...)` succeed, it returns a namespace. Usually, the namespace contains 

- variables of `str`, `int` etc for a single arguments
- variables of `None` for not-specified arguments
- lists for arguments with `nargs` greater that `1`  or `nargs` equals to `+` or `*`

`resolve_escapes_namespace(name_space)` takes a namespace, walks through it and call `resolve_escapes(string)` (see above) on every string variable and every string in list variable in the namespace. The return value is the same namespace with resolved escapes in strings and lists containing strings.

## Usage

That two functions were developed to use with a standard Python module `argparse`. The `argparse` is good, but there are some limitations:

1. It is not clear how to pass a command line argument containing spaces (e.g. a file name with spaces). Almost all `argparse` examples use `.split(" ")` method to split a command line into a list of tokens and pass the list to `argparse`. Obviously, such approach does not allow arguments with spaces, so if we need arguments with spaces, we need some additional agreements and pre-parsing actions to turn a command line into token list.
2. We can't use arguments started with `-` if the arguments are not a negative numbers. So, if we need to use such arguments, we need  some additional agreements and pre-parsing actions to split a command line into tokens.

With that two functions, you can do the following:

1. Turn a command line `"--cool_argument \\-this\\ argument\\ starts\\ with\\ \\-"` into a list `["--cool_argument", "\\-this\\ argument\\ starts\\ with\\ \\-"]` with `tokenize(command_line)` function.
2. Process the list with `argparse` and get the `cool_argument` as a Python variable of value `"\\-this\\ argument\\ starts\\ with\\ \\-"`.
3. Call `resolve_escapes(string)` on the variable and get `"-this argument starts with -"`.

Or,

1. Turn a command line `"--cool_argument \\-this\\ argument\\ starts\\ with\\ \\-"` into a list `["--cool_argument", "\\-this\\ argument\\ starts\\ with\\ \\-"]` with `tokenize(command_line)` function.
2. Process the list with `argparse` and get a namespace `Namespace(cool_argument="\\-this\\ argument\\ starts\\ with\\ \\-")`.
3. Call `resolve_escapes_namespace(name_space)` on the namespace and get `Namespace(cool_argument="-this argument starts with -")`

So we can use any arguments including arguments with spaces and leading `-`.