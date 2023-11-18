<h1 id="kmap-py">kMap.py</h1>
<p>kMap.py is a python based program for simulation and data analysis in photoemission tomography
(<a href="https://en.wikipedia.org/wiki/Photoemission_orbital_tomography"> https://en.wikipedia.org/wiki/Photoemission_orbital_tomography</a>). The underlying theoretical methodology is described in the following publication:</p>
<p>Dominik Brandstetter, Xiaosheng Yang, Daniel Lüftner, F. Stefan Tautz, and Peter Puschnig, "kMap.py: A Python program for simulation and data analysis in photoemission tomography", Computer Physics Communications 263, 107905 (2021) <a href="https://doi.org/10.1016/j.cpc.2021.107905">https://doi.org/10.1016/j.cpc.2021.107905</a></p>
<p>Please cite this work when using results from kMap.py in your publications.</p>



<h2 id="authors">Authors</h2>
<ul>
<li>Peter Puschnig  (peter.puschnig@uni-graz.at)</li>
<li>Dominik Brandstetter (dominik.brandstetter@uni-graz.at)</li>
</ul>
<p>Download Code from GitHub Page: <a href="https://github.com/brands-d/kMap">https://github.com/brands-d/kMap</a></p>


<h2 id="quick-start">Quick-Start</h2>
<p>Installation:</p>
<pre><code>pip <span class="hljs-keyword">install</span> kMap
</code></pre><p>Usage:</p>
<pre><code><span class="hljs-attribute">python -m kmap</span>
</code></pre><h2 id="detailed-installation-guide-from-source">Detailed installation guide from source</h2>
<p>kMap.py was predominantly developed on and for Linux. There are currently (19.09.2020) no issues on Windows, however, MacOS stands untested so far.</p>
<p>The installation is mostly done via make commands. Because Windows does not support Makefiles natively, this installation guide will differ between Linux and Windows at multiple points. Please follow the part corresponding to your operating system. For Mac users: As MacOS natively support bash, the Linux guide should work fine.</p>
<h3 id="1-install-python">1. Install Python</h3>
<p>Before installing kMap.py, please make sure you have a python version of 3.7 or higher installed. If not, you can get one here</p>
<pre><code><span class="hljs-symbol">https:</span>//www.python<span class="hljs-meta">.org</span>/downloads/
</code></pre><p>With this, you should have pip already installed. If not please install it using this guide (<a href="https://pip.pypa.io/en/stable/installing/">https://pip.pypa.io/en/stable/installing/</a>).</p>
<h3 id="2-clone-git-project">2. Clone Git Project</h3>
<p>Clone the project into a local repository. If you have git installed, simply execute the following command for https:</p>
<pre><code>git <span class="hljs-keyword">clone</span> <span class="hljs-title">https</span>://github.com/brands-d/kMap.git
</code></pre><p>or if you have an ssh connection set up:</p>
<pre><code>git <span class="hljs-keyword">clone</span> <span class="hljs-title">git</span>@github.com:brands-d/kMap.git
</code></pre><p>Alternatively, if don&#39;t have git installed you can download the .zip file here:</p>
<pre><code>https:<span class="hljs-regexp">//gi</span>thub.com<span class="hljs-regexp">/brands-d/</span>kMap<span class="hljs-regexp">/archive/m</span>aster.zip
</code></pre><p>and extract the project into the local directory.</p>
<h3 id="3-virtual-environment">3. Virtual environment</h3>
<p>It is recommended to use a virtual environment to run kMap.py in. If you are using Anaconda or are familiar with venv, please set up a new environment and activate it. Then skip ahead to section 5. Installation. If you don&#39;t want to utilize a virtual environment at all, please also skip ahead to section 5. Installation.</p>
<p>To use a virtual environment please check if you have virtualenv already installed. If not please do so with the following command:</p>
<pre><code>pip <span class="hljs-keyword">install</span> virtualenv
</code></pre><h4 id="linux">Linux</h4>
<p>The following commands will set up a virtual environment inside the kMap&#39;s root directory</p>
<pre><code>make <span class="hljs-built_in">setup</span>
</code></pre><h4 id="windows">Windows</h4>
<p>Please execute the following commands. If your shell does not recognize the &quot;rm&quot; command, replace &quot;rm&quot; with &quot;del&quot;.</p>
<pre><code><span class="hljs-symbol">rm</span> -rf venv <span class="hljs-keyword">build </span>dist *.egg-<span class="hljs-meta">info</span>
<span class="hljs-symbol">python</span> -m venv venv
</code></pre><h3 id="4-activate-enviroment">4. Activate Enviroment</h3>
<p>The environment is set up but needs to be activated manually. ATTENTION: You will need to reactivate the environment for every new shell again. Please follow this point to do so.</p>
<h4 id="linux">Linux</h4>
<pre><code><span class="hljs-keyword">source</span> .<span class="hljs-regexp">/venv/</span>bin<span class="hljs-regexp">/activate</span>
</code></pre><h4 id="windows">Windows</h4>
<pre><code>.<span class="hljs-symbol">\e</span>nv<span class="hljs-symbol">\S</span>cripts<span class="hljs-symbol">\a</span>ctivate
</code></pre><p>To deactivate the environment simply call (both operation systems)</p>
<pre><code><span class="hljs-attribute">deactivate</span>
</code></pre><h3 id="5-installation">5. Installation</h3>
<p>If you skipped section 3. and 4. please make sure you are in the environment you want the packages to be installed in. Additionally, please make sure you are using the latest version of pip as PyQt5 is known to have trouble with older versions. You can (should) upgrade pip using</p>
<pre><code>pip <span class="hljs-keyword">install</span> <span class="hljs-comment">--upgrade pip</span>
</code></pre><p>If you want to have more control over what is happening, please follow the &quot;Manually&quot; section.</p>
<p>The following commands will install kMap.py and all necessary packages inside</p>
<h4 id="linux">Linux</h4>
<pre><code>make <span class="hljs-keyword">install</span>
</code></pre><h4 id="windows">Windows</h4>
<pre><code>python setup<span class="hljs-selector-class">.py</span> install
</code></pre><h3 id="5-testing">5. Testing</h3>
<p>Last please run the tests to check if they come back passing.</p>
<h4 id="linux">Linux</h4>
<pre><code><span class="hljs-keyword">make</span> test-<span class="hljs-keyword">all</span>
</code></pre><h3 id="windows">Windows</h3>
<pre><code>python -m <span class="hljs-keyword">unittest</span> discover
</code></pre><p>It should say something like &quot;OK&quot; at the end. If you see &quot;FAILED&quot; one or more tests came back negative. If that&#39;s the case please make sure you installed kMap.py correctly and retry. If it still fails, please contact one of the authors.</p>
<h2 id="configuration">Configuration</h2>
<p>All configuration files can be found in ./kmap/config. Each configuration file (logging, settings and shortcut) exists in two different versions (xxx_user.ini and xxx_default.ini). DO NOT edit the default version. You can lose all your settings when updating. Instead, copy any settings you want to change into the respective user file and change it there. The user file does not have to contain all settings, but only those you want to be changed.</p>
<p>This can be done inside the GUI under the &quot;Preferences&quot; menu. &quot;Reload Settings&quot; reloads the settings at runtime. Most settings (not all of them) can be changed at run time this way.</p>
<p>Recommended settings to customize:
app - Customize the size the app starts in depending on your resolution.
paths - Customize the search path for data for quicker access.</p>
<h2 id="usage">Usage</h2>
<p>Before running, make sure you are in the correct environment in which you installed kMap.py. If you decided to use the venv kMap.py comes with, this corresponds to 4. Activate Environment.</p>
<p>To start kMap.py simply run</p>
<pre><code><span class="hljs-attribute">python -m kmap</span>
</code></pre><p>Tutorial videos demonstrating the most important features of kMap.py can be found here: <a href="https://www.youtube.com/playlist?list=PLAoZOqtibC5ypO57SU4emdelPzSGQRO8c">https://www.youtube.com/playlist?list=PLAoZOqtibC5ypO57SU4emdelPzSGQRO8c</a> </p>
<h2 id="updating">Updating</h2>
<p>Major releases for kMap.py are distributaed via the PyPI Server (pip install). The source code and all minor updates with it are hosted on GitHub (<a href="https://github.com/brands-d/kMap">https://github.com/brands-d/kMap</a>). If you cloned the project using git executing</p>
<pre><code>git pull origin <span class="hljs-literal">master</span>
</code></pre><p>will update the project to the most recent release.
If you downloaded the .zip file in section 2. Clone Git Project manually, please download it again from the GitHub page and follow the installation instructions. Copy and replace your user settings files from the old version to the new version.</p>
<p>The project is currently structured into a &quot;master&quot; branch (release), a &quot;dev&quot; branch (beta) and various working branches (experimental) usually named after the person working on it. It is not recommended to clone from those branches. </p>
<h2 id="bug-report">Bug Report</h2>
<p>Bug reports are highly appreciated. Please first run the</p>
<pre><code><span class="hljs-attribute">make report</span>
</code></pre><p>command (only Linux, no equivalent for Windows currently). This will create a report.tar.gz file containing relevant files like the log files and your settings. Please add this file to any bug report! (Windows: Until an easy solution is added please attach at the log file (default.log) to your bug report). Please note that this process might take a while since all test will be run.</p>
<p>Simply send this file via E-mail to one of the authors
(dominik.brandstetter@edu.uni-graz.at).</p>
<h2 id="project-structure">Project Structure</h2>
<p>The root folder of the kMap.py source code should contain after successful installation at least the following files and directories:</p>
<ul>
<li>/dist</li>
<li>/docs</li>
<li>/example</li>
<li>/kmap</li>
<li>.gitignore</li>
<li>LICENSE.md</li>
<li>Makefile</li>
<li>README.md</li>
<li>Manifest.in</li>
<li>setup.py</li>
</ul>
<h3 id="-dist">/dist</h3>
<p>Contains the distribution versions of major releases in wheel and tar.gz form.</p>
<h3 id="-docs">/docs</h3>
<p>The /docs subdirectory contains documentation regarding the project. This includes a style guide, class- and package-diagrams as well as a description of the .hdf5 file structure.</p>
<h3 id="-example">/example</h3>
<p>The /example subdirectory contains example data (/example/data) and example scripts (/example/scripts). The scripts are both a show-off what is possible and a tutorial of how to do various things with kMap.py. Check out the file /example/scripts/README for further information.</p>
<h3 id="-kmap">/kmap</h3>
<p>This is the main folder for the program itself. It contains all the code and tests split into the following subdirectories:</p>
<ul>
<li>/config</li>
<li>/controller</li>
<li>/library</li>
<li>/model</li>
<li>/resources</li>
<li>/tests</li>
<li>/ui</li>
</ul>
<p>The source code roughly follows the MVC (model-view-controller) design pattern. However, due to various reasons, this separation is not strictly followed all the time.</p>
<h4 id="-config">/config</h4>
<p>This directory contains all the configuration files as well as the &quot;config&quot; class responsible for loading, parsing and providing the settings throughout the rest of the program.</p>
<h4 id="-controller">/controller</h4>
<p>This directory contains all the controller classes and is somewhat the heart of the kMap.py program.</p>
<p>Pretty much every feature/GUI element has its own controller class. Controller classes (as in MCV) contain everything not suited or possible in model classes or .ui files. They handle the interaction with other elements, signals/slots, creation and destruction, some necessary GUI editing as well as quick and minor calculations.</p>
<h4 id="-library">/library</h4>
<p>This directory contains various base classes.</p>
<p>The most important classes are:</p>
<ul>
<li>misc.py: This file contains various general methods and useful methods used at different parts of kMap.py.</li>
<li>orbital.py: This class is responsible for loading .cube files, calculating momentum maps from the simulation data and providing an easy interface to other parts of the program.</li>
<li>plotdata.py: All image-like data plotted in kMap.py is based on this class. It provides additional core attributes (like axis information) and core functionality like interpolation and smoothing.</li>
<li>sliceddata.py : This class defines sliced-data as a 3D data set with axis information usually constructed out of .hdf5 experimental data.</li>
</ul>
<h4 id="-model">/model</h4>
<p>This directory contains model classes (as in MCV) for various more complex controller classes.</p>
<p>Model classes encapsulate more complex handling of data from the more general organisational matters dealt with by the controller classes themselves. They are completely removed from handling GUI elements or interacting with other elements and only get, store, edit and provide an interface to data. Therefore most controller classes don&#39;t need such a model class.</p>
<h4 id="-resources">/resources</h4>
<p>This directory contains different types of additional resources for the program to run (like the icon image file).</p>
<h4 id="-tests">/tests</h4>
<p>This directory contains all the tests available.</p>
<p>Each file contains one or more test classes based on the unittest module. Run them through the &quot;make test-all&quot; command or individually by &quot;python -m unittest kmap/tests/xxx&quot; where &quot;xxx&quot; denotes the file containing the class you want to test.</p>
<h4 id="-ui">/ui</h4>
<p>This directory contains all the .ui files exported by QtCreator and imported and parsed by the classes in the /controller directory.</p>
<p>The .ui files represent the view part in the MVC pattern. They are auto-generated by QtCreator, a program with an open-source license option to easily and simply create Qt-based GUIs. The files are written in a .xml format and can be opened, viewed and edited by the QtCreator program.</p>
<p>With some exceptions, all GUI related things are defined here (in QtCreator).</p>
