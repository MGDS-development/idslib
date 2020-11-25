#!/usr/bin/env python3

import json
import requests
import rdflib
import tempfile

DCAT = rdflib.Namespace("http://www.w3.org/ns/dcat#")

class IDSHook():

	def __init__(self, broker_endpoint, api_key):
		self.broker_endpoint = broker_endpoint
		self.api_key = api_key
		
	def getCatalogs(self):
		r = requests.get(self.broker_endpoint + "catalogues/")
		
		if not r.status_code == 200:
			print("Error fetching catalogues!")
		else:
			j = r.json()
			return j['results']['bindings']
		
	def getCatalog(self, catalog_id):
		r = requests.get(self.broker_endpoint + "catalogues/" + catalog_id)
		
		if not r.status_code == 200:
			print("Error fetching catalog!")
		else:
			g = rdflib.Graph()
			d = r.text
			g.parse(data=d, format='json-ld')
		
			return g
			
	def getDataset(self, dataset_id, catalog_id):
		
		r = requests.get(self.broker_endpoint + "datasets/" + dataset_id + "?catalogue=" + catalog_id)
		
		if not r.status_code == 200:
			print("Error fetching catalogues!")
		else:
			g = rdflib.Graph()
			d = r.text
			g.parse(data=d, format='json-ld')
		
			return g
			
	def addDataset(self, g, catalog_id):
		h = {
			'Content-Type': 'text/n3',
			'Authorization': self.api_key
			}
		d = g.serialize(format='n3')
		#print(d)
		r = requests.post(self.broker_endpoint + "datasets/?catalogue=" + catalog_id, data=d, headers = h)
		print(r.status_code)
		print(r.text)
		
		
	def removeDataset(self, dataset_id, catalog_id):
		r = requests.delete(self.broker_endpoint + "datasets/?id=" + dataset_id + "&catalog=" + catalog_id)
		print(r.status_code)
		print(r.text)
	
	def getDatasetData(self, dataset_id, catalog_id):
		
		r = requests.get(self.broker_endpoint + "datasets/" + dataset_id + "?catalogue=" + catalog_id)
		
		destination_file = tempfile.NamedTemporaryFile(prefix='idslib', suffix='dataset.tmp').name
		
		#print("Downloading data on: "+destination_file)
		
		if not r.status_code == 200:
			print("Error fetching catalogues!")
			return None
		else:
			g = rdflib.Graph()
			d = r.text
			g.parse(data=d, format='json-ld')
		
			for t in g.triples((None, DCAT.accessURL, None)):
				self.download_file(t[2], destination_file)
				return destination_file

	def download_file(self, url, local_filename):
		with requests.get(url, stream=True) as r:
			r.raise_for_status()
			with open(local_filename, 'wb') as f:
				for chunk in r.iter_content(chunk_size=8192): 
					f.write(chunk)
		return local_filename
		

