# -*- coding: utf-8 -*-
"""Inverse kinematics via damped least squares (Levenberg-Marquardt style).

Iteratively solves ``J dq = (target - ee)`` with a damping term to stay
numerically stable near singularities::

    dq = J^T (J J^T + lambda^2 I)^-1 (target - ee)

``ik_dls`` is the raw solver; ``ik_chain`` is the convenience wrapper that
returns a full joint-angle vector (None if it fails to converge).
"""


def _matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def _matvec_t(A, x):
    n = len(A[0])
    return [sum(A[i][j] * x[i] for i in range(len(A))) for j in range(n)]


def _matmul(A, B):
    Bt = list(zip(*B))
    return [[sum(a * b for a, b in zip(row, col)) for col in Bt] for row in A]


def _solve22(A, b):
    # 2x2 (or 3x3 for the 3x3 system here we solve the 3x3 JJ^T + lam^2 I)
    n = len(b)
    # Gaussian elimination with partial pivoting
    M = [list(row) + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        if abs(M[col][col]) < 1e-12:
            continue
        for r in range(col + 1, n):
            f = M[r][col] / M[col][col]
            for c in range(col, n + 1):
                M[r][c] -= f * M[col][c]
    x = [0.0] * n
    for i in range(n - 1, -1, -1):
        s = M[i][n]
        for j in range(i + 1, n):
            s -= M[i][j] * x[j]
        x[i] = s / M[i][i] if abs(M[i][i]) > 1e-12 else 0.0
    return x


def ik_dls(chain, target, angles, damping=0.05, max_iter=60, tol=1e-3):
    from .jacobian import numeric_jacobian
    from ..core.linalg import sub3, norm
    q = list(angles)
    for _ in range(max_iter):
        J, ee = numeric_jacobian(chain, q)
        err = sub3(target, ee)
        if norm(err) < tol:
            return q
        # solve (J J^T + lam^2 I) delta = err  then dq = J^T delta
        JJt = _matmul(J, list(zip(*J)))
        lam2 = damping * damping
        for i in range(3):
            JJt[i][i] += lam2
        delta = _solve22(JJt, err)
        dq = _matvec_t(J, delta)
        q = [q[i] + dq[i] for i in range(len(q))]
    return q


def ik_chain(chain, target, init=None, damping=0.05, max_iter=60, tol=1e-3):
    from ..core.linalg import norm, sub3
    init = init if init is not None else [0.0] * chain.n_dof
    q = ik_dls(chain, target, init, damping, max_iter, tol)
    from .fk import fk_chain
    _, ee = fk_chain(chain, q)
    if norm(sub3(ee, target)) > tol * 10:
        return None
    return q
