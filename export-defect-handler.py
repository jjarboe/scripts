import WebService
import sys
import os
from xml.dom import minidom
from xml.dom.minidom import Node
import random
 
def getText(nodelist):
    rc = []
    for node in nodelist:
       #print node.toxml()
       if node.nodeType == node.TEXT_NODE:
          rc.append(node.data)
    return ''.join(rc)
 
def getNodeText(element, nodename):
    try:
        return getText( (element.getElementsByTagName(nodename)[0]).childNodes)
    except IndexError:
        return None
 
if __name__ == '__main__':
 
    wsOpts = WebService.WSOpts()
    parser = wsOpts.get_common_opts()
 
    parser.add_option("--inputfile", dest="inputfile", help="XML file exported from CIM")
    parser.add_option("--debug", action="store_true", dest="debug", help="XML file exported from CIM")
 
    (options, args) = parser.parse_args()
 
    if not options.inputfile:
        print "Input file of defects to be exported must be specified"
        sys.exit(-1)
 
    if not options.password:
        parser.print_help()
        sys.exit(-1)

    debug = None 
    if options.debug and options.debug == True: debug = True

    xmlcid =  minidom.parse(options.inputfile)
 
    if debug: print xmlcid, type(xmlcid)
    if debug: print xmlcid.documentElement.tagName
 
    uxml = xmlcid.getElementsByTagName('cxp:exportedDefect') 
 
    for uxml_element in uxml: 
     user = getNodeText(uxml_element, 'user')
 
    if debug: print "User clicking button is: ", str(user).replace('<','&lt;')
 
    for project_element in uxml: 
     project = getNodeText(project_element, 'project')
 
    if debug: print "Project being viewed is: ", project
 
    if debug: print "==================================== Merged Defect =================================="
    mdxml = xmlcid.getElementsByTagName('cxp:mergedDefect')
 
    for mdxml_element in mdxml:
        cid = getNodeText(mdxml_element, 'cid')
        componentName = getNodeText(mdxml_element, 'componentName')
        checker = getNodeText(mdxml_element, 'checkerName')
        checkerSubcategory = getNodeText(mdxml_element, 'checkerSubcategory')
        file = getNodeText(mdxml_element, 'filePathname')
        function = getNodeText(mdxml_element, 'functionDisplayName')
        try:
            v = [map(lambda y: getText(y.childNodes), x.getElementsByTagName('name')) for x in mdxml_element.getElementsByTagName('defectStateAttributeValues')]
            def norm_dict(x):
                if len(x) == 1:
                    return (x[0],u'')
                return x
            attrs = dict(map(norm_dict,v))
        except ValueError:
            print str(v).replace('<','&lt;')
        owner = attrs['Owner']
        classification = attrs['Classification']

        if debug: print "CID = ", cid
        if debug: print "file = ", file
        if debug: print "function = ", function 
    try:
         if debug: print getNodeText(mdxml[0],'externalReference')
         external_ref = getNodeText(mdxml[0],'externalReference').strip()
    except:
         if debug: print ''
         external_ref = None
         
    if external_ref is None:
        bts_id = '%s-%d' % (project.upper()[:5],random.randint(109,4794))
        print 'as %s.  Refresh page to see new external reference.' % (bts_id,)
        
        WebService.client.connect(api_version=5, options=options)
        defectServiceClient = WebService.client.defect

        def makeId(node):
            f = defectServiceClient.getDO('streamDefectIdDataObj',
                defectTriageId = long(getNodeText(node, 'defectTriageId')),
                defectTriageVerNum = int(getNodeText(node, 'defectTriageVerNum')),
                id = long(getNodeText(node, 'id')),
                verNum = int(getNodeText(node, 'verNum'))
            )
            return f

        sds = []
        for nl in [x.childNodes for x in xmlcid.getElementsByTagName('cxp:streamDefect')]:
            for n in nl:
                try:
                    t = n.tagName
                except AttributeError:
                    pass
                else:
                    if t == 'id':
                        sds.append(makeId(n))

        state = {
            'externalReference': bts_id,
            'comment': 'User %s: Exported CID %s as Issue %s' %  (user, cid, bts_id),
        }
        
        defectServiceClient.updateStreamDefects(sds, state)