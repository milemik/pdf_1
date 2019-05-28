from PyPDF2 import PdfFileReader
import os
from time import sleep


def get_pdfs():
	list_pwd = os.listdir()
	list_pdfs = []
	for d in list_pwd:
	    if d.endswith(".pdf"):
	        list_pdfs.append(d)
	return list_pdfs

def get_info(l_pdfs):
	for doc in range(len(l_pdfs)):
		print(30* "==")
		pdfFileOb = open(l_pdfs[doc], 'rb')
		pwf_reader = PdfFileReader(pdfFileOb)
		print(f"Opening {l_pdfs[doc]}")
		page_1 = pwf_reader.getPage(0)
		con = page_1.extractText()

		content = con.split('\n')
		#print(content)
		phone = 'No phone'
		email = 'No email'
		for cont in range(len(content)):
			if content[cont] == 'SUPPLEMENTAL DATA':
				property_location = content[cont-1]
				#print(f"Property Location at position: {cont}")
			if content[cont] == "Assoc Pid#":
				current_owner = []
				#print(f"Content Owner at position : {cont}")
				c = 1
				while c < 3:
					if content[cont - c].isdigit() == True:
						pass
					else:
						current_owner.append(content[cont - c])
					c += 1
			if content[cont] == "Owner Phone":
				phone, email = [content[cont+3], content[cont+4]]
				#print(f"Phone at position: {cont}")
			if content[cont] == "Assessed":
				total = content[cont+1]
				if total == 'CURRENT ASSESSMENT':
					total = content[cont-1]
		if 'TOPO.' in current_owner:
			#print("current_owner is bad Finding new value...")
			current_owner = []
			for c in range(len(content)):
				if content[c] == 'Additional Owners:':
					x = 0
					while x < 5:
						if content[c + x].isdigit() == True:
							pass
						else:
							current_owner.append(content[c + x])
						x += 1
		if current_owner[0].split(',')[0].isdigit() == True and current_owner[0].split(',')[-1].isdigit() == True:
			#print("CURRENT OWNER is bad, finding new value")
			current_owner = []
			for o in range(len(content)):
				if content[o] == 'Use Co':
					for n in range(8, 10):
						current_owner.append(content[o+n])
		if property_location == 'Rolling':
			#print("Property location is Rolling Finding new value...")
			for c in range(len(content)):
				if content[c] == 'Map ID':
					property_location = content[c+1]
		if property_location == 'Assessed Value':
			for j in range(len(content)):
				if content[j] == 'Property Location:':
					property_location = content[j+1]
			#print(f'Found new value Map ID: {property_location}')
		if property_location == '1':
			property_location = content[-2]
		print(f"Property location: {property_location}\nCurrent owner: {current_owner}\nPhone, Email: {phone}, {email}\nTotal: {total}")
		pdfFileOb.close()
		#sleep(10)
		#return property_location


def create_excel():
	pass


def main():
	pdfs = get_pdfs()
	get_info(pdfs)

main()