<h2>Copyleaks Python SDK</h2>
<p>
Copyleaks SDK is a simple framework that allows you to scan textual content for plagiarism and trace content distribution online, using the <a href="https://api.copyleaks.com">Copyleaks plagiarism checker cloud</a>.
</p>
<p>
Detect plagiarism using Copyleaks SDK in:  
<ul>
<li>Online content and webpages</li>
<li>Local and cloud files (<a href=https://api.copyleaks.com/GeneralDocumentation/TechnicalSpecifications#supportedfiletypes">see supported files</a>)</li>
<li>Free text</li>
<li>OCR (Optical Character Recognition) - scanning pictures with textual content (<a href="https://api.copyleaks.com/GeneralDocumentation/TechnicalSpecifications#supportedfiletypes">see supported files</a>)</li>
</ul>
</p>
<h3>Installation</h3>
<p>Supported Python version: 3.</p><p>You have two ways to integrate with the Copyleaks SDK:</p>
<ul>
<li><b>Recommended</b> - Use the Python Package Manager - <a href="https://pypi.python.org/pypi/copyleaks">PiPy</a>.
  <br>
  When integrating this way you will automatically be able to update the SDK to its latest version:
<pre>
pip3 install copyleaks
</pre>
</li>
<li>Download the code from this repository and add it to your project.
</ul>
  <p>You can also check out <a href="https://www.youtube.com/watch?v=B2Lck9Pst2M"> this video</a> showing how to use this SDK.</p>
<h3>Register and Get Your API Key</h3>
 <p>To use the Copyleaks SDK you need to have a Copyleaks account. The registration to Copyleaks is free of charge and quick. <a href="https://copyleaks.com/Account/Register">Signup</a> and confirm your account to finalize your registration.</p>
 <p>Now, generate your personal API key on your dashboard (<a href="https://api.copyleaks.com/businessesapi">Businesses dashboard</a>, <a href="https://api.copyleaks.com/academicapi">Education dashboard</a> or <a href="https://api.copyleaks.com/websitesapi">Websites dashboard</a>) under 'Access Keys'.</p>
 <p>For more information check out our <a href="https://api.copyleaks.com/Guides/HowToUse">API guide</a>.</p>
<h3>Examples</h3>
Get started using this API with this examples. <a href="https://github.com/Copyleaks/Python-Plagiarism-Checker/blob/master/ExampleAsynchronous.py">ExampleAsynchronous.py</a> is an example of creating a process and getting a completion callback with the results. <a href="https://github.com/Copyleaks/Python-Plagiarism-Checker/blob/master/ExampleSynchronous.py">ExampleSynchronous.py</a> is an example of creating a process, checking its status and getting the results programmatically.
<h3>Usage</h3>
<p>Login to your account using your email, api-key and the product that you would like to use.
</p>
<pre>
from copyleaks.copyleakscloud import CopyleaksCloud
from copyleaks.product import Product
cloud = CopyleaksCloud(Product.Education, 'YOUR_EMAIL_HERE', 'YOUR_API_KEY_HERE')# You can change the product.
</pre>
<p>Create `ProcessOptions` instance to add custom headers to your request. For more info see the <a href="https://github.com/Copyleaks/Python-Plagiarism-Checker#configuration">Configuration</a> section below.
</p>
<pre>
options = ProcessOptions()
options.setSandboxMode(True)  # Scan will not consume any credits and will return dummy results.
options.setHttpCallback("http://yoursite.here/callback") # Recieve a completion callback with the results. For testing purposes we recommend using http://requestb.in
</pre>
<p>This example shows how to scan a URL using the line:</p>
<pre>process = cloud.createByUrl('http://python.org', options)</pre>
<p>Available create methods: `createByUrl`, `createByFile`, `createByText`, `createByOcr` and `createByFiles`.
For more info visit the <a href="https://api.copyleaks.com/documentation">Api Documentation</a>.
</p>
<p>If you don't wish to use callbacks you can check the process status and get the process results.</p>
<p>Check process status:
</p>
<pre>
[iscompleted, percents] = process.isCompleted()
</pre>
<p>Get the results:</p>
<pre>results = process.getResults()</pre>
<h3>Configuration</h3>
<p>Custumize your process using this optional headers. For more information visit <a href="https://api.copyleaks.com/documentation/headers">Optional Request Headers</a>
</p>
<pre>
options = ProcessOptions()
options.setSandboxMode(True) # Scan will not consume any credits and will return dummy results.
options.setHttpCallback("http://yoursite.here/callback") # Recieve a completion callback. For testing purposes we recommend using http://requestb.in
options.setHttpInProgressResultsCallback("http://yoursite.here/callback/results")
options.setEmailCallback("Your@email.com")
options.setCustomFields({'Custom': 'field'})
options.setAllowPartialScan(True)
options.setCompareDocumentsForSimilarity(True)  # Available only on compareByFiles
options.setImportToDatabaseOnly(True)  # Available only on Education API
</pre>
<h3>Dependencies</h3>
<pre>
pip3 install requests
pip3 install python-dateutil
pip3 install enum34
</pre>
<h3>Read More</h3>
<ul>
<li><a href="https://api.copyleaks.com">API Homepage</a></li>
<li><a href="https://api.copyleaks.com/documentation">API Documentation</a></li>
<li><a href="https://api.copyleaks.com/Guides/HowToUse">Copyleaks API guide</a></li>
<li><a href="https://copyleaks.com">Copyleaks Homepage</a></li>
</ul>
