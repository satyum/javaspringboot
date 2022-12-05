from jinja2 import Environment, FileSystemLoader
import yaml
import sys
import os

def processTemplate(para):
	try:
	#  if  str(sys.argv[1]) == "--ec2":
	#   print("test worked")

		pfile=str(sys.argv[1])
		config = yaml.full_load(open("parameters/"+pfile))
		template_file=config.get('template')
		template_loc="templates/"+template_file+".yml"
		#template_file=pfile.split("-", 1)[0]
		#rname1=rname[0]
		#pfile=str(sys.argv[2])
		#print(rname)
		#print(pfile)
		f = open("output/"+template_file+".yml","w")
		env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
		template = env.get_template(template_loc)
		f.write(template.render(config))
		f.close()
	except:
		print ("\nerror!! Please check file name \n ")
		help()

def help():
	print ("\t Usage:")
	print ("\t python3 templ.py <parameter-file.yml> ")
	print ("\t python3 templ.py s3-param.yml\n")

def main():
	os.system('clear')
	if len(sys.argv) < 2 :
		help()
	else:
		if str(sys.argv[1]).endswith((".yml", ".yaml",".json")):
			processTemplate(str(sys.argv[1]))
		else:
			print("\t Please use the following file type\n ")
			print("\t 1. yaml\n")
			print("\t 2. yml\n")
			print("\t 3. json\n")
			help()
		#print(str(sys.argv[1])+" "+str(sys.argv[2]))	
if __name__ == "__main__":
	main()
