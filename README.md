## Copyleaks Python SDK

Copyleaks SDK is a simple framework that allows you to scan textual content for plagiarism and trace content distribution online, using the [Copyleaks plagiarism checker cloud](https://api.copyleaks.com).

Detect plagiarism using Copyleaks SDK in:

*   Online content and webpages
*   Local and cloud files ([see supported files](https://api.copyleaks.com/GeneralDocumentation/TechnicalSpecifications#supportedfiletypes"))
*   Free text
*   OCR (Optical Character Recognition) - scanning pictures with textual content ([see supported files](https://api.copyleaks.com/GeneralDocumentation/TechnicalSpecifications#supportedfiletypes))

### Installation

Supported Python version: 3.

You have two ways to integrate with the Copyleaks SDK:

* **Recommended** - Use the Python Package Manager - [PiPy](https://pypi.python.org/pypi/copyleaks).  
    When integrating this way you will automatically be able to update the SDK to its latest version:

    <pre>pip3 install copyleaks
    </pre>

*   Download the code from this repository and add it to your project.

### Register and Get Your API Key

To use the Copyleaks SDK you need to have a Copyleaks account. The registration to Copyleaks is free of charge and quick. [Sign up](https://api.copyleaks.com/?register=true) and confirm your account to finalize your registration.

Now, generate your personal API key on your [dashboard](https://api.copyleaks.com/dashboard) under 'API Access Credentials'.

For more information check out our [API guide](https://api.copyleaks.com/documentation/v3).

### Examples

See the [example.py](https://github.com/Copyleaks/Python-Plagiarism-Checker/blob/master/example.py) file.

* To change the Identity server URI (default:"https://id.copyleaks.com"):

<pre>Copyleaks.set_identity_uri("your identity server uri");
</pre>

* To change the API server URI (default:"https://api.copyleaks.com"):

<pre>Copyleaks.set_api_uri("your api server uri");
</pre>

### Dependencies

<pre>pip3 install requests pytz python-dateutil
</pre>

### Read More

*   [API Homepage](https://api.copyleaks.com)
*   [API Documentation](https://api.copyleaks.com/documentation)
*   [Plagiarism Report](https://github.com/Copyleaks/plagiarism-report)
