<body>
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
<p>Supported Python version: 3.6 or greater</p><p>You have two ways to integrate with the Copyleaks SDK:</p>
<ul>
<li><b>Recommended</b> - Use the Python Package Manager - <i>Coming soon</i><!--a href="https://pypi.python.org/pypi/copyleaks">PiPy</a-->.
  <br>
  When integrating this way you will automatically be able to update the SDK to its latest version:
<pre>
pip3 install copyleaks
</pre> 

</li>
<li>Download the code from this repository and add it to your project.
</ul>
  <!--p>You can also check out <a href="https://www.youtube.com/watch?v=B2Lck9Pst2M"> this video</a> showing how to use this SDK.</p-->
  <p>Check out the example video <i>Coming soon</i></p>
<h3>Register and Get Your API Key</h3>
 <p>To use the Copyleaks SDK you need to have a Copyleaks account. The registration to Copyleaks is free of charge and quick. <a href="https://copyleaks.com/Account/Register">Signup</a> and confirm your account to finalize your registration.</p>
 <p>Now, generate your personal API key on your dashboard (<a href="https://api.copyleaks.com/businessesapi">Businesses dashboard</a>, <a href="https://api.copyleaks.com/academicapi">Education dashboard</a> or <a href="https://api.copyleaks.com/websitesapi">Websites dashboard</a>) under 'Access Keys'.</p>
 <p>For more information check out our <a href="https://api.copyleaks.com/Guides/HowToUse">API guide</a>.</p>
<h3>Examples</h3>
<a href="https://github.com/Copyleaks/Python-Plagiarism-Checker/blob/master/ExampleAsynchronous.py">ExampleAsynchronous.py</a> is an example of creating a process and getting a completion callback with the results.
Copyleaks API can also be used in synchronous mode, <a href="mailto:Support@Copyleaks.com">Contact us</a> for assistance.
<!--a href="https://github.com/Copyleaks/Python-Plagiarism-Checker/blob/master/ExampleSynchronous.py">ExampleSynchronous.py</a> <a>is an example of creating a process, checking its status and getting the results programmatically.</a-->
<h3>Usage</h3>
<p>Login to your account using your email and api-key.
</p>
<pre>
identity = CopyleaksIdentityApi()
login_response = identity.login('&lt;YOUR_EMAIL_HERE&gt;', '&lt;YOUR_API_KEY_HERE&gt;')
</pre>
<p>Create a unique scan id</p>
<p>The scan id you provide is determined by you it will usually match the scan entity in your system.
Each scan you submit to Copyleaks must have a unique ID and in the following format:<br>
  Allowed characters: all alpha numeric characters and any of the following: <i>!@#$^&*-+%=_()[]{}<>'";:/?.,~`|\</i><br>
  Maximum length: 36 characters</p>
</p>

```
scan_id = uuid.uuid4()

```
<p>Create `ScanProperties` instance to define the properties of your scan.</p>

```

scan_properties = ScanProperties(
        # Add this scan option to your process to submit your document to full scan
        # Other possible values:
        #    eSubmitAction.Index: Upload your content to Copyleaks internal database to be compared against in future scans
        #    eSubmitAction.checkCredits: Check the amount of credits your content submit request will consume
        action = eSubmitAction.Scan,

        # Add this scan option to your process to use sandbox mode.
        # The process will not consume any credits and will return dummy results.
        # For more info about optional headers visit https://api.copyleaks.com/documentation/headers
        sandbox=True,

        # Add callbacks to specify the address on which you want to receive a completion callback and/or onNewResult callback
        # For testing purposes you can use https://github.com/Runscope/requestbin or any other request test server tool
        callbacks = CallbacksSection(

          # An example callback url that will be called on scan completion
          # Best practices:
          #    - It is recommended to add the scan id in the callback url to be able to match it with the submitted scan
          #    - It is recommended to add the '{STATUS}' placeholder, this placeholder will be replaced by copyleaks API with the process status
          #      Possible process statuses (Also available at enum eScanStatus):
          #        - Scanned
          #        - Failed
          #        - CreditsChecked
          #        - Indexed
          completion=f"http://yoursite.here/{scan_id}/{{STATUS}}/completed-callback",

          # An example callback url that will be called when a new result is found
          onNewResult=f"http://yoursite.here/{scan_id}/result-callback"
        )
    )
```
<p>This example shows how to scan a URL:</p>
<pre>
api = CopyleaksScansApi(eProduct.Education, login_response.access_token)
url_document = UrlDocument('https://example.com', scan_properties)
api.submit_url(scan_id, url_document)
</pre>
<p>Available create methods: `submit_url`, `submit_file`, `submit_ocr`.
For more info visit the <a href="https://api.copyleaks.com/swagger">Api Documentation</a>.
</p>
<p>When a new result is found it will tirgger the 'onNewResult' callback, once the scan is completed it will trigger the 'completion' callback</p>
<p>Get the results synchronously:</p>
<pre>results = api.completion(scan_id)</pre>

<h3>Dependencies</h3>
<pre>
pip3 install requests
</pre>
<h3>Read More</h3>
<ul>
<li><a href="https://api.copyleaks.com">API Homepage</a></li>
<li><a href="https://api.copyleaks.com/documentation">API Documentation</a></li>
<li><a href="https://api.copyleaks.com/Guides/HowToUse">Copyleaks API guide</a></li>
<li><a href="https://copyleaks.com">Copyleaks Homepage</a></li>
</ul>
</body>