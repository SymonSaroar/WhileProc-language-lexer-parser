# classes for AST nodes representing the WhileProc language defined in this file.
# WhileProc CFG:
###
# (starting symbol P)
# P -> S ";" P | S
# S -> "proc" f "(" L ")" "{" P "}"
#    | "if" C "{" P "}" "else" "{" P "}"
#    | "while" C "{" P "}"
#    | "print" C
#    | C
# L -> x "," X | x | Ɛ
# X -> x "," X | x
# C -> E | E "<" E | E "=" E
# E -> T | T M
# M -> "+" T M | "-" T M | Ɛ
# T -> F | F N
# N -> "*" F N | "/" F N | Ɛ
# F -> A | A "^" F
# A -> "(" C ")"
#    | x ":" "=" C
#    | f "(" R ")"
#    | x
#    | n
# R -> C "," Q | C | Ɛ
# Q -> C "," Q | C
###


class Node:
    def run(self):
        (v, env, out) = self.interpret({}, "")
        return out


class SeqStatement(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are statements (ProcStatement, IfStatement, Plus, etc.) sequenced with a semicolon
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        return self.rhs.interpret(env0, out0)

    def __str__(self):
        return str(self.lhs) + ";" + str(self.rhs)


class ProcStatement(Node):
    def __init__(self, f, params, body):
        # f is a Variable object, params is a list of Variable objects, body is a statement
        self.f = f
        self.params = params
        self.body = body

    def interpret(self, env, out):
        env0 = env.copy()
        env0.update({self.f.id: self})
        return 1, env0, out

    def __str__(self):
        return "proc " + str(self.f) + "(" + ",".join(map(str, self.params)) + "){" + str(self.body) + "}"


class IfStatement(Node):
    def __init__(self, guard, then_body, else_body):
        # guard is an expression object (Equal, LessThan, Mult, etc.),
        # then_body is a Prog object, else_body is a statement
        self.guard = guard
        self.then_body = then_body
        self.else_body = else_body

    def interpret(self, env, out):
        (v0, env0, out0) = self.guard.interpret(env, out)
        if v0 == 0:
            return self.else_body.interpret(env0, out0)
        else:
            return self.then_body.interpret(env0, out0)

    def __str__(self):
        return "if " + str(self.guard) + " {" + str(self.then_body) + "} else {" + str(self.else_body) + "}"


class WhileStatement(Node):
    def __init__(self, guard, body):
        # guard is a Condition (or Plus, Literal, etc.) object, body is a statement
        self.guard = guard
        self.body = body

    def interpret(self, env, out):
        (v0, env0, out0) = self.guard.interpret(env, out)
        if v0 != 0:
            (v0, env0, out0) = self.body.interpret(env0, out0)
            return self.interpret(env0, out0)
        else:
            return 0, env, out

    def __str__(self):
        return "while " + str(self.guard) + " {" + str(self.body) + "}"


class PrintStatement(Node):
    def __init__(self, rhs):
        # rhs is an expression (LessThan, Div, Expo, etc.) object
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.rhs.interpret(env, out)
        return 0, env0, out0 + str(v0) + "\n"

    def __str__(self):
        return "print " + str(self.rhs)


class LessThan(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expressions (Plus, Mult, etc.) objects
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        (v1, env1, out1) = self.rhs.interpret(env0, out0)
        if v0 < v1:
            return 1, env1, out1
        else:
            return 0, env1, out1

    def __str__(self):
        return "(" + str(self.lhs) + "<" + str(self.rhs) + ")"


class Equal(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Plus, Mult, etc.) objects
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        (v1, env1, out1) = self.rhs.interpret(env0, out0)
        if v0 == v1:
            return 1, env1, out1
        else:
            return 0, env1, out1

    def __str__(self):
        return "(" + str(self.lhs) + "=" + str(self.rhs) + ")"


class Plus(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Plus, Mult, etc.) objects
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        (v1, env1, out1) = self.rhs.interpret(env0, out0)
        return v0 + v1, env1, out1

    def __str__(self):
        return "(" + str(self.lhs) + "+" + str(self.rhs) + ")"


class Minus(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Plus, Mult, etc.) objects
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        (v1, env1, out1) = self.rhs.interpret(env0, out0)
        return v0 - v1, env1, out1

    def __str__(self):
        return "(" + str(self.lhs) + "-" + str(self.rhs) + ")"


class Mult(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Div, Mult, etc.) objects
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        (v1, env1, out1) = self.rhs.interpret(env0, out0)
        return v0 * v1, env1, out1

    def __str__(self):
        return "(" + str(self.lhs) + "*" + str(self.rhs) + ")"


class Div(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Div, Mult, etc.) objects
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        (v1, env1, out1) = self.rhs.interpret(env0, out0)
        if v1 == 0:
            return float('nan'), env1, out1
        return (v0 / v1), env1, out1

    def __str__(self):
        return "(" + str(self.lhs) + "/" + str(self.rhs) + ")"


class Expo(Node):
    def __init__(self, lhs, rhs):
        # lhs and rhs are expression (Expo, Assign, etc.) objects
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.lhs.interpret(env, out)
        (v1, env1, out1) = self.rhs.interpret(env0, out0)
        return (v0 ** v1), env1, out1

    def __str__(self):
        return "(" + str(self.lhs) + "^" + str(self.rhs) + ")"


class Assign(Node):
    def __init__(self, lhs, rhs):
        # lhs is a Variable object, and rhs is an expression (Plus, Assign, Mult, etc.) object
        self.lhs = lhs
        self.rhs = rhs

    def interpret(self, env, out):
        (v0, env0, out0) = self.rhs.interpret(env, out)
        env1 = env0.copy()
        env1.update({self.lhs.id: v0})
        return v0, env1, out0

    def __str__(self):
        return "(" + str(self.lhs) + ":=" + str(self.rhs) + ")"


class Call(Node):
    def __init__(self, f, args):
        # f is a Variable object and args is a list of expression objects (LessThan, Mult, etc.)
        self.f = f
        self.args = args

    def interpret(self, env, out):
        pr = env[self.f.id]
        if isinstance(pr, ProcStatement):
            if len(pr.params) == len(self.args):
                eval_args = []
                last_env = env
                last_out = out
                for v in self.args:
                    (v0, env0, out0) = v.interpret(last_env, last_out)
                    last_env = env0
                    last_out = out0
                    eval_args.append(v0)
                (v0, env0, out0) = pr.body.interpret({k.id: v for (k, v) in zip(pr.params, eval_args)}, out)
                return v0, env, out0
            else:
                print("Runtime error: procedure call with wrong parity.")
        else:
            print("Runtime error: invoked value is not a procedure.")
        exit(1)

    def __str__(self):
        return str(self.f) + "(" + ",".join(map(str, self.args)) + ")"


class Variable(Node):
    def __init__(self, ident):
        # ident is a string encoding the variable's identifier               
        self.id = ident

    def interpret(self, env, out):
        return env[self.id], env, out

    def __str__(self):
        return str(self.id)


class Literal(Node):
    def __init__(self, s):
        # s is a string encoding the literal integer or floating point value 
        self.n = float(s)

    def interpret(self, env, out):
        return self.n, env, out

    def __str__(self):
        return str(self.n)


class ErrorMessage(Node):
    def __init__(self, s):
        # This node should be returned when parsing malformed input (e.g., "proc f(){}")
        # s is an error string
        self.s = s

    def interpret(self, env, out):
        # print(self.s)
        return 0, env, out + self.s + "\n"

    def __str__(self):
        return self.s
