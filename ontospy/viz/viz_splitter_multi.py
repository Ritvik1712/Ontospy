# !/usr/bin/env python
#  -*- coding: UTF-8 -*-


from . import *  # imports __init__
from .. import ontospy
from ..core.entities import OntoClass, OntoProperty, OntoSKOSConcept, Ontology


# TEMPLATE: HTML SPLITTER MULTI FILE


#
# ===========
# Comments:
# ===========
#





def run(graph, ontology, uri, main_entity):
    """
    From a graph instance outputs a nicely formatted html documentation file.
    
    2016-08-07: hacked for multi file save
    """

    context = {
                    "ontology": ontology,
                    "main_uri" : uri,
                    "ontograph": graph,
                    "STATIC_PATH": ontospy.ONTOSPY_VIZ_STATIC,
                }
    
        
    if type(main_entity) == OntoClass:
        ontotemplate = open(ontospy.ONTOSPY_VIZ_TEMPLATES + "splitter/splitter_classinfo.html", "r")
        context.update({ "main_entity" : main_entity,
                         "main_entity_type": "class"
                         })
    elif type(main_entity) == OntoProperty:
        ontotemplate = open(ontospy.ONTOSPY_VIZ_TEMPLATES + "splitter/splitter_propinfo.html", "r")
        context.update({ "main_entity" : main_entity,
                         "main_entity_type": "property"
                         })
    elif type(main_entity) == OntoSKOSConcept:
        ontotemplate = open(ontospy.ONTOSPY_VIZ_TEMPLATES + "splitter/splitter_conceptinfo.html", "r")
        context.update({ "main_entity" : main_entity,
                         "main_entity_type": "concept"
                         })
    else:
            # if type(main_entity) == Ontology:
        ontotemplate = open(ontospy.ONTOSPY_VIZ_TEMPLATES + "splitter/splitter_ontoinfo.html", "r")


    t = Template(ontotemplate.read())
    c = Context(context)

    rnd = t.render(c)

    return safe_str(rnd)







if __name__ == '__main__':
    """
    > python -m ontospy.viz.viz_splitter_multi

    2016-08-04: # testing bypassing the usual abstract routine so to generate multiple files

    """
    import sys
    try:

        # script for testing - must launch this module direclty eg

        # > python -m ontospy.viz.viz_splitter_multi

        func = locals()["run"] # main func dynamically
        # run_test_viz(func)

        import webbrowser, random

        ontouri = ontospy.get_localontologies()[random.randint(0, 10)] # [0] #
        print("Testing with URI: %s" % ontouri)

        g = ontospy.get_pickled_ontology(ontouri)
        if not g:
            g = ontospy.do_pickle_ontology(ontouri)


        def _saveVizLocally(contents, filename="index.html", path=None):
            if not path:
                filename = ontospy.ONTOSPY_LOCAL_VIZ + "/" + filename
            else:
                filename = os.path.join(path, filename)

            f = open(filename, 'wb')
            f.write(contents)  # python will convert \n to os.linesep
            f.close()  # you can omit in most cases as the destructor will call it

            url = "file://" + filename
            return url

        try:
            ontology = g.ontologies[0]
            uri = ontology.uri
        except:
            ontology = None
            uri = g.graphuri
            
        DEST_FOLDER = "/Users/michele.pasin/Desktop/test/"

        # main index page for graph
        contents = func(g, ontology, uri, None)
        index_url = _saveVizLocally(contents, "index.html", DEST_FOLDER)
            
        for c in g.classes:
            # getting main func dynamically
            contents = func(g, ontology, uri, c)
            _filename = c.slug + ".html"
            url = _saveVizLocally(contents, _filename, DEST_FOLDER)
            
        for c in g.properties:
            # getting main func dynamically
            contents = func(g, ontology, uri, c)
            _filename = c.slug + ".html"
            url = _saveVizLocally(contents, _filename, DEST_FOLDER)


        for c in g.skosConcepts:
            # getting main func dynamically
            contents = func(g, ontology, uri, c)
            _filename = c.slug + ".html"
            url = _saveVizLocally(contents, _filename, DEST_FOLDER)


        if index_url:  # open browser
            import webbrowser
            webbrowser.open(index_url)



        sys.exit(0)

    except KeyboardInterrupt as e: # Ctrl-C
        raise e



