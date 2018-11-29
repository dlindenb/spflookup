#!/usr/bin/python
#
# SPF dns-record resolver.
#
# Report which IP adresses and/or subnets are included in a single SPF record.
#
import sys
import getopt
import dns.resolver


def usage():
	"""
	Show script usage
	"""
	print "USAGE:"
	print "spflookup.py [parameter] <url>\n"
	print "DESCRIPTION:\n"
	print "This script parses a given url of a spf record, to report all includes."
	print "In the end, an overview is given about the IP addresses and/or IP subnets"
	print "allowed sending mail, when implementing the given SPF record\n"
	print "PARAMETERS:\n"
	print "\t-h, --help\t\tPrint this help."
	print "\t-u URL, --url=URL\tParse this URL to resolve all IP addresses "
	print "\t\t\t\tand/or IP subnets."
	print "\n\n\n"
	
	
def resolve_spf(url):
	"""
	This function resolves the SPF record of the given URL
	"""
	qtype = 'TXT'						# only resolve TXT records
	entries = []
	entries.append(url)					# append given url to entries list
	
	answer = dns.resolver.query(url, qtype, raise_on_no_answer=False)	# query dns

	for rdata in answer:				# proces response of first record
		for strings in rdata.strings:
			entry = strings.split()		# split string on white spaces
			entries.extend(entry)		# append strings as list entries to entries list
	return entries						# return list
	
# MAIN #
def main():
	"""
	Main program function
	"""

	url = ''
	records = []

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hu:", ["help", "url="])
	except getopt.GetoptError as err:
		# print error, followed by help info, then exit
		print str(err)
		usage()
		sys.exit(2)
	if not len(opts) >= 1:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit(1)
		elif opt in ("-u", "--url"):
			url = arg
		else:
			assert False, "unhandled option"

	records.append(list(resolve_spf(url)))	# append/clone entries list to the records list

	for idx, val in enumerate(records):		# enumerate include entries in record list
		print (idx, val)
		for i in range(len(val)):
			if "include" in val[i]:			# if include, add new spf entry to records
				tmp_record = (str(val[i]).split(":"))
				tmp_record.pop(0)
				records.append(list(resolve_spf(str(tmp_record[0]))))
				del tmp_record[:]
	
	print "###"
	print "Number of records: ", len(records)


if __name__ == "__main__":
   main()
