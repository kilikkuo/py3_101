from itertools import tee

def pairwise(iterable):
    # https://docs.python.org/3.4/library/itertools.html#itertools-recipes
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

SMOOTH_RSI_FACTOR = 12  # A heuristic number from yahoo server.

def calc_smooth_rsi(n, prices):
    # NOTE : "prices" 的順序必須從最久遠到最新, OLDEST => NEWEST
    global SMOOTH_RSI_FACTOR
    assert len(prices) >= n * SMOOTH_RSI_FACTOR, "len(prices)=(%d) should equal or greater than # of days(%d)*12."%(len(prices), n)

    first_round_prices = prices[:n+1]
    zipped = pairwise(first_round_prices)

    sum_up = 0.0
    sum_dn = 0.0
    # 計算總共的上漲差之和, 與下跌差之和
    for item in zipped:
        if item[1] >= item[0]:
            sum_up += item[1] - item[0]
        else:
            sum_dn += item[0] - item[1]
    # 計算總共的上漲差之和, 與下跌差之和
    first_avg_gain = sum_up / n
    first_avg_loss = sum_dn / n
    if len(prices) == len(first_round_prices):
        # 理論上的 RSI 計算公式
        assert False, '不採用此公式'
        RS = first_avg_gain / first_avg_loss if first_avg_loss != 0 else 100
        RSI = 100. - 100. / (1. + RS)
        return RSI
    else:
        # 透過前一輪的平均漲跌幅 來計算包含下一日的 RSI 值
        # 例如 : n = 3, 上一輪的 3日-RSI1 從(1/1,1/2,1/3), 下一輪的 3日-RSI2 則從(1/2,1/3,1/4)
        # 利用 (RSI1 的平均漲跌幅) * (n-1) + (1/4 對 1/3 的漲或跌) / n,
        # 當作是下一輪 的平均漲跌幅, 由此值來計算 RSI2
        avg_gain = first_avg_gain
        avg_loss = first_avg_loss
        for i in range(n, len(prices)-1):
            current_gain = 0
            current_loss = 0
            seq_prices = prices[i:i+2]
            if seq_prices[1] >= seq_prices[0]:
                current_gain = seq_prices[1] - seq_prices[0]
            else:
                current_loss = seq_prices[0] - seq_prices[1]

            avg_gain = (avg_gain * (n-1) + current_gain) / n
            avg_loss = (avg_loss * (n-1) + current_loss) / n
            RS = avg_gain / avg_loss if avg_loss != 0 else 100
            RSI = 100. - 100. / (1. + RS)
        return RSI

if __name__ == "__main__":
    a = [1, 2, 3, 4, 2, 3, 3, 4, 3 ,2 ,4, 2, 1, 1, 3, 2, 4, 4, 4, 2, 1, 3, 2, 2,
         1, 2, 3, 4, 4, 3, 1, 1, 2, 2, 4, 4, 3, 3, 1]
    print(calc_smooth_rsi(3, a))
