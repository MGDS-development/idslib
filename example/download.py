import idslib

catalog = '0b36f247-e73e-4f24-ae5a-207a4bff7303'
dataset = '01bdd8a9-38da-464e-94e5-9487b48da524'

h = idslib.IDSHook("https://broker.mgds.xnor.ga/api/hub/", "yourapikey")

tmpfile = h.getDatasetData(dataset, catalog)

print(tmpfile)
