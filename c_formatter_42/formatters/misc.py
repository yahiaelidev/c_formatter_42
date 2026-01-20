# ############################################################################ #
#                                                                              #
#                                                         :::      ::::::::    #
#    misc.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: charles <me@cacharle.xyz>                  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2021/02/07 14:39:26 by charles           #+#    #+#              #
#    Updated: 2021/02/07 21:16:03 by charles          ###   ########.fr        #
#                                                                              #
# ############################################################################ #

import re


def parenthesize_return(content: str) -> str:
    return re.sub(
        r"return\s+(?!;)(?!\(.*\);)(?P<value>\(?.*?)\s*;",
        lambda match: f"return ({match.group('value').strip()});",
        content,
        re.DOTALL,
    )


def space_before_semi_colon(content: str) -> str:
    return re.sub(
        r"(?P<keyword>return|break|continue);",
        lambda match: match.group("keyword") + " ;",
        content,
    )


def space_operators_from_structs(content: str) -> str:
    """
    Norminette Error:
    SPC_AFTER/BFR_OPERATOR      ... missing space after/before operator
    """
    left_operators = r'("[^"\\]*(?:\\.[^"\\]*)*")|(\w)(==|!=|<=|>=|&&|\|\||=)'
    right_opperators = r'("[^"\\]*(?:\\.[^"\\]*)*")|(==|!=|<=|>=|&&|\|\||=)(\w)'

    def replace_left(match):
        if match.group(1):
            return match.group(1)
        return f"{match.group(2)} {match.group(3)}"

    def replace_right(match):
        if match.group(1):
            return match.group(1)
        return f"{match.group(2)} {match.group(3)}"

    content = re.sub(left_operators, replace_left, content)
    content = re.sub(right_opperators, replace_right, content)

    return content


def remove_multiline_condition_space(content: str) -> str:
    return re.sub(
        r"(?P<tabs>\t+) {1,3}(?P<rest>.*)",
        lambda match: f"{match.group('tabs')}\t{match.group('rest')}",
        content,
    )


def insert_void(content: str) -> str:
    return re.sub(
        r"(?P<funcdef>[0-9a-zA-Z_]+\t+\**[0-9a-zA-Z_]*\s*)\(\s*\)",
        lambda match: f"{match.group('funcdef')}(void)",
        content,
    )
