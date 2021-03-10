{
    'name': "Fleet vehicle documents",

    'summary': """Manage fleet vehicle documents and notify before expire date""",

    'description': """
This module allow Fleet managers to manage all kinds of fleet documents and automatic send an email notification 
when a document is about to get expired.

Key Features
============

Document Types Management
-------------------------

* Fleet Manager can define unlimited document types. For example, Proof of ownership, Proof of insurance, etc
* Each document type has the following properties:

    * Name: the name of the document type, which is unique in the system wide
    * Days to Notify: the default value for number of days prior to the expiry for the system to notify about the expiration of the document of this type
    * Description: text field to describe to type
    * Kept by: An information field to indicated whether the original document of this type should be kept by the company or in the vehicle. It is a default value for the document of this type
    * Return Upon Termination: The default value for the documents of this type to indicate if the origin of the document should be return to its owner upon termination

Vehicle Document
-----------------

* Is an Odoo document that allows Fleet manager to manage all the documents related to the vehicle of the company
* Each document contains the following information

    * Doc. Numer: the number/name of the document
    * Kept By: An information field to indicated whether the original document is currently kept by the company or in the vehicle
    * Return Upon Termination: If checked, the original document must be return to its owner. I.e. if the origin is kept by the company, it should be returned in thbe vehicle; if the origin is kept in the vehicle, it should be returned to the company
    * Doc. Manager: the one in the Fleet management department that takes responsibility for managing this document
    * Document Type: Indicate the type of this document (e.g. Proof of ownership, etc)
    * Vehicle: the vehicle to whom this document is related
    * Issue Date: the date on which the document was issued
    * Issued By: linked to a partner record
    * Place of Issue
    * Expire Date: the date on which the document gets expired (if applicable)
    * Days to Notify: number of days to notify before the expiration of the document.
    * Image 1: store a photo of the document
    * Image 2: store another photo of the document
    * PDF: Store the PDF version of the Document
* PDF Viewer: the PDF version can be viewed online without downloads

Vehicle
--------

* Show a stat button on the vehicle form to indicate number of documents related to this vehicle
* Click the button will drive the user to the list of the documents
    
Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    'author': 'Markus Mair',
    'support': 'markusmair77@outlook.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Fleet',
    'version': '1.0.1',

    # any module necessary for this one to work correctly
    'depends': ['fleet', ],

    # always loaded
    'data': [
        'data/document_type_data.xml',
        'data/scheduler_data.xml',
        'data/mail_template_data.xml',
        'security/vehicle_document_security.xml',
        'security/ir.model.access.csv',
        'views/vehicle_document_views.xml',
        'views/vehicle_document_type_views.xml',
        'views/fleet_vehicle_views.xml',
        ],
    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 75,
    'currency': 'EUR',
    'license': 'OPL-1',
}
