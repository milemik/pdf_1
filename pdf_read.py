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
	#doc = 4
	for doc in range(len(l_pdfs)):
		print(30* "==")
		pdfFileOb = open(l_pdfs[doc], 'rb')
		pwf_reader = PdfFileReader(pdfFileOb)
		print(f"Opening {l_pdfs[doc]}")
		page_1 = pwf_reader.getPage(0)
		con = page_1.extractText()
		#page_2 = pwf_reader.getPage(1).getObject().extractText()
		#page_3 = pwf_reader.getPage(2).getObject().extractText()

		content = con.split('\n')
		print(content)
		phone = 'No phone'
		email = 'No email'
		for cont in range(len(content)):
			if content[cont] == 'SUPPLEMENTAL DATA':
				property_location = content[cont-1]# 'Property Location'
				print(f"Property Location at position: {cont}")
			#if content[cont] == "Additional Owners:":
			if content[cont] == "CURRENT OWNER":
				current_owner = []
				print(f"Content Owner at position : {cont}")
				for c in range(0, 5):
					#current_owner = f"{content[cont-4]} {content[cont-3]} {content[cont-2]} {content[cont-1]}"
					try:
						int(content[cont+c])
					except ValueError:
						current_owner.append(content[cont+c])
					'''
					if content[cont+c].isdigit():
						break
					'''
			if content[cont] == "Owner Phone":
				phone, email = [content[cont+3], content[cont+4]]
				print(f"Phone at position: {cont}")
			if content[cont] == "Assessed":  # Assessed
				#total = content[cont+2] # total
				total = content[cont+1] # Assessed
				if total == 'CURRENT ASSESSMENT':
					total = content[cont-1]
		if 'TOPO.' in current_owner:
			print("current_owner is bad Finding new value...")
			current_owner = []
			for c in range(len(content)):
				if content[c] == 'Additional Owners:':
					x= 0
					while x < 5:
						try:
							int(content[c-x])
							pass
						except ValueError:
							x+=1
							current_owner.append(content[c-x])
		if 'SALE PRICE' in current_owner:
			print("CURRENT OWNER is bad, finding new value")
			current_owner = []
			for o in range(len(content)):
				if content[o] == 'Use Co':
					for n in range(8, 10):
						current_owner.append(content[o+n])
			print(f'Found new value {property_location}')
		if property_location == 'Rolling':
			print("Property location is Rolling Finding new value...")
			for c in range(len(content)):
				if content[c] == 'Map ID':
					property_location = content[c+1]
			print(f'Found new value {property_location}')
		#print(f"On position 218 is: {content[218]}")
		print(f"Property location: {property_location}\nCurrent owner: {current_owner}\nPhone, Email: {phone}, {email}\nTotal: {total}")
		pdfFileOb.close()
		#sleep(10)


def main():
	pdfs = get_pdfs()
	get_info(pdfs)

main()
'''
print(30* "==")
print(page_2)
print(30* "==")
print(page_3)
print(30* "==")
'''
### WE NEED property location:     "Property Location:" +1


## WE NEED CURRENT OWNER  "CURRENT OWNER" 4 fields before"Additional Owners:"

#WE NEED OWNER PHONE, MAIL "Owner Phone" , "Owner Email" +3 PHONE +4 EMAIL

# FROM CURRENT ASSESSMENT we need :Total one before 'Appraised Bldg. Value (Card)' OR AFTER 'Total'