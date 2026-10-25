import re

s = open(r"_riset/main_bundle.js", encoding="utf-8").read()
i = s.find("function me(")
print(s[max(0, i - 1200): i + 1600])
