import numbers
import pandas as pd


def cusum_side(close, h, k=0):
    """Sample points with CUSUM Filter and use its direction as betting side

    Args:
        close (pd.Series): Price series

        h (float or pd.Series): Threasholds to sampmle points.\
            If specified with float, translate to pd.Series(h, index=close.index)

        k (float, optional): Minimum speed parameter to hit threashold.\
            Defaults to 0, which means inactive

    Returns:
        pd.Series: Betting sides at sampled points
    """
    # asssum that E y_t = y_{t-1}
    side = []
    s_pos, s_neg = 0, 0
    diff = close.diff().dropna()
    # time variant threshold
    if isinstance(h, numbers.Number):
        h = pd.Series(h, index=diff.index)
    h = h.reindex(diff.index, method='bfill')
    h = h.dropna()
    timestamps = []
    th = h.loc[h.index[0]]
    for t in h.index:
        s_pos = max(0, s_pos + diff.loc[t] - k)
        s_neg = min(0, s_neg + diff.loc[t] + k)
        if s_pos > th:
            s_pos = 0
            timestamps.append(t)
            th = h.loc[t]
            side.append(1)
        elif s_neg < -th:
            s_neg = 0
            timestamps.append(t)
            th = h.loc[t]
            side.append(-1)
    side = pd.Series(side, index=pd.DatetimeIndex(timestamps))
    return side