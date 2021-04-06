import functools

R = 0.4

@functools.cache
def calculate_result_probs(elo_A, elo_B, HFA=0, draw_possible=True):
    dr = elo_A - elo_B + HFA

    p = 1 / (10 ** (-dr / 400) + 1)

    if not draw_possible:
        return (p,0,1-p)

    w = p * (R + p - R * p)
    d = 2 * (p - w)
    l = 1 - w - d

    return (w,d,l)