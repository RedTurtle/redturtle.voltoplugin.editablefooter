
=====================
Volto Editable Footer
=====================

Add-on that allows to edit title and text for 4 footer columns in Volto.

Features
--------

- Control panel for plone registry to manage columns configuration.
- Restapi view that exposes these settings for Volto.
- Each column is a set of title (textline field) and text (rich text).

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

Only columns populated will be returned by this endpoint.

Control panel
-------------

You can edit settings directly from Volto because the control has been registered on Plone and available with plone.restapi.


Volto integration
-----------------

To use this product in Volto, your Volto project needs to include a new plugin: **ADDRESS_HERE**


You also need to set the right widget in widgets mapping::

    ...
    column_1_text: WysiwygWidget,
    column_2_text: WysiwygWidget,
    column_3_text: WysiwygWidget,
    column_4_text: WysiwygWidget,
    ...

Translations
------------

This product has been translated into

- Italian


Installation
------------

Install redturtle.volto_editablefooter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        redturtle.volto_editablefooter


and then running ``bin/buildout``


Contribute
----------

- Issue Tracker: https://github.com/RedTurtle/redturtle.volto_editablefooter/issues
- Source Code: https://github.com/RedTurtle/redturtle.volto_editablefooter


License
-------

The project is licensed under the GPLv2.

Authors
-------

This product was developed by **RedTurtle Technology** team.

.. image:: https://avatars1.githubusercontent.com/u/1087171?s=100&v=4
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
