#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from syntax import *

# Tokens are:
# identifiers: starts with a letter (any case) or underscore and then may have any alphanumeric or
# underscore characters following
#
# numbers: which are either one or more digits (0-9) or zero or more digits followed
# by a period followed by one or more digits
#
# keywords: proc, if, else, while, print
#
# symbols: one of +-/*^,:=<{}();
#
tokenRegex = [r"[A-Za-z_]\w*", r"\d+\.\d+|\d+", r"proc|if|else|while|print", r"([+\-/\*^,:=<{}();])"]


def lex(s):
    # Remove comments
    s = re.sub(r"^\s*", "", s, flags=re.M)
    s = re.sub(r"^//.*\n", "", s, flags=re.M)
    s = re.sub(r"^/\*(.|[\r\n])*?\*/", "", s, flags=re.M)
    # Remove inline comments /***/
    s = re.sub(r"/\*.*?\*/", "", s)
    tokens = re.sub(tokenRegex[3], r" \1 ", s).split()

    return tokens


def parse(tokens):
    def is_id(s):
        if s is None:
            return False
        return re.fullmatch(tokenRegex[0], s)

    def is_num(s):
        if s is None:
            return False
        return re.fullmatch(tokenRegex[1], s)

    def peek(n):
        nonlocal tokens
        if not tokens:
            return None
        return tokens[n]

    def expect(s):
        nonlocal tokens
        if peek(0) == s:
            tokens.pop(0)
            return True
        else:
            return ErrorMessage(f"Expected a '{s}'")

    def parse_p():
        s = parse_s()
        if isinstance(s, ErrorMessage):
            return s
        while peek(0) == ";":
            expect(";")
            s1 = parse_s()
            if isinstance(s1, ErrorMessage):
                return s1
            s = SeqStatement(s, s1)  # See: syntax.py
        return s

    def parse_s():
        token = peek(0)
        if token == "proc":
            expect("proc")
            if is_id(peek(0)):
                f = Variable(peek(0))
                expect(peek(0))
                expected = expect("(")
                if isinstance(expected, ErrorMessage):
                    return expected
                l = parse_l()
                if isinstance(l, ErrorMessage):
                    return l
                expected = expect(")")
                if isinstance(expected, ErrorMessage):
                    return expected
                expected = expect("{")
                if isinstance(expected, ErrorMessage):
                    return expected
                p = parse_p()
                if isinstance(p, ErrorMessage):
                    return p
                expected = expect("}")
                if isinstance(expected, ErrorMessage):
                    return expected
                return ProcStatement(f, l, p)
            else:
                return ErrorMessage("Expected Identifier")

        elif token == "if":
            expect("if")
            c = parse_c()
            if isinstance(c, ErrorMessage):
                return c
            expected = expect("{")
            if isinstance(expected, ErrorMessage):
                return expected
            p1 = parse_p()
            if isinstance(p1, ErrorMessage):
                return p1
            expected = expect("}")
            if isinstance(expected, ErrorMessage):
                return expected
            expected = expect("else")
            if isinstance(expected, ErrorMessage):
                return ErrorMessage("Expected else statement")
            expected = expect("{")
            if isinstance(expected, ErrorMessage):
                return expected
            p2 = parse_p()
            if isinstance(p2, ErrorMessage):
                return p2
            expected = expect("}")
            if isinstance(expected, ErrorMessage):
                return expected
            return IfStatement(c, p1, p2)

        elif token == "while":
            expect("while")
            c = parse_c()
            if isinstance(c, ErrorMessage):
                return c
            expected = expect("{")
            if isinstance(expected, ErrorMessage):
                return expected
            p = parse_p()
            if isinstance(p, ErrorMessage):
                return p
            expected = expect("}")
            if isinstance(expected, ErrorMessage):
                return expected
            return WhileStatement(c, p)

        elif token == "print":
            expect("print")
            c = parse_c()
            if isinstance(c, ErrorMessage):
                return c
            return PrintStatement(c)
        else:
            return parse_c()

    def parse_l():
        ret = []
        if is_id(peek(0)):
            v = peek(0)
            expect(peek(0))
            ret.append(Variable(v))
            if peek(0) == ",":
                expect(",")
                x = parse_x()
                if isinstance(x, ErrorMessage):
                    return x
                ret += x

        return ret

    def parse_x():
        ret = parse_l()
        if not ret:
            return ErrorMessage("Expected Variable Identifier after ','")
        return ret

    def parse_c():
        e = parse_e()
        if isinstance(e, ErrorMessage):
            return e
        if peek(0) == "<":
            expect(peek(0))
            e1 = parse_e()
            if isinstance(e1, ErrorMessage):
                return e1
            return LessThan(e, e1)
        elif peek(0) == "=":
            expect("=")
            e1 = parse_e()
            if isinstance(e1, ErrorMessage):
                return e1
            return Equal(e, e1)
        else:
            return e

    def parse_e():
        t = parse_t()
        if isinstance(t, ErrorMessage):
            return t
        while peek(0) == "+" or peek(0) == "-":
            if peek(0) == "+":
                expect("+")
                t1 = parse_t()
                if isinstance(t1, ErrorMessage):
                    return t1
                t = Plus(t, t1)
            else:
                expect("-")
                t1 = parse_t()
                if isinstance(t1, ErrorMessage):
                    return t1
                t = Minus(t, t1)
        return t

    def parse_t():
        a = parse_f()
        if isinstance(a, ErrorMessage):
            return a
        while peek(0) == "*" or peek(0) == "/":
            if peek(0) == "*":
                expect("*")
                f = parse_f()
                if isinstance(f, ErrorMessage):
                    return f
                a = Mult(a, f)
            else:
                expect("/")
                f = parse_f()
                if isinstance(f, ErrorMessage):
                    return f
                a = Div(a, f)
        return a

    def parse_f():
        a = parse_a()
        if isinstance(a, ErrorMessage):
            return a
        if peek(0) == "^":
            expect("^")
            f = parse_f()
            if isinstance(f, ErrorMessage):
                return f
            return Expo(a, f)
        else:
            return a

    def parse_a():
        if peek(0) == "(":
            expect("(")
            c = parse_c()
            if isinstance(c, ErrorMessage):
                return c
            expected = expect(")")
            if isinstance(expected, ErrorMessage):
                return expected
            return c
        elif is_id(peek(0)):
            v = Variable(peek(0))
            expect(peek(0))

            if peek(0) == ":":
                expect(":")
                expected = expect("=")
                if isinstance(expected, ErrorMessage):
                    return ErrorMessage("Expected a '=' after ':'")
                c = parse_c()
                if isinstance(c, ErrorMessage):
                    return c
                return Assign(v, c)
            elif peek(0) == "(":
                expect("(")
                r = parse_r()
                if isinstance(r, ErrorMessage):
                    return r
                expected = expect(")")
                if isinstance(expected, ErrorMessage):
                    return expected
                return Call(v, r)
            else:
                return v
        elif is_num(peek(0)):
            n = Literal(peek(0))
            expect(peek(0))
            return n
        else:
            return ErrorMessage(f"syntax Error after {peek(0)}. Expected a '(' or an identifier or a number")

    def parse_r():
        ret = []
        c = parse_c()
        if isinstance(c, ErrorMessage):
            return c
        ret.append(c)
        if peek(0) == ",":
            expect(",")
            r = parse_r()
            if isinstance(r, ErrorMessage):
                return r
            ret += r

        return ret

    # def parse_q():
    #     ret = []
    #     c = parse_c()
    #     if isinstance(c, ErrorMessage):
    #         return c
    #     ret.append(c)
    #     while peek(0) == ",":
    #         expect(",")
    #         q = parse_q()
    #         if isinstance(q, ErrorMessage):
    #             return q
    #         ret += q
    #     return ret

    return parse_p()

