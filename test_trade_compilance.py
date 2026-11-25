import csv

from trade_app import TradeRequest, TradeApplication
from default_data import portfolios


# Create application
app = TradeApplication(portfolios)


# Expected decisions for the 20 trades
expected_decisions = [
    "Approved",
    "Approved",
    "Approved",
    "Approved",
    "Rejected",
    "Needs Manual Sign-off",
    "Rejected",
    "Approved",
    "Approved",
    "Rejected",
    "Approved",
    "Needs Manual Sign-off",
    "Approved",
    "Rejected",
    "Approved",
    "Needs Manual Sign-off",
    "Approved",
    "Approved",
    "Approved",
    "Approved"
]


results = []

passed = 0
failed = 0


# Read trades from CSV file
with open("trades_test.csv", "r", newline="") as file:

    reader = csv.DictReader(file)

    for index, row in enumerate(reader):

        # Create trade request
        request = TradeRequest(
            portfolio_id=row["portfolio_id"],
            security_id=row["security_id"],
            action=row["action"],
            quantity=float(row["quantity"]),
            price=float(row["price"]),
            security_type=row["security_type"]
        )

        # Process trade
        response = app.process_trade(request)

        # Get expected decision
        expected = expected_decisions[index]

        actual = response.decision

        # Compare results
        if actual == expected:
            status = "PASS"
            passed += 1
        else:
            status = "FAIL"
            failed += 1

        # Store results
        results.append([
            request.portfolio_id,
            request.security_id,
            request.action,
            request.quantity,
            request.price,
            actual,
            response.reason,
            expected,
            status
        ])


# Display results
print("\nTRADE APPROVAL TEST RESULTS")
print("=" * 100)

for result in results:

    print("\nPortfolio:", result[0])
    print("Security:", result[1])
    print("Action:", result[2])
    print("Quantity:", result[3])
    print("Price:", result[4])
    print("Decision:", result[5])
    print("Reason:", result[6])
    print("Expected:", result[7])
    print("Test Status:", result[8])

    print("-" * 60)


# Test summary
print("\nTEST SUMMARY")
print("=" * 100)

print("Total Trades:", len(results))
print("Passed:", passed)
print("Failed:", failed)


# Write results to a new CSV file
with open(
    "trade_approval_results.csv",
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "portfolio_id",
        "security_id",
        "action",
        "quantity",
        "price",
        "decision",
        "reason",
        "expected_decision",
        "test_status"
    ])

    writer.writerows(results)


print("\nResults saved to trade_approval_results.csv")