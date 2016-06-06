<h2>Copyleaks Python SDK</h2>
<p>
Copyleaks SDK is a simple framework that allows you to scan textual content for plagiarism and trace content distribution online, using the <a href="https://copyleaks.com">Copyleaks plagiarism checker cloud</a>.
</p>
<p>
Detect plagiarism using Copyleaks SDK in:  
<ul>
<li>Online content and webpages</li>
<li>Local and cloud files (<a href=https://api.copyleaks.com/Documentation/TechnicalSpecifications/#non-textual-formats">see supported files</a>)</li>
<li>OCR (Optical Character Recognition) - scanning pictures with textual content (<a href="https://api.copyleaks.com/Documentation/TechnicalSpecifications/#ocr-formats">see supported files</a>)</li>
</ul>
</p>
<h3>Integration</h3>
<p>You have two ways to integrate with the Copyleaks SDK:</p>
<ul>
<li><b>Recommended</b> - Use the Python Package Manager - <a href="https://pypi.python.org/pypi/copyleaks">PiPy</a>.
  <br>
  When integrating this way you will automatically be able to update the SDK to its latest version:
<pre>
pip install copyleaks
</pre>
</li>
<li>Download the code from this repository and add it to your project.
</ul>
<h3>Register and Get Your API Key</h3>
 <p>To use the Copyleaks SDK you need to have a Copyleaks account. The registration to Copyleaks is free of charge and quick. <a href="https://copyleaks.com/Account/Register">Signup</a> and confirm your account to finalize your registration.</p>
 <p>Now, you can generate your personal API key. Do so by loging into your <a href="https://api.copyleaks.com/Home/Dashboard">dashboard</a>, and under 'Access Keys' you will be able to see and generate your API keys.</p>
 <p>For more information check out our <a href="https://api.copyleaks.com/Guides/HowToUse">API guide</a>.</p>
<h3>Example</h3>
<p><a href="https://github.com/Copyleaks/Python-Plagiarism-Checker/blob/master/copyleaks/main.py">Main.py</a> will show you how to scan for plagiarism in the URL: 'http://python.com'. All you have to do is to update the following line with your email and API key:
</p>
<pre>
cloud = CopyleaksCloud('YOUR_EMAIL_HERE', 'YOUR_API_KEY_HERE')
</pre>

<p>This example shows how to scan a URL using the line:</p>
<pre> process = cloud.createByUrl('http://python.com', options)</pre>
<p>You can change 'createByURL' with 'creatByFile' to scan local files:</p>
<pre> process = cloud.createByFile('test.txt', options) </pre>
<p>or with 'createByOCR to scan local images containing text:</p>
<pre>process = cloud.createByOcr('ocr-example.jpg', eOcrLanguage.English, options)</pre>
<h3>Read More</h3>
<ul>
<li><a href="https://api.copyleaks.com/Guides/HowToUse">Copyleaks API guide</a></li>
<li><a href="https://api.copyleaks.com/Documentation">Copyleaks API documentation</a></li>
</ul>

