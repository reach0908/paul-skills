from price import line_total

actual = line_total(10, 3)
print(f"line_total(10, 3): expected=30, observed={actual}", flush=True)
assert actual == 30, f"expected 30, observed {actual}"
