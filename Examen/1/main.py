from checker import build_url, is_https, show_response, check_site, scan_sites, check_headers, retry_check

print("=== PARTEA 1 ===")
print("1.", build_url("example.com", "login"))
print("2.", build_url("example.com", "/login"))
print("3.", is_https("https://example.com"))
print("4.", is_https("http://example.com"))

print("\n=== PARTEA 2 ===")
show_response("https://example.com")

print("\n=== PARTEA 3 ===")
print(check_site("https://example.com"))
print(check_site("https://this-site-does-not-exist.invalid"))

print("\n=== PARTEA 4 ===")
scan_sites()

print("\n=== PARTEA 5 ===")
print(check_headers("https://example.com"))

print("\n=== PARTEA 6 ===")
print(retry_check("https://httpbin.org/status/200"))
print(retry_check("https://httpbin.org/status/404"))
print(retry_check("https://httpbin.org/status/500", attempts=2))
