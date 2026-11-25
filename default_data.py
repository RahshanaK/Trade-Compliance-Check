from trade_app import Portfolio


portfolios = {

    "POR001": Portfolio(
        "POR001",
        100000,
        ["XYZCORP"],
        0.30,
        [
            ("AAPL", 100, 140),
            ("TCS", 100, 300),
            ("INFY", 20, 1450)
        ]
    ),

    "POR002": Portfolio(
        "POR002",
        50000,
        [],
        0.30,
        [
            ("GOOGL", 2, 1900),
            ("MSFT", 10, 400)
        ]
    ),

    "POR003": Portfolio(
        "POR003",
        100000,
        ["BADCO"],
        0.40,
        [
            ("TCS", 20, 290),
            ("INFY", 20, 1400),
            ("RELIANCE", 30, 2300)
        ]
    ),

    "POR004": Portfolio(
        "POR004",
        100000,
        [],
        0.35,
        [
            ("GOOGL", 5, 1900),
            ("AAPL", 100, 140)
        ]
    ),

    "POR005": Portfolio(
        "POR005",
        100000,
        [],
        0.30,
        [
            ("AAPL", 10, 145),
            ("TCS", 20, 245)
        ]
    )

}