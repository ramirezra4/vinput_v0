from Platterfunc import main
def test_platter(vin):
    out = main(vin)
    print(out)
    return out

"""Test Acura"""
# ILX 4dr Sedan w/ Premium Package
jeepers = main('19UDE2F76NA004740')
print(jeepers)

"""Test Audi"""
# some car

"""Test BMW"""
