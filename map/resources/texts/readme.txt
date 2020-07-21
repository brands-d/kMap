<h1 id="map">Map</h1>
<p>Map is a utility project to display, modify and compare momentum maps of
orbitals from ARPES experiments and DFT calculations.</p>
<h2 id="author">Author</h2>
<ul>
<li>Name: Dominik Brandstetter</li>
<li>Email: dominik.brandstetter@edu.uni-graz.at</li>
<li>GitHub Page: <a href="https://github.com/brands-d">https://github.com/brands-d</a></li>
</ul>
<h2 id="installation">Installation</h2>
<h3 id="1-install-python">1. Install Python</h3>
<p>Before installing Map, please make sure you have a python version of 3.7
or higher installed. If not, you can get one here</p>
<a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a>
<p>With this, you should have pip already installed. If not please install
it using this guide (<a href="https://pip.pypa.io/en/stable/installing/">https://pip.pypa.io/en/stable/installing/</a>)</p>
<h3 id="2-clone-git-project">2. Clone Git Project</h3>
<p>Clone the project into a local repository. If you have git installed,
simply execute the following command for https:</p>
<pre><code>git <span class="hljs-keyword">clone</span> <span class="hljs-title">https</span>://github.com/brands-d/Map.git
</code></pre><p>or if you have an ssh connection setup:</p>
<pre><code>git <span class="hljs-keyword">clone</span> <span class="hljs-title">git</span>@github.com:brands-d/Map.git
</code></pre><p>Alternatively, if don&#39;t have git installed (i.e. using Windows) you can
download the .zip file here:</p>
<pre><code>https:<span class="hljs-regexp">//gi</span>thub.com<span class="hljs-regexp">/brands-d/</span>Map<span class="hljs-regexp">/archive/m</span>aster.zip
</code></pre><p>and extract the project into the local directory.</p>
<h3 id="3-virtual-environment">3. Virtual environment</h3>
<p>Map comes with a complete setup of a virtual environment for Map only
which is the cleanest and safest option to use. This, however,
reinstalls packages you might already have in a distinct directory
which can take up some space (currently about 400MB).
If you want to keep storage Map takes up down, or prefer using our own
environment or program (like conda) you can skip 3. and 4. entirely.</p>
<p>If you don&#39;t have virtualenv already installed, please do so with the
following command:</p>
<pre><code>pip <span class="hljs-keyword">install</span> virtualenv
</code></pre><h4 id="linux-macos-probably-">Linux &amp; MacOS (probably)</h4>
<p>The following commands will set up a venv folder inside the Map&#39;s root
directory</p>
<pre><code>make <span class="hljs-built_in">setup</span>
</code></pre><h4 id="windows">Windows</h4>
<p>Windows doesn&#39;t come with make installed. Therefore, you have to execute
the commands manually</p>
<pre><code><span class="hljs-symbol">rm</span> -rf venv <span class="hljs-keyword">build </span>dist *.egg-<span class="hljs-meta">info</span>
<span class="hljs-symbol">python</span> -m venv venv
</code></pre><h3 id="4-activate-enviroment">4. Activate Enviroment</h3>
<p>Next, we need to activate the environment. ATTENTION: You will need to
reactivate the environment for every new shell again. Please follow this
point to do so.</p>
<h4 id="linux-macos-probably-">Linux &amp; MacOS (probably)</h4>
<pre><code><span class="hljs-keyword">source</span> .<span class="hljs-regexp">/venv/</span>bin<span class="hljs-regexp">/activate</span>
</code></pre><h4 id="windows">Windows</h4>
<pre><code>.<span class="hljs-symbol">\e</span>nv<span class="hljs-symbol">\S</span>cripts<span class="hljs-symbol">\a</span>ctivate
</code></pre><p>To deactivate the environment simply call</p>
<pre><code><span class="hljs-attribute">deactivate</span>
</code></pre><h3 id="4-installation">4. Installation</h3>
<p>If you skipped section 3. please make sure you are in the environment
you want the packages to be installed. Additionally, please make sure
you are using the latest version of pip as PyQt5 is known to have
trouble with older versions. You can (should) upgrade pip using</p>
<pre><code>pip <span class="hljs-keyword">install</span> <span class="hljs-comment">--upgrade pip</span>
</code></pre><p>If you want to have more control over what is happening, please
follow the &quot;Manually&quot; section. Recommend only if you know what
you are doing.</p>
<h4 id="linux-macos-probably-">Linux &amp; MacOS (probably)</h4>
<p>The following commands will install Map and all necessary packages
inside</p>
<pre><code>make <span class="hljs-keyword">install</span>
</code></pre><h4 id="windows">Windows</h4>
<p>Again Windows users have to do it manually</p>
<pre><code>python -m pip install -r requirements<span class="hljs-selector-class">.txt</span>
python setup<span class="hljs-selector-class">.py</span> install
</code></pre><h4 id="manually">Manually</h4>
<p>To have more control over what is happening, please install the
packages necessary manually. You can find a list in the
requirements.txt file. Afterwards, run</p>
<pre><code>python setup<span class="hljs-selector-class">.py</span> install
</code></pre><h3 id="5-testing">5. Testing</h3>
<p>Afterwards please run tests to check if they come back passing.</p>
<h4 id="linux">Linux</h4>
<pre><code><span class="hljs-keyword">make</span> test-<span class="hljs-keyword">all</span>
</code></pre><h3 id="windows">Windows</h3>
<pre><code>python -m <span class="hljs-keyword">unittest</span> discover
</code></pre><p>It should say something like &quot;OK&quot; at the end. If you see &quot;FAILED&quot;
one or more test came back negative. If that&#39;s the case please make
sure you installed Map correctly and retry. If it still fails, please
contact the author.</p>
<h2 id="configuration">Configuration</h2>
<p>All configuration files can be found in ./map/resources/config. They are
outside the index of git, which means you can (and have to) edit and
change them directly.</p>
<h2 id="usage">Usage</h2>
<p>Before running, make sure you are in the correct environment, in which
you installed Map. If you decided to use the venv Map comes with, redo 1. of the installation instruction.</p>
<p>To start Map simply run</p>
<h3 id="linux-macos-probably-">Linux &amp; MacOS (probably)</h3>
<pre><code>make <span class="hljs-keyword">run</span><span class="bash"></span>
</code></pre><h3 id="windows">Windows</h3>
<pre><code><span class="hljs-keyword">python</span> -<span class="hljs-keyword">m</span> <span class="hljs-keyword">map</span>
</code></pre>
<h2 id="bug report">Bug Report</h2>
<p>Bug reports are highly appreciated. Please first run</p>
<pre><code>make <span class="hljs-keyword">report</span><span class="bash"></span></pre>
<p>command (only Linux and maybe MacOS, no equivalent for Windows
currently). This will create a report.tar.gz file containing relevant
files like the log files and your settings. Please add this file to any
bug report! (Windows: Until a easy solution is added please attach at
least the log file (default.log) to your bug report).
Please note that this process might take a while since all test will be
run.</p>
<p>Simply send this file via E-mail to author
(dominik.brandstetter@edu.uni-graz.at).</p>