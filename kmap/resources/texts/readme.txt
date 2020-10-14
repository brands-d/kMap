<h1 class="code-line" data-line-start=0 data-line-end=1 ><a id="kMappy_0"></a>kMap.py</h1>
<p class="has-line-data" data-line-start="1" data-line-end="2">kMap.py is a python based program for simulation and data analysis in photoemission tomography. When using results from kMap.py in scientific publications, please cite the following paper: <a href="https://arxiv.org/abs/2009.13099"> https://arxiv.org/abs/2009.13099</p>
<p class="has-line-data" data-line-start="3" data-line-end="4">It provides an easy-to-use graphical user interface powered by PyQt5 to simulate photoemission momentum maps of molecular orbitals and to perform a one-to-one comparison between simulation and experiment. For this kMap.py provides tools like line- or region-restricted intensity scans/plots, interpolation capabilities, adjustable simulation parameters (like orientation, final state kinetic energy and polarization state of the incident light field) as well as an interface to powerful least-square fits between simulation and experiment to quickly determine optimal parameters.</p>
<p class="has-line-data" data-line-start="5" data-line-end="6">GitHub Page: <a href="https://github.com/brands-d/kMap">https://github.com/brands-d/kMap</a></p>
<h2 class="code-line" data-line-start=7 data-line-end=8 ><a id="Authors_7"></a>Authors</h2>
<ul>
<li class="has-line-data" data-line-start="8" data-line-end="9">Peter Puschnig, Assoz. Prof. Dipl.-Ing. Dr. (<a href="mailto:peter.puschnig@uni-graz.at">peter.puschnig@uni-graz.at</a>)</li>
<li class="has-line-data" data-line-start="9" data-line-end="11">Dominik Brandstetter, BSc. (<a href="mailto:dominik.brandstetter@edu.uni-graz.at">dominik.brandstetter@edu.uni-graz.at</a>)</li>
</ul>
<h2 class="code-line" data-line-start=11 data-line-end=12 ><a id="Installation_11"></a>Installation</h2>
<p class="has-line-data" data-line-start="12" data-line-end="13">kMap.py was predominantly developed on and for Linux. There are currently (19.09.2020) no issues on Windows, however, MacOS stands untested so far.</p>
<p class="has-line-data" data-line-start="14" data-line-end="15">The installation is mostly done via make commands. Because Windows does not support Makefiles natively, this installation guide will differ between Linux and Windows at multiple points. Please follow the part corresponding to your operating system. For Mac users: As MacOS natively support bash, the Linux guide should work fine.</p>
<h3 class="code-line" data-line-start=16 data-line-end=17 ><a id="1_Install_Python_16"></a>1. Install Python</h3>
<p class="has-line-data" data-line-start="17" data-line-end="18">Before installing kMap.py, please make sure you have a python version of 3.7 or higher installed. If not, you can get one here</p>
<pre><code>https://www.python.org/downloads/
</code></pre>
<p class="has-line-data" data-line-start="21" data-line-end="22">With this, you should have pip already installed. If not please install it using this guide (<a href="https://pip.pypa.io/en/stable/installing/">https://pip.pypa.io/en/stable/installing/</a>).</p>
<h3 class="code-line" data-line-start=23 data-line-end=24 ><a id="2_Clone_Git_Project_23"></a>2. Clone Git Project</h3>
<p class="has-line-data" data-line-start="24" data-line-end="25">Clone the project into a local repository. If you have git installed, simply execute the following command for https:</p>
<pre><code>git clone https://github.com/brands-d/kMap.git
</code></pre>
<p class="has-line-data" data-line-start="28" data-line-end="29">or if you have an ssh connection set up:</p>
<pre><code>git clone git@github.com:brands-d/kMap.git
</code></pre>
<p class="has-line-data" data-line-start="32" data-line-end="33">Alternatively, if don’t have git installed you can download the .zip file here:</p>
<pre><code>https://github.com/brands-d/kMap/archive/master.zip
</code></pre>
<p class="has-line-data" data-line-start="36" data-line-end="37">and extract the project into the local directory.</p>
<h3 class="code-line" data-line-start=38 data-line-end=39 ><a id="3_Virtual_environment_38"></a>3. Virtual environment</h3>
<p class="has-line-data" data-line-start="39" data-line-end="40">It is recommended to use a virtual environment to run kMap.py in. If you are using Anaconda or are familiar with venv, please set up a new environment and activate it. Then skip ahead to section 5. Installation. If you don’t want to utilize a virtual environment at all, please also skip ahead to section 5. Installation.</p>
<p class="has-line-data" data-line-start="41" data-line-end="42">To use a virtual environment please check if you have virtualenv already installed. If not please do so with the following command:</p>
<pre><code>pip install virtualenv
</code></pre>
<h4 class="code-line" data-line-start=45 data-line-end=46 ><a id="Linux_45"></a>Linux</h4>
<p class="has-line-data" data-line-start="46" data-line-end="47">The following commands will set up a virtual environment inside the kMap’s root directory</p>
<pre><code>make setup
</code></pre>
<h4 class="code-line" data-line-start=50 data-line-end=51 ><a id="Windows_50"></a>Windows</h4>
<p class="has-line-data" data-line-start="51" data-line-end="52">Please execute the following commands. If your shell does not recognize the “rm” command, replace “rm” with “del”.</p>
<pre><code>rm -rf venv build dist *.egg-info
python -m venv venv
</code></pre>
<h3 class="code-line" data-line-start=56 data-line-end=57 ><a id="4_Activate_Enviroment_56"></a>4. Activate Enviroment</h3>
<p class="has-line-data" data-line-start="57" data-line-end="58">The environment is set up but needs to be activated manually. ATTENTION: You will need to reactivate the environment for every new shell again. Please follow this point to do so.</p>
<h4 class="code-line" data-line-start=59 data-line-end=60 ><a id="Linux_59"></a>Linux</h4>
<pre><code>source ./venv/bin/activate
</code></pre>
<h4 class="code-line" data-line-start=62 data-line-end=63 ><a id="Windows_62"></a>Windows</h4>
<pre><code>.\env\Scripts\activate
</code></pre>
<p class="has-line-data" data-line-start="65" data-line-end="66">To deactivate the environment simply call (both operation systems)</p>
<pre><code>deactivate
</code></pre>
<h3 class="code-line" data-line-start=69 data-line-end=70 ><a id="5_Installation_69"></a>5. Installation</h3>
<p class="has-line-data" data-line-start="70" data-line-end="71">If you skipped section 3. and 4. please make sure you are in the environment you want the packages to be installed in. Additionally, please make sure you are using the latest version of pip as PyQt5 is known to have trouble with older versions. You can (should) upgrade pip using</p>
<pre><code>pip install --upgrade pip
</code></pre>
<p class="has-line-data" data-line-start="74" data-line-end="75">If you want to have more control over what is happening, please follow the “Manually” section.</p>
<p class="has-line-data" data-line-start="76" data-line-end="77">The following commands will install kMap.py and all necessary packages inside</p>
<h4 class="code-line" data-line-start=78 data-line-end=79 ><a id="Linux_78"></a>Linux</h4>
<pre><code>make install
</code></pre>
<h4 class="code-line" data-line-start=81 data-line-end=82 ><a id="Windows_81"></a>Windows</h4>
<pre><code>python -m pip install -r requirements.txt
python setup.py install
</code></pre>
<h4 class="code-line" data-line-start=85 data-line-end=86 ><a id="Manually_85"></a>Manually</h4>
<p class="has-line-data" data-line-start="86" data-line-end="87">To have more control over what is happening, please install the packages necessary manually. You can find a list in the requirements.txt file. Afterwards, run</p>
<pre><code>python setup.py install
</code></pre>
<h3 class="code-line" data-line-start=90 data-line-end=91 ><a id="5_Testing_90"></a>5. Testing</h3>
<p class="has-line-data" data-line-start="91" data-line-end="92">Last please run the tests to check if they come back passing.</p>
<h4 class="code-line" data-line-start=93 data-line-end=94 ><a id="Linux_93"></a>Linux</h4>
<pre><code>make test-all
</code></pre>
<h3 class="code-line" data-line-start=96 data-line-end=97 ><a id="Windows_96"></a>Windows</h3>
<pre><code>python -m unittest discover
</code></pre>
<p class="has-line-data" data-line-start="99" data-line-end="100">It should say something like “OK” at the end. If you see “FAILED” one or more tests came back negative. If that’s the case please make sure you installed kMap.py correctly and retry. If it still fails, please contact one of the authors.</p>
<h2 class="code-line" data-line-start=101 data-line-end=102 ><a id="Configuration_101"></a>Configuration</h2>
<p class="has-line-data" data-line-start="102" data-line-end="103">All configuration files can be found in ./kmap/resources/config. Each configuration file (logging, settings and shortcut) exists in two different versions (xxx_user.ini and xxx_default.ini). DO NOT edit the default version. You can lose all your settings when updating. Instead, copy any settings you want to change into the respective user file and change it there. The user file does not have to contain all settings, but only those you want to be changed.</p>
<p class="has-line-data" data-line-start="104" data-line-end="105">This can be done inside the GUI under the “Preferences” menu. “Reload Settings” reloads the settings at runtime. Most settings (not all of them) can be changed at run time this way.</p>
<p class="has-line-data" data-line-start="106" data-line-end="109">Recommended settings to customize:<br>
app - Customize the size the app starts in depending on your resolution.<br>
paths - Customize the search path for data for quicker access.</p>
<h2 class="code-line" data-line-start=110 data-line-end=111 ><a id="Usage_110"></a>Usage</h2>
<p class="has-line-data" data-line-start="111" data-line-end="112">Before running, make sure you are in the correct environment in which you installed kMap.py. If you decided to use the venv kMap.py comes with, this corresponds to 4. Activate Environment.</p>
<p class="has-line-data" data-line-start="113" data-line-end="114">To start kMap.py simply run</p>
<h3 class="code-line" data-line-start=115 data-line-end=116 ><a id="Linux_115"></a>Linux</h3>
<pre><code>make run
</code></pre>
<h3 class="code-line" data-line-start=118 data-line-end=119 ><a id="Windows_118"></a>Windows</h3>
<pre><code>python -m kmap
</code></pre>
<p class="has-line-data" data-line-start="121" data-line-end="122">Tutorial videos demonstrating the most important features of kMap.py can be found here: <a href="https://www.youtube.com/playlist?list=PLAoZOqtibC5ypO57SU4emdelPzSGQRO8c">https://www.youtube.com/playlist?list=PLAoZOqtibC5ypO57SU4emdelPzSGQRO8c</a></p>
<h2 class="code-line" data-line-start=123 data-line-end=124 ><a id="Updating_123"></a>Updating</h2>
<p class="has-line-data" data-line-start="124" data-line-end="125">kMap.py is currently distributed like a regular git project hosted on GitHub (<a href="https://github.com/brands-d/kMap">https://github.com/brands-d/kMap</a>). If you cloned the project using git executing</p>
<pre><code>git pull origin master
</code></pre>
<p class="has-line-data" data-line-start="128" data-line-end="130">will update the project to the most recent release.<br>
If you downloaded the .zip file in section 2. Clone Git Project manually, please download it again from the GitHub page and follow the installation instructions. Copy and replace your user settings files from the old version to the new version.</p>
<p class="has-line-data" data-line-start="131" data-line-end="132">The project is currently structured into a “master” branch (release), a “dev” branch (beta) and various working branches (experimental) usually named after the person working on it. It is not recommended to clone from those branches.</p>
<h2 class="code-line" data-line-start=133 data-line-end=134 ><a id="Bug_Report_133"></a>Bug Report</h2>
<p class="has-line-data" data-line-start="134" data-line-end="135">Bug reports are highly appreciated. Please first run the</p>
<pre><code>make report
</code></pre>
<p class="has-line-data" data-line-start="138" data-line-end="139">command (only Linux, no equivalent for Windows currently). This will create a report.tar.gz file containing relevant files like the log files and your settings. Please add this file to any bug report! (Windows: Until an easy solution is added please attach at the log file (default.log) to your bug report). Please note that this process might take a while since all test will be run.</p>
<p class="has-line-data" data-line-start="140" data-line-end="142">Simply send this file via E-mail to one of the authors<br>
(<a href="mailto:dominik.brandstetter@edu.uni-graz.at">dominik.brandstetter@edu.uni-graz.at</a>).</p>
<h2 class="code-line" data-line-start=143 data-line-end=144 ><a id="Project_Structure_143"></a>Project Structure</h2>
<p class="has-line-data" data-line-start="144" data-line-end="145">The root folder of the kMap.py source code should contain after successful installation at least the following files and directories:</p>
<ul>
<li class="has-line-data" data-line-start="145" data-line-end="146">/docs</li>
<li class="has-line-data" data-line-start="146" data-line-end="147">/example</li>
<li class="has-line-data" data-line-start="147" data-line-end="148">/kmap</li>
<li class="has-line-data" data-line-start="148" data-line-end="149">.gitignore</li>
<li class="has-line-data" data-line-start="149" data-line-end="150">LICENSE.md</li>
<li class="has-line-data" data-line-start="150" data-line-end="151">Makefile</li>
<li class="has-line-data" data-line-start="151" data-line-end="152">README.md</li>
<li class="has-line-data" data-line-start="152" data-line-end="153">requirements.txt</li>
<li class="has-line-data" data-line-start="153" data-line-end="155">setup.py</li>
</ul>
<h3 class="code-line" data-line-start=155 data-line-end=156 ><a id="docs_155"></a>/docs</h3>
<p class="has-line-data" data-line-start="156" data-line-end="157">The /docs subdirectory contains documentation regarding the project. This includes a style guide, class- and package-diagrams as well as a description of the .hdf5 file structure.</p>
<h3 class="code-line" data-line-start=158 data-line-end=159 ><a id="example_158"></a>/example</h3>
<p class="has-line-data" data-line-start="159" data-line-end="160">The /example subdirectory contains example data (/example/data) and example scripts (/example/scripts). The scripts are both a show-off what is possible and a tutorial of how to do various things with kMap.py. Check out the file /example/scripts/README for further information.</p>
<h3 class="code-line" data-line-start=161 data-line-end=162 ><a id="kmap_161"></a>/kmap</h3>
<p class="has-line-data" data-line-start="162" data-line-end="163">This is the main folder for the program itself. It contains all the code and tests split into the following subdirectories:</p>
<ul>
<li class="has-line-data" data-line-start="163" data-line-end="164">/config</li>
<li class="has-line-data" data-line-start="164" data-line-end="165">/controller</li>
<li class="has-line-data" data-line-start="165" data-line-end="166">/library</li>
<li class="has-line-data" data-line-start="166" data-line-end="167">/model</li>
<li class="has-line-data" data-line-start="167" data-line-end="168">/resources</li>
<li class="has-line-data" data-line-start="168" data-line-end="169">/tests</li>
<li class="has-line-data" data-line-start="169" data-line-end="171">/ui</li>
</ul>
<p class="has-line-data" data-line-start="171" data-line-end="172">The source code roughly follows the MVC (model-view-controller) design pattern. However, due to various reasons, this separation is not strictly followed all the time.</p>
<h4 class="code-line" data-line-start=173 data-line-end=174 ><a id="config_173"></a>/config</h4>
<p class="has-line-data" data-line-start="174" data-line-end="175">This directory contains all the configuration files as well as the “config” class responsible for loading, parsing and providing the settings throughout the rest of the program.</p>
<h4 class="code-line" data-line-start=176 data-line-end=177 ><a id="controller_176"></a>/controller</h4>
<p class="has-line-data" data-line-start="177" data-line-end="178">This directory contains all the controller classes and is somewhat the heart of the kMap.py program.</p>
<p class="has-line-data" data-line-start="179" data-line-end="180">Pretty much every feature/GUI element has its own controller class. Controller classes (as in MCV) contain everything not suited or possible in model classes or .ui files. They handle the interaction with other elements, signals/slots, creation and destruction, some necessary GUI editing as well as quick and minor calculations.</p>
<h4 class="code-line" data-line-start=181 data-line-end=182 ><a id="library_181"></a>/library</h4>
<p class="has-line-data" data-line-start="182" data-line-end="183">This directory contains various base classes.</p>
<p class="has-line-data" data-line-start="184" data-line-end="185">The most important classes are:</p>
<ul>
<li class="has-line-data" data-line-start="185" data-line-end="186">misc.py: This file contains various general methods and useful methods used at different parts of kMap.py.</li>
<li class="has-line-data" data-line-start="186" data-line-end="187">orbital.py: This class is responsible for loading .cube files, calculating momentum maps from the simulation data and providing an easy interface to other parts of the program.</li>
<li class="has-line-data" data-line-start="187" data-line-end="188">plotdata.py: All image-like data plotted in kMap.py is based on this class. It provides additional core attributes (like axis information) and core functionality like interpolation and smoothing.</li>
<li class="has-line-data" data-line-start="188" data-line-end="190">sliceddata.py: This class defines sliced-data as a 3D data set with axis information usually constructed out of .hdf5 experimental data.</li>
</ul>
<h4 class="code-line" data-line-start=190 data-line-end=191 ><a id="model_190"></a>/model</h4>
<p class="has-line-data" data-line-start="191" data-line-end="192">This directory contains model classes (as in MCV) for various more complex controller classes.</p>
<p class="has-line-data" data-line-start="193" data-line-end="194">Model classes encapsulate more complex handling of data from the more general organisational matters dealt with by the controller classes themselves. They are completely removed from handling GUI elements or interacting with other elements and only get, store, edit and provide an interface to data. Therefore most controller classes don’t need such a model class.</p>
<h4 class="code-line" data-line-start=195 data-line-end=196 ><a id="resources_195"></a>/resources</h4>
<p class="has-line-data" data-line-start="196" data-line-end="197">This directory contains different types of additional resources for the program to run (like the icon image file).</p>
<h4 class="code-line" data-line-start=198 data-line-end=199 ><a id="tests_198"></a>/tests</h4>
<p class="has-line-data" data-line-start="199" data-line-end="200">This directory contains all the tests available.</p>
<p class="has-line-data" data-line-start="201" data-line-end="202">Each file contains one or more test classes based on the unittest module. Run them through the “make test-all” command or individually by “python -m unittest kmap/tests/xxx” where “xxx” denotes the file containing the class you want to test.</p>
<h4 class="code-line" data-line-start=203 data-line-end=204 ><a id="ui_203"></a>/ui</h4>
<p class="has-line-data" data-line-start="204" data-line-end="205">This directory contains all the .ui files exported by QtCreator and imported and parsed by the classes in the /controller directory.</p>
<p class="has-line-data" data-line-start="206" data-line-end="207">The .ui files represent the view part in the MVC pattern. They are auto-generated by QtCreator, a program with an open-source license option to easily and simply create Qt-based GUIs. The files are written in a .xml format and can be opened, viewed and edited by the QtCreator program.</p>
<p class="has-line-data" data-line-start="208" data-line-end="209">With some exceptions, all GUI related things are defined here (in QtCreator).</p>