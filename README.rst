
=====================
Volto Editable Footer
=====================

Add-on that allows to edit footer columns in Volto.

Features
--------

- Control panel for plone registry to manage columns configuration.
- Restapi view that exposes these settings for Volto.

This addon only add a registry entry where store some configuration data. You need to provide
the edit interface in your Volto theme.

Volto endpoint
--------------

Anonymous users can't access registry resources by default with plone.restapi (there is a special permission).

To avoid enabling registry access to everyone, this package exposes a dedicated restapi route with the infos to draw the menu: *@footer-columns*::

    > curl -i http://localhost:8080/Plone/@footer-columns -H 'Accept: application/json'


The response is something similar to this::

    [
        {
            'text': {'data': '<span>foo</span>'},
            'title': 'First column'
        },
        {
            'text': {'content-type': 'text/html', 'data': ''},
            'title': 'Second column'
        }
    ]


Control panel
-------------

You can edit settings directly from Volto because the control has been registered on Plone and available with plone.restapi.


Volto integration
-----------------

To use this product in Volto, your Volto project needs to include a new plugin: volto-editablefooter_.

.. _volto-editablefooter: https://github.com/RedTurtle/volto-editablefooter


Translations
------------

This product has been translated into

- Italian


Installation
------------

Install redturtle.voltoplugin.editablefooter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        redturtle.voltoplugin.editablefooter


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/RedTurtle/redturtle.voltoplugin.editablefooter/issues
- Source Code: https://github.com/RedTurtle/redturtle.voltoplugin.editablefooter


License
-------

The project is licensed under the GPLv2.

Authors
-------

This product was developed by **RedTurtle Technology** team.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
