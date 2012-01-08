f=file("items.json")
#out=file("items_out.json","w+")
results = []
for item in f:
    str=item.decode("unicode_escape")
    results.append(str)

print "\n".join(results)
#out.writelines("\n".join(results))

