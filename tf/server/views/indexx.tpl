<html> 
    <head>
        <meta charset="utf-8"/>
        <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
        <title>TF {{dataSource}}-{{jobName}}</title>
        <meta name="application-name" content="Text-Fabric Search Box"/>
        <link rel="shortcut icon" href="/server/static/favicon.ico">
        <link rel="stylesheet" href="/server/static/mainx.css"/>
        <link rel="stylesheet" href="/server/static/fontawesome.css">
        {{!css}}
    </head>
    <body>
        <form id="go" method="post" enctype="multipart/form-data">
        <input type="hidden" id="appName" name="appName" value="{{dataSource}}"/>
        <div class="page">
            <div id="sidebar">
                <div status="about">
                    <a href="#"><img class="icon" src="/server/static/icon.png"/></a>
                </div>
                <div status="help">
                    <a href="#">Help</a>
                </div>
                <div status="jobs">
                    <a href="#">Jobs</a>
                </div>
                <div status="options">
                    <a href="#">Options</a>
                </div>
                <div status="export">
                    <a href="#">Export</a>
                </div>
            </div>
            <div id="sidebarcont">
                <input type="hidden" id="side" name="side" value="{{side}}"/>
                <div status="about">
                    <div>
                        <p><a target="_blank" href="https://github.com/Dans-labs/text-fabric">Text-Fabric</a> is made by
                           <a target="_blank" href="https://dans.knaw.nl/en/about/organisation-and-policy/staff/roorda">Dirk Roorda</a>,
                           <a target="_blank" href="https://dans.knaw.nl/en">DANS (Data Archiving and Networked Services</a>
                        </p>
                    </div>
                    <div><img class="mainlogo" src="/server/static/dans.png"/></div>
                </div>
                <div status="jobs">
                    <input
                        id="jobh" type="hidden" name="jobName"
                        value="{{jobName}}"
                    />
                    <p class="ilab">This is job
                        <select class="" id="jchange">
                        </select>
                    </p>
                    <div>
                        <button
                            class="fa fa-plus" type="submit" id="jnew"
                            title="start a fresh job"
                        ></button>
                        <button
                            class="fa fa-file-import" type="button" id="jopen"
                            title="upload a job and open it"
                        ></button>
                        <button
                            class="fa fa-window-restore" type="submit"
                            formtarget="_blank"
                            title="open this job in a new tab"
                        ></button>
                        <button
                            class="fa fa-edit" type="submit" id="jrename"
                            title="rename this job"
                        > </button>
                        <button
                            class="fa fa-times" type="submit" id="jclear"
                            title="clear values of this job"
                        ></button>
                        <button
                            class="fa fa-trash" type="submit" id="jdelete"
                            title="delete this job"
                        ></button>
                    </div>
                    <div id="jfilediv">
                        <input
                            id="jfile" type="file"
                            accept="application/json"
                        />
                    </div>
                </div>
                <div status="options">
                    <div>
                        {{!textFormatOpts}}
                    </div>
                    <div>
                        <input
                            class="r int" type="text" id="lnk" name="linked" value="{{linked}}"
                            placeholder="1"
                        /> <span class="ilab">link column</span>
                    </div>
                    <div>
                        <details id="condd" {{'open' if condensedAtt else ''}}>
                            <summary>
                                <input
                                    class="queryR" type="checkbox" id="cond" name="condensed" {{condensedAtt}}
                                /> <span class="ilab">condense results</span>
                            </summary>
                            {{!condenseOpts}}
                        </details>
                    </div>
                    <div>
                        <input
                            class="sectionsR tuplesR queryR" type="checkbox" id="withn" name="withNodes" {{withNodesAtt}}
                        /> <span class="ilab">show nodes</span>
                    </div>
                    {{!options}}
                </div>
                <div status="export">
                    <div>
                        <p class="ilab">Author</p>
                        <div>
                            <input
                                class="name" type="text" name="author" value="{{author}}"
                                placeholder="My Name"
                            />
                        </div>
                        <p class="ilab">Title</p>
                        <div>
                            <input
                                class="name" type="text" name="title" value="{{title}}"
                                placeholder="Title"
                            />
                        </div>
                        <p class="ilab">Description</p>
                        <div class="description">
                            <textarea
                                class="description" name="description"
                                placeholder="Description"
                            >{{description}}</textarea>
                        </div>
                        <p class="ilab">
                            <button
                                type="submit" formaction="/download" formtarget="_new"
                                title="download the data of this job"
                            ><span class="fa fa-download"/></button>
                            <button
                                type="submit" formaction="/export" formtarget="_new"
                                title="export this job in a new tab"
                            ><span class="fa fa-box-open"/></button>
                        </p>
                        <div id="queryMessages" class="messages">
                            {{messages}}
                        </div>
                    </div>
                </div>
                <div status="help">
                    <input type="hidden" id="help" name="help" value="{{help}}"/>
                    <div class="header">
                        {{!header}}
                    </div>
                    <details id="helpTf" class="help">
                        <summary>Text-Fabric Browser</summary>
                        <p>Explore the {{dataSource}} corpus.</p>
                        <p>Use the
                            <span class="sections">{{defaultCondenseType}}-</span>,
                            <span class="tuples">node-</span>, and
                            <span class="template">search-</span> pads
                            to specify material of interest.</p>
                        <p>Copy individual results to the <span class="tuples">node pad</span>
                           to compare them to each other.</p>
                        <p>Describe your study and export your work as a PDF with links
                           to archived copies of the {{dataSource}} corpus and this tool.</p>
                        <p>Open <b>multiple windows and tabs</b> with this url,
                           they all communicate with one and the same TF kernel;
                           the lengthy data loading only happens when the TF kernel starts up,
                           not when multiple webinterfaces communicate with the TF kernel.
                           See <i>Jobs</i> for ways to perform other queries.</p>
                        <p>When you terminate <code>text-fabric</code> on the command line,
                           the TF kernel will also be terminated.</p>
                    </details>
                    <details id="helpSections" class="help sections">
                        <summary>{{defaultCondenseType.capitalize()}} pad</summary>
                        <p>Enter a reference here,
                           such as {{!exampleSection}}.</p>
                        <p>Copy {{defaultCondenseType}}s to here by clicking on a
                           {{defaultCondenseType}} reference in the result list.</p>
                        <p>Click <b>Go</b> to fetch the results.</p>
                        <p>The results of the references appear in the result list,
                           with a negative sequence number.</p>
                    </details>
                    <details id="helpTuples" class="help tuples">
                        <summary>Node Pad</summary>
                        <p>Enter a node or list of nodes here,
                           such as <code>123</code> or
                           <code>123,456,789</code>.</p>
                        <p>Copy the nodes of a result to here by clicking on
                           the sequence number of a result in the result list.</p>
                        <p>Copy a node to here by clicking on its number
                           (when the option <i>show nodes</i> is checked).</p>
                        <p>Click <b>Go</b> to fetch the results.</p>
                        <p>The results of the nodes appear in the result list,
                           with a negative sequence number.</p>
                    </details>
                    <details id="helpTemplate" class="help query">
                        <summary>Search Pad</summary>
                        <p>Enter a search template here.
                           See the buttons on top for the docs.</p>
                        <p>Click <b>Go</b> to fetch the results.</p>
                        <p>The results of the search appear in the result list,
                           with a positive sequence number.</p>
                    </details>
                    <details id="helpResults" class="help">
                        <summary>Result list</summary>
                        <p>Show the text in the {{defaultTextFormat}} text format:
                           see the <i>text format</i> option.</p>
                        <p>Group results by {{defaultCondenseType}}:
                           see the <i>condense</i> option.</p>
                        <p>Click the triangle to expand a result into a pretty view.</p>
                        <p>If nothing happens, check the <i>condense</i> option:
                           objects that are bigger than the condense object type,
                           will not be expanded into pretty view. Either uncheck the 
                           <i>condense</i> option or select a bigger condense type.</p>
                        <p>Click the <i>expand all</i> checkbox to collapse and open all results.</p>
                        <p>Click the sequence number to add the nodes in this result to the <i>node pad</i>.</p>
                        <p>Click the reference, to add it to the <i>reference pad</i>.</p>
                        <p>Use the navigation button to walk through the results.<p>
                        <p>Results that you have expanded remain in view.</p>
                    </details>
                    <details id="helpJobs" class="help">
                        <summary>Jobs</summary>
                        <p>Your job will be saved in your browser</p>
                        <p>Rename or duplicate your job, by typing a new name in the name field.</p>
                        <p>Load an other job by selecting
                           the name under which it has been saved.
                           This job will be loaded in a new tab.
                           So you can work with multiple jobs in multiple tabs with only one running
                           <code>text-fabric</code> instance.</p>
                    </details>
                    <details id="helpOptions" class="help">
                        <summary>Options</summary>
                        <p><b>Link column</b> The column number whose contents will be hyperlinked to the online version
                           of the corpus.</p>
                        <p><b>Text format</b> Show the results in a text format of your choice: original script,
                           transcription, or phonetic representations may be offered.</p>
                        <p><b>Condense results</b> Show the results grouping all nodes in result tuples into
                           containers, such as {{defaultCondenseType}}s.
                           The containers are <i>pretty</i>-displayed, with the result nodes in it highlighted.
                           Choose the container type as you wish.</p>
                        <p><b>Show nodes</b> Show the node number for every object in the results.
                           The node number is your access to all information about that object.
                           If you click on it, it will be copied to the <i>node pad</i>.</p>
                    </details>
                    <details id="helpExport" class="help">
                        <summary>Export</summary>
                        <p>Export your results. Provide your name, title, and description (markdown is supported),
                           and click <b>Export</b>.</p>
                        <p>The exported page opens in a new window or tab, formatted for saving as PDF.<br/>
                           Use your browser to export this page to PDF.<br/>
                           The PDF will contain a complete description of your work, with persistent links
                           to the corpora and the tools, with additional metadata, and with the information
                           you specify. It reflects the results as you see them on your screen.</p>
                        <p>Additional data will be exported as files in a subdirectory corresponding to the current job:<br/>
                           (1) a file <code>RESULTSX.tsv</code>
                           with all your query results (uncondensed). <b>This file can directly be opened in Excel.</b>
                           Every row corresponds with a result tuple of nodes.
                           It contains result sequence number, a verse reference to where
                           the result occurs, and fields for the member nodes.
                           Every member of the result tuple corresponds to a few columns: node number, node type, full text,
                           and features that you have used in the search template for that node.<br/>
                           <b>Hint:</b> If you want to include more features, use them with a trivial condition in your template,
                           like so: <code>fff*</code> where <code>fff</code> is the name of your feature. The <code>*</code>
                           operator means: <i>no value restriction</i>.<br/>
                           (2) a markdown file <code>about.md</code> with the metadata and description.<br/>
                           (3) <code>.tsv</code> files corresponding to the results of the the contents of the pads: these
                           files contain the node numbers only.<br/>
                           (4) a file <code>CONTEXT.tsv</code> with full corpus information of every node in every result.</p>
                        <p><b>Tip</b> Archive the PDF and data files in an online repository, and you can cite your work properly.</p>
                    </details>
                </div>
            </div>
            <div class="leftcol">
                <p class="ilab">
                    <button
                        id="sectionsGo" class="xl fa fa-sync"
                        title="get {{defaultCondenseType}}s"
                        type="button"
                    ></button>
                    {{defaultCondenseType}} pad
                </p>
                <textarea
                    id="sections" class="sections" name="sections"
                    placeholder="{{exampleSectionText}}"
                >{{sections}}</textarea>
                <div id="sectionMessages" class="messages">
                </div>

                <hr>

                <p class="ilab">
                    <button
                        id="tuplesGo" class="xl fa fa-sync" type="button"
                        title="get nodes"
                    ></button>
                    node pad
                </p>
                <textarea
                    id="tuples" class="tuples" name="tuples"
                    placeholder="100,101,102"
                >{{tuples}}</textarea>
                <div id="tupleMessages" class="messages">
                </div>

                <hr>

                <p class="ilab">
                    <button
                        id="queryGo" class="xl" type="button"
                        title="run query and get results"
                    ><span class="fa fa-cog"/></button>
                    search pad
                </p>
                <textarea
                    id="query" class="query" name="query"
                    placeholder="{{defaultCondenseType}}"
                >{{query}}</textarea>
                <div id="setNames" class="setnames">
                </div>
                <div id="queryMessages" class="messages">
                </div>

                <hr>
            </div>
            <div class="midcol">
                <div class="materialnav">
                    <input type="hidden" name="mode" id="mode" value="{{mode}}"/>
                    <div>
                        <div id="navigation">
                            <div class="expand sections">
                                <span class="ilab sections">expand all {{defaultCondenseType}}s</span>
                                <input type="checkbox" id="sectionsExpac"/>
                                <input type="hidden" name="sectionsExpandAll" id="sectionsExpa" value="{{sectionsExpandAll}}"/>
                            </div>
                            <div class="expand tuples">
                                <span class="ilab tuples">expand all nodes</span>
                                <input type="checkbox" id="tuplesExpac"/>
                                <input type="hidden" name="tuplesExpandAll" id="tuplesExpa" value="{{tuplesExpandAll}}"/>
                            </div>
                            <div class="expand query">
                                <span class="ilab query">expand all results</span>
                                <input type="checkbox" id="queryExpac" />
                                <input type="hidden" name="queryExpandAll" id="queryExpa" value="{{queryExpandAll}}"/>
                            </div>
                            <div>
                                <input
                                    class="queryR int" type="text" id="pos" name="position" value="{{position}}"
                                /> <span class="ilab">current position</span>
                            </div>
                            <div>
                                <input
                                    class="queryR int" type="text" name="batch" value="{{batch}}"
                                /> <span class="ilab">results per page</span>
                            </div>
                        </div>
                        <p class="ilab"><a href="#" id="moderesults">Results</a></p>
                        <div class="pages" id="pages">
                            {{!pages}}
                        </div>
                    </div>
                    <div>
                        <p class="ilab"><a href="#" id="modepassage">Passage</a></p>
                        <input type="hidden" name="sec0" id="sec0" value="{{sec0}}"/>
                        <input type="hidden" name="sec1" id="sec1" value="{{sec1}}"/>
                        <input type="hidden" name="sec2" id="sec2" value="{{sec2}}"/>
                        <div class="passages" id="passages">{{!passages}}</div>
                    </div>
                </div>
            </div>
            <div class="rightcolx">
                <input type="hidden" id="passageOp" name="passageOpened" value=""/>
                <input type="hidden" id="sectionsOp" name="sectionsOpened" value=""/>
                <input type="hidden" id="tuplesOp" name="tuplesOpened" value=""/>
                <input type="hidden" id="queryOp" name="queryOpened" value=""/>
                <input type="hidden" id="features" name="features" value="{{features}}"/>
                <div id="sectionsTable" class="table"></div>
                <div id="tuplesTable" class="table"></div>
                <div id="queryTable" class="table"></div>
                <div id="passageTable" class="table"></div>
            </div>
        </div>
        </form>
        <script src="/server/static/jquery.js"></script>
        <script src="/server/static/tfx.js"/></script>
    </body>
</html>