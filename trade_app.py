class Portfolio:
    def __init__(self, portfolio_id, cash_balance,
                 restricted_securities, max_position_pct,
                 current_holdings):

        self.portfolio_id = portfolio_id
        self.cash_balance = cash_balance
        self.restricted_securities = restricted_securities
        self.max_position_pct = max_position_pct
        self.current_holdings = current_holdings


class TradeRequest:
    def __init__(self, portfolio_id, security_id,
                 action, quantity, price, security_type):

        self.portfolio_id = portfolio_id
        self.security_id = security_id
        self.action = action
        self.quantity = quantity
        self.price = price
        self.security_type = security_type


class TradeResponse:
    def __init__(self, decision, reason):
        self.decision = decision
        self.reason = reason

def validate_trade(portfolio, request):

    if request.quantity <= 0 or request.price <= 0:
        return False

    if request.action not in ["Buy", "Sell"]:
        return False

    return True

def check_restricted_security(portfolio, request):

    if request.security_id in portfolio.restricted_securities:
        return False

    return True

def check_sell_holdings(portfolio, request):

    if request.action == "Sell":

        available_quantity = 0

        for security_id, quantity, market_price in portfolio.current_holdings:

            if security_id == request.security_id:
                available_quantity = quantity
                break

        if available_quantity < request.quantity:
            return False

    return True

def check_buy_cash(portfolio, request):

    if request.action == "Buy":

        trade_value = request.quantity * request.price

        if trade_value > portfolio.cash_balance:
            return False

    return True

def check_position_concentration(portfolio, request):

    if request.action == "Buy":

        # Step 1: Post trade cash
        trade_value = request.quantity * request.price

        post_trade_cash = (
            portfolio.cash_balance - trade_value
        )

        # Step 2: Find existing quantity of this security
        existing_quantity = 0

        for security_id, quantity, market_price in portfolio.current_holdings:

            if security_id == request.security_id:
                existing_quantity = quantity
                break

        post_trade_quantity = (
            existing_quantity + request.quantity
        )

        # Step 3: Value of this security after trade
        post_trade_value = (
            post_trade_quantity * request.price
        )

        # Step 4: Value of all other holdings
        value_of_other_holdings = 0

        for security_id, quantity, market_price in portfolio.current_holdings:

            if security_id != request.security_id:

                value_of_other_holdings += (
                    quantity * market_price
                )

        # Step 5: Total portfolio value after trade
        total_portfolio_value_after = (
            post_trade_cash
            + post_trade_value
            + value_of_other_holdings
        )

        # Step 6: Calculate position percentage
        position_pct = (
            post_trade_value / total_portfolio_value_after
        )

        # Step 7: Compare with maximum position limit
        if position_pct > portfolio.max_position_pct:

            return False

    return True

class TradeApprovalService:

    def evaluate(self, portfolio, request):

        # Step 1: Validate
        if not validate_trade(portfolio, request):
            return TradeResponse(
                "Rejected",
                "Invalid trade data."
            )

        # Step 2: Restricted security
        if not check_restricted_security(portfolio, request):
            return TradeResponse(
                "Rejected",
                "Security is restricted for this portfolio."
            )

        # Step 3: Sell check
        if not check_sell_holdings(portfolio, request):
            return TradeResponse(
                "Rejected",
                "Insufficient holdings to sell."
            )

        # Step 4: Buy affordability
        if not check_buy_cash(portfolio, request):
            return TradeResponse(
                "Rejected",
                "Insufficient cash for this buy order."
            )

        # Step 5: Position concentration
        if not check_position_concentration(portfolio, request):
            return TradeResponse(
                "Needs Manual Sign-off",
                "Exceeds maximum position concentration — requires approval."
            )

        # Step 6: All checks passed
        return TradeResponse(
            "Approved",
            "Trade passed all validation checks."
        )


class TradeApplication:

    def __init__(self, portfolios):

        self.portfolios = portfolios
        self.approval_service = TradeApprovalService()

    def process_trade(self, request):

        portfolio = self.portfolios.get(
            request.portfolio_id
        )

        if portfolio is None:
            return TradeResponse(
                "Rejected",
                "Portfolio not found."
            )

        return self.approval_service.evaluate(
            portfolio, request
        )


portfolio = Portfolio(
    portfolio_id="P101",
    cash_balance=50000,
    restricted_securities=["SEC999"],
    max_position_pct=0.10,

    current_holdings=[
        ("SEC101", 100, 200),
        ("SEC102", 200, 100),
        ("SEC103", 50, 400)
    ]
)

portfolios = {
    "P101": portfolio
}

app = TradeApplication(portfolios)

request = TradeRequest(
    portfolio_id="P101",
    security_id="SEC101",
    action="Buy",
    quantity=50,
    price=200,
    security_type="Equity"
)

response = app.process_trade(request)

print("Decision:", response.decision)
print("Reason:", response.reason)
