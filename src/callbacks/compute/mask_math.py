"""Mask maths: evaluate a MATLAB-style formula over custom detector masks.

MATLAB Quant4D evaluated the formula of a "Math" mask with ``eval`` after
replacing each mask ID (``A``, ``B``, ... ``AB``) by that mask.  This module
implements the same expression language without ``eval``: a small parser for
the subset of MATLAB that makes sense for 2-D masks.

Orientation: MATLAB stores the diffraction pattern as an ``X x Y`` array, so
in a formula the first index is x and the second y (``A(1:3, :)`` are the
first three *columns* of the displayed pattern, ``A'`` swaps x and y).  The
masks are handed to the evaluator transposed to that orientation and the
result is transposed back, so formulas written for the MATLAB app give the
same mask here.

Supported
---------
* numbers (``2``, ``0.5``, ``1e-3``), ``pi``, ``eps``, ``Inf``, ``NaN``,
  ``true``, ``false``; mask IDs (capital letters)
* ``+ - .* ./ .^`` element-wise, ``*`` (scalar or matrix product), ``/`` by a
  scalar, ``^`` of scalars
* ``== ~= < <= > >=``, ``& | ~``, ``&& ||``
* transpose ``'`` and ``.'``
* indexing with 1-based subscripts, ranges ``a:b`` / ``a:step:b``, ``:``
  and ``end``: ``A(1:3, :)``, ``A(end, 2:end)``, linear ``A(k)``
* concatenation ``[A, B; C, D]`` (spaces also separate elements:
  ``[A B]``, ``[A -B]``)
* functions: abs sqrt exp log log2 log10 sin cos tan round floor ceil fix sign
  mod rem max min sum mean any all rot90 fliplr flipud circshift transpose
  double single logical not and or xor zeros ones numel size isnan isinf
"""
from __future__ import annotations

import re
from typing import Callable

import numpy as np

__all__ = ["MaskMathError", "mask_ids", "evaluate_mask_formula"]


class MaskMathError(ValueError):
    """The formula could not be parsed or evaluated; the message says why."""


_TOKEN = re.compile(r"""
    (?P<num>(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?) |
    (?P<id>[A-Za-z_]\w*) |
    (?P<op>\.\^|\.\*|\./|\.'|==|~=|<=|>=|&&|\|\||[-+*/^'<>&|~(),;:\[\]]) |
    (?P<ws>[ \t]+) |
    (?P<nl>\r?\n) |
    (?P<bad>.)
""", re.VERBOSE)


def mask_ids(formula: str) -> list[str]:
    """Mask IDs (runs of capital letters) used in *formula*, in order of first use."""
    seen = []
    for m in re.finditer(r"\b[A-Z]+\b", formula):
        if m.group() not in seen and m.group() not in ("Inf", "NaN"):
            seen.append(m.group())
    return seen


def _ends_operand(tok) -> bool:
    return tok is not None and (tok[0] in ("num", "id") or tok[1] in (")", "]", "'", ".'"))


def _tokenize(text: str) -> list[tuple[str, str]]:
    raw = []
    for m in _TOKEN.finditer(text):
        kind = m.lastgroup
        if kind == "bad":
            raise MaskMathError(f"unexpected character {m.group()!r} at position {m.start() + 1}")
        raw.append((kind, m.group()))

    out: list[tuple[str, str]] = []
    depth: list[str] = []                       # open brackets/parentheses
    for k, (kind, val) in enumerate(raw):
        prev = out[-1] if out else None
        in_brackets = bool(depth) and depth[-1] == "["
        if kind == "nl":
            if in_brackets:
                out.append(("op", ";"))
            continue
        if kind == "ws":
            # inside [...], a space between two operands separates elements;
            # "[a -b]" is two elements but "[a - b]" is one
            if in_brackets and _ends_operand(prev) and k + 1 < len(raw):
                nk, nv = raw[k + 1]
                after = raw[k + 2] if k + 2 < len(raw) else ("ws", " ")
                starts = nk in ("num", "id") or nv in ("(", "[") or \
                    (nv == "~" and after[1] != "=") or (nv in ("+", "-") and after[0] != "ws")
                if starts:
                    out.append(("op", ","))
            continue
        if val == "'" and not _ends_operand(prev):
            raise MaskMathError("strings are not supported (a quote must follow a value, to transpose it)")
        if val in ("(", "["):
            depth.append(val)
        elif val in (")", "]"):
            if not depth or {")": "(", "]": "["}[val] != depth[-1]:
                raise MaskMathError(f"unbalanced {val!r}")
            depth.pop()
        out.append((kind, val))
    if depth:
        raise MaskMathError(f"missing closing {')' if depth[-1] == '(' else ']'}")
    return out


def _as_bool(x):
    return np.asarray(x) != 0


def _mtimes(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return a * b if a.ndim == 0 or b.ndim == 0 or a.size == 1 or b.size == 1 else a @ b


def _mrdivide(a, b):
    b = np.asarray(b, float)
    if b.size != 1:
        raise MaskMathError("'/' needs a scalar divisor; use './' for element-wise division")
    return np.asarray(a, float) / b.item()


def _mpower(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.size == 1 and b.size == 1:
        return a ** b
    raise MaskMathError("'^' needs scalars; use '.^' for element-wise powers")


def _colwise(fn):
    def f(a, *rest):
        a = np.asarray(a, float)
        if rest:                                          # two-argument max/min: element-wise
            return {"max": np.maximum, "min": np.minimum}[fn.__name__](a, np.asarray(rest[0], float))
        return fn(a, axis=0, keepdims=True) if a.ndim == 2 and a.shape[0] > 1 else fn(a)
    return f


def _named(fn, name):
    fn.__name__ = name
    return fn


def _circshift(a, k):
    k = np.atleast_1d(np.asarray(k, int))
    a = np.asarray(a)
    if k.size == 1:
        return np.roll(a, int(k[0]), axis=0)
    return np.roll(a, tuple(int(v) for v in k[:a.ndim]), axis=tuple(range(min(k.size, a.ndim))))


def _rot90(a, k=1):
    return np.rot90(np.asarray(a), int(np.asarray(k).item()))


def _matlab_mod(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return np.where(b == 0, a, a - np.floor(a / np.where(b == 0, 1, b)) * b)


def _size(a, d=None):
    s = np.asarray(a).shape or (1, 1)
    s = s if len(s) > 1 else (1,) * (2 - len(s)) + s
    return np.array(s, float).reshape(1, -1) if d is None else float(s[int(d) - 1])


def _zeros_ones(fill):
    def f(*dims):
        dims = [int(np.asarray(d).item()) for d in dims] or [1]
        return np.full(dims * 2 if len(dims) == 1 else dims, fill, float)
    return f


_FUNCS: dict[str, Callable] = {
    "abs": np.abs, "sqrt": np.emath.sqrt, "exp": np.exp, "log": np.emath.log, "log2": np.emath.log2,
    "log10": np.emath.log10,   # complex for negative input, as in MATLAB (then rejected)
    "sin": np.sin, "cos": np.cos, "tan": np.tan, "floor": np.floor, "ceil": np.ceil,
    "round": lambda a: np.sign(a) * np.floor(np.abs(a) + 0.5),   # MATLAB rounds halves away from zero
    "fix": np.trunc, "sign": np.sign, "mod": _matlab_mod, "rem": np.fmod,
    "max": _colwise(_named(np.max, "max")), "min": _colwise(_named(np.min, "min")),
    "sum": _colwise(_named(np.sum, "sum")), "mean": _colwise(_named(np.mean, "mean")),
    "any": lambda a: np.any(_as_bool(a), axis=0, keepdims=True) if np.ndim(a) == 2 else np.any(_as_bool(a)),
    "all": lambda a: np.all(_as_bool(a), axis=0, keepdims=True) if np.ndim(a) == 2 else np.all(_as_bool(a)),
    "rot90": _rot90, "fliplr": lambda a: np.fliplr(np.atleast_2d(a)), "flipud": lambda a: np.flipud(np.atleast_2d(a)),
    "circshift": _circshift, "transpose": lambda a: np.asarray(a).T,
    "double": lambda a: np.asarray(a, float), "single": lambda a: np.asarray(a, np.float32),
    "logical": _as_bool, "not": lambda a: ~_as_bool(a),
    "and": lambda a, b: _as_bool(a) & _as_bool(b), "or": lambda a, b: _as_bool(a) | _as_bool(b),
    "xor": lambda a, b: _as_bool(a) ^ _as_bool(b),
    "zeros": _zeros_ones(0.0), "ones": _zeros_ones(1.0),
    "numel": lambda a: float(np.asarray(a).size), "size": _size,
    "isnan": np.isnan, "isinf": np.isinf,
}

_CONST = {"pi": np.pi, "eps": float(np.finfo(float).eps), "Inf": np.inf, "inf": np.inf,
          "NaN": np.nan, "nan": np.nan, "true": True, "false": False}

_BINARY = {
    "||": lambda a, b: _as_bool(a) | _as_bool(b), "&&": lambda a, b: _as_bool(a) & _as_bool(b),
    "|": lambda a, b: _as_bool(a) | _as_bool(b), "&": lambda a, b: _as_bool(a) & _as_bool(b),
    "==": np.equal, "~=": np.not_equal, "<": np.less, "<=": np.less_equal, ">": np.greater, ">=": np.greater_equal,
    "+": np.add, "-": np.subtract,
    "*": _mtimes, "/": _mrdivide, ".*": np.multiply, "./": np.divide,
}
_LEVELS = [("||",), ("&&",), ("|",), ("&",), ("==", "~=", "<", "<=", ">", ">="), ("+", "-"), ("*", "/", ".*", "./")]


class _Colon:
    """A bare ':' subscript."""


class _Range:
    def __init__(self, start, step, stop):
        self.start, self.step, self.stop = start, step, stop

    def values(self):
        a, s, b = (float(np.asarray(v).item()) for v in (self.start, self.step, self.stop))
        if s == 0:
            return np.zeros(0)
        n = int(np.floor((b - a) / s + 1e-10)) + 1
        return a + s * np.arange(max(n, 0))


class _Parser:
    def __init__(self, tokens, variables):
        self.toks, self.i, self.vars = tokens, 0, variables
        self.end_stack: list = []                  # sizes for 'end' inside subscripts

    # -- token helpers
    def peek(self, offset=0):
        j = self.i + offset
        return self.toks[j] if j < len(self.toks) else (None, None)

    def take(self, val=None):
        tok = self.peek()
        if val is not None and tok[1] != val:
            raise MaskMathError(f"expected {val!r} but found {tok[1]!r}" if tok[1] else f"expected {val!r} at the end")
        self.i += 1
        return tok

    # -- grammar
    def parse(self):
        if not self.toks:
            raise MaskMathError("the formula is empty")
        value = self.expr()
        if self.peek()[0] is not None:
            raise MaskMathError(f"unexpected {self.peek()[1]!r}")
        return value

    def expr(self, level=0):
        if level == len(_LEVELS):
            return self.unary()
        left = self.expr(level + 1)
        while self.peek()[1] in _LEVELS[level]:
            op = self.take()[1]
            left = _BINARY[op](left, self.expr(level + 1))
        return left

    def range_expr(self):
        """An expression that may be a range a:b or a:s:b (subscripts, brackets)."""
        if self.peek()[1] == ":" and self.peek(1)[1] in (",", ")"):
            self.take(":")
            return _Colon()
        first = self.expr()
        if self.peek()[1] != ":":
            return first
        self.take(":")
        second = self.expr()
        if self.peek()[1] == ":":
            self.take(":")
            return _Range(first, second, self.expr())
        return _Range(first, 1.0, second)

    def unary(self):
        op = self.peek()[1]
        if op in ("-", "+"):
            self.take()
            v = self.unary()
            return -np.asarray(v, float) if op == "-" else v
        if op == "~":
            self.take()
            return ~_as_bool(self.unary())
        return self.power()

    def power(self):
        base = self.postfix()
        while self.peek()[1] in ("^", ".^"):
            op = self.take()[1]
            sign = 1.0
            while self.peek()[1] in ("-", "+"):         # 2^-1
                sign *= -1.0 if self.take()[1] == "-" else 1.0
            exponent = np.asarray(self.postfix(), float) * sign
            base = np.power(np.asarray(base, float), exponent) if op == ".^" else _mpower(base, exponent)
        return base

    def postfix(self):
        value = self.primary()
        while self.peek()[1] in ("'", ".'"):
            self.take()
            value = np.asarray(value).T
        return value

    def primary(self):
        kind, val = self.peek()
        if kind == "num":
            self.take()
            return float(val)
        if val == "(":
            self.take("(")
            v = self.expr()
            self.take(")")
            return v
        if val == "[":
            return self.matrix()
        if kind == "id":
            self.take()
            if val == "end":
                if not self.end_stack:
                    raise MaskMathError("'end' can only be used inside a subscript")
                return float(self.end_stack[-1])
            if val in self.vars:
                value = self.vars[val]
                if self.peek()[1] == "(":
                    return self.index(np.asarray(value))
                return value
            if val in _FUNCS:
                args = self.call_args() if self.peek()[1] == "(" else []
                try:
                    return _FUNCS[val](*args)
                except MaskMathError:
                    raise
                except Exception as exc:
                    raise MaskMathError(f"{val}(...): {exc}") from None
            if val in _CONST:
                return _CONST[val]
            if val.isupper():
                raise MaskMathError(f"unknown mask ID {val!r}")
            raise MaskMathError(f"unknown name {val!r}")
        raise MaskMathError(f"unexpected {val!r}" if val else "the formula ends too early")

    def call_args(self):
        self.take("(")
        args = []
        if self.peek()[1] != ")":
            args.append(self.expr())
            while self.peek()[1] == ",":
                self.take(",")
                args.append(self.expr())
        self.take(")")
        return args

    def index(self, array):
        self.take("(")
        subs = []
        linear = self._linear_ahead()
        while True:
            n = len(subs)
            # 'end' refers to the size of the dimension being indexed (or the element count, for A(k))
            self.end_stack.append(array.size if linear else (array.shape[n] if n < array.ndim else 1))
            try:
                subs.append(self.range_expr())
            finally:
                self.end_stack.pop()
            if self.peek()[1] == ",":
                self.take(",")
                continue
            break
        self.take(")")
        return _apply_index(array, subs)

    def _linear_ahead(self):
        """True if the subscript list starting here has a single entry (linear indexing)."""
        depth, j = 0, self.i
        while j < len(self.toks):
            v = self.toks[j][1]
            if v in ("(", "["):
                depth += 1
            elif v in (")", "]"):
                if depth == 0:
                    return True
                depth -= 1
            elif v == "," and depth == 0:
                return False
            j += 1
        return True

    def matrix(self):
        self.take("[")
        rows, row = [], []
        while self.peek()[1] != "]":
            if self.peek()[1] == ";":
                self.take(";")
                rows.append(row)
                row = []
                continue
            if self.peek()[1] == ",":
                self.take(",")
                continue
            item = self.range_expr()
            row.append(item.values().reshape(1, -1) if isinstance(item, _Range) else item)
        self.take("]")
        rows.append(row)
        blocks = [[np.atleast_2d(np.asarray(v, float)) for v in r] for r in rows if r]
        if not blocks:
            return np.zeros((0, 0))
        try:
            return np.vstack([np.hstack(r) for r in blocks])
        except ValueError as exc:
            raise MaskMathError(f"dimensions do not agree in [...]: {exc}") from None


def _subscript(sub, size):
    if isinstance(sub, _Colon):
        return slice(None)
    vals = sub.values() if isinstance(sub, _Range) else np.asarray(sub)
    if vals.dtype == bool:
        return np.flatnonzero(vals.ravel(order="F"))
    idx = np.asarray(vals, float).ravel()
    if np.any(idx != np.round(idx)) or np.any(idx < 1) or np.any(idx > size):
        raise MaskMathError(f"index out of range: subscripts must be whole numbers from 1 to {size}")
    return idx.astype(int) - 1


def _apply_index(array, subs):
    if len(subs) == 1:                                      # linear, column-major as in MATLAB
        flat = array.ravel(order="F")
        if isinstance(subs[0], _Colon):
            return flat.reshape(-1, 1)
        out = flat[_subscript(subs[0], flat.size)]
        return out.reshape(1, -1) if array.ndim == 2 and array.shape[0] == 1 else out.reshape(-1, 1)
    if len(subs) != array.ndim:
        raise MaskMathError(f"{len(subs)} subscripts for a {array.ndim}-D mask")
    idx = [_subscript(s, n) for s, n in zip(subs, array.shape)]
    return array[np.ix_(*[np.arange(n)[i] for i, n in zip(idx, array.shape)])]


def evaluate_mask_formula(formula: str, masks: dict, shape: tuple) -> np.ndarray:
    """Evaluate *formula* over *masks* and return a mask of ``shape = (NPxY, NPxX)``.

    Parameters
    ----------
    formula : str
        MATLAB-style expression; mask IDs are the keys of *masks*.
    masks : dict of str -> np.ndarray
        Custom masks, each of shape ``(NPxY, NPxX)``.
    shape : (ny, nx)

    Raises
    ------
    MaskMathError
        With a message suitable for the user.
    """
    tokens = _tokenize(formula)
    used = [t[1] for t in tokens if t[0] == "id" and t[1].isupper() and t[1] not in _CONST]
    unknown = sorted({u for u in used if u not in masks})
    if unknown:
        raise MaskMathError(f"unknown mask ID(s): {', '.join(unknown)}")
    matlab_view = {k: np.asarray(v, float).T for k, v in masks.items()}       # X x Y, as in MATLAB
    try:
        with np.errstate(divide="ignore", invalid="ignore"):
            result = _Parser(tokens, matlab_view).parse()
    except MaskMathError:
        raise
    except (ValueError, TypeError, IndexError) as exc:     # e.g. sizes that do not agree
        raise MaskMathError(str(exc)) from None
    result = np.asarray(result)
    if np.iscomplexobj(result):
        raise MaskMathError("the result is complex")
    ny, nx = int(shape[0]), int(shape[1])
    try:
        out = np.zeros((nx, ny)) + np.asarray(result, float)                  # scalars and rows/columns broadcast
    except ValueError:
        raise MaskMathError(f"the result is {result.shape[0]} x {result.shape[1] if result.ndim > 1 else 1} (X x Y), "
                            f"the pattern is {nx} x {ny}") from None
    return out.T
